"""
Module for checking dependencies in a logic program.
"""

from abc import ABC, abstractmethod

from clingo.ast import AST, ASTType, Sign, Transformer
from networkx import DiGraph, MultiDiGraph, simple_cycles, strongly_connected_components

from ..utils.data import Predicate
from ..utils.logging import get_logger
from ..utils.transformation import atom_to_predicate

log = get_logger(__name__)


def _parity_node_to_str(node) -> str:  # type: ignore
    pred, bit = node
    return f"({pred}, {bit})"


def _nodes_to_str(nodes, to_str=str) -> str:  # type: ignore
    ret_str = "["
    for i, n in enumerate(nodes):
        if i > 0:
            ret_str += ", "
        ret_str += to_str(n)
    ret_str += "]"
    return ret_str


def _edges_to_str(edges, data: bool = False, to_str=str) -> str:  # type: ignore
    ret_str = "["
    for i, e in enumerate(edges):
        if i > 0:
            ret_str += ", "
        if data:
            ret_str += "((" + to_str(e[0]) + "," + to_str(e[1]) + "), " + str(e[2]["weight"]) + ")"
        else:
            ret_str += "(" + to_str(e[0]) + "," + to_str(e[1]) + ")"
    ret_str += "]"
    return ret_str


def _cycles_to_str(cycles) -> str:  # type: ignore
    ret_str = "{"
    for i, c in enumerate(cycles):
        if i > 0:
            ret_str += ", "
        ret_str += _nodes_to_str(c)
    ret_str += "}"
    return ret_str


def _build_signed_graph(program: list[AST], public_predicates: set[Predicate]) -> "MultiDiGraph[Predicate]":
    """
    Build the signed predicate dependency graph and log its nodes and edges.
    """
    graph_builder = SignedDependencyGraphBuilder(public_predicates)
    for n in program:
        graph_builder(n)

    graph = graph_builder.graph

    log.debug("Nodes: %s", _nodes_to_str(graph.nodes))
    log.debug("Edges: %s", _edges_to_str(graph.edges(data=True), True))

    return graph


def has_negative_cycle(program: list[AST], public_predicates: set[Predicate]) -> bool:
    """
    Check if a program fulfills uniqueness by checking a modified predicate dependency graph for negative cycles.
    """
    log.debug("Building signed dependency graph for has_negative_cycle")
    graph = _build_signed_graph(program, public_predicates)

    for scc in strongly_connected_components(graph):
        subgraph = graph.subgraph(scc)
        for _, _, data in subgraph.edges(data=True):
            if data.get("weight", 0) < 0:
                log.debug("SCC with negative loop: %s", _nodes_to_str(scc))
                return True

    return False


def has_odd_negative_cycle(program: list[AST], public_predicates: set[Predicate]) -> bool:
    """
    Check if a program has a negative cycle with an odd number of negations.

    Only negated literals of private predicates are taken into account (exactly as for
    has_negative_cycle). A single negation counts as one negation while a double negation
    (including the implicit double negation of a private choice rule) counts as two; the
    latter therefore does not change the parity of a cycle.

    The check reduces to a parity problem: the number of negations on a cycle is odd iff
    the number of single-negation private edges on it is odd. To detect such a cycle we
    build a parity-doubled graph with two copies of every node tagged with a parity bit,
    where traversing an edge flips the bit by the edge's parity. A directed cycle with odd
    parity through v then corresponds to (v, 0) and (v, 1) lying in the same strongly
    connected component of the doubled graph.
    """
    log.debug("Building signed dependency graph for has_odd_negative_cycle")
    graph = _build_signed_graph(program, public_predicates)

    log.debug("Building parity graph for has_odd_negative_cycle")
    doubled: "DiGraph[tuple[Predicate, int]]" = DiGraph()  # pylint: disable=unsubscriptable-object
    for u, v, data in graph.edges(data=True):
        parity = data.get("parity", 0)
        doubled.add_edge((u, 0), (v, parity))
        doubled.add_edge((u, 1), (v, 1 - parity))

    log.debug("Parity nodes: %s", _nodes_to_str(doubled.nodes, _parity_node_to_str))
    log.debug("Parity edges: %s", _edges_to_str(doubled.edges, to_str=_parity_node_to_str))

    for scc in strongly_connected_components(doubled):
        both = {node for node, bit in scc if bit == 0} & {node for node, bit in scc if bit == 1}
        if both:
            log.debug("SCC with odd negative cycle: %s", _nodes_to_str(scc))
            return True

    return False


def has_recursive_aggregates(program: list[AST]) -> bool:
    """
    Check if a program contains recursive aggregates.
    """
    log.debug("Building aggregate dependency graph for has_recursive_aggregates")
    graph_builder = AggregateDependencyGraphBuilder()
    for n in program:
        graph_builder(n)

    graph = graph_builder.graph
    cycles = list(simple_cycles(graph))

    log.debug("Nodes: %s", _nodes_to_str(graph.nodes))
    log.debug("Edges: %s", _edges_to_str(graph.edges))
    if cycles:
        log.debug("Cycles: %s", _cycles_to_str(cycles))
    else:
        log.debug("No cycles found")

    return bool(cycles)


class DependencyGraphBuilder(Transformer, ABC):
    """
    Base class for dependency graphs.
    """

    def __init__(self) -> None:
        super().__init__()
        self.graph: MultiDiGraph[Predicate] = MultiDiGraph()  # pylint: disable=unsubscriptable-object
        self.current_head: Predicate | None = None

    def _add_node_and_set_current(self, atom: AST) -> Predicate:
        if atom.ast_type != ASTType.SymbolicAtom:
            raise RuntimeError(f"Unexpected atom {atom}")  # nocoverage

        pred = atom_to_predicate(atom)
        self.graph.add_node(pred)
        self.current_head = pred

        return pred

    def visit_Rule(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Process each rule: add head predicate as node and process body.
        """
        self.current_head = None

        if node.head.ast_type == ASTType.Literal:
            if node.head.atom.ast_type == ASTType.SymbolicAtom:
                self._add_node_and_set_current(node.head.atom)
                self.visit_sequence(node.body)

        elif node.head.ast_type == ASTType.Aggregate:
            if len(node.head.elements) > 1:
                raise ValueError(f"Choice rule should not have more than 1 element: {node}")

            element = node.head.elements[0]

            match element.ast_type:
                case ASTType.ConditionalLiteral:
                    self._add_node_and_set_current(element.literal.atom)
                case ASTType.Literal:  # nocoverage
                    self._add_node_and_set_current(element.atom)
                case _:  # nocoverage
                    raise ValueError(f"Unexpected choice element: {element}")

            self.visit_sequence(node.body)

        return node

    @abstractmethod
    def visit_Literal(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Subclasses implement adding dependencies for literals.
        """
        raise NotImplementedError  # nocoverage


class SignedDependencyGraphBuilder(DependencyGraphBuilder):
    """
    Transformer to build a predicate dependency graph.
    """

    def __init__(self, public_predicates: set[Predicate]) -> None:
        super().__init__()
        self._public_predicates = public_predicates

    def _is_private(self, pred: Predicate) -> bool:
        return pred not in self._public_predicates

    def visit_Rule(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Process each rule: add head predicate as node and process body.

        If head is a choice add a self edge.
        """
        self.current_head = None

        if node.head.ast_type == ASTType.Literal:
            if node.head.atom.ast_type == ASTType.SymbolicAtom:
                self._add_node_and_set_current(node.head.atom)
                self.visit_sequence(node.body)

        elif node.head.ast_type == ASTType.Aggregate:
            if len(node.head.elements) > 1:
                raise ValueError(f"Choice rule should not have more than 1 element: {node}")

            element = node.head.elements[0]

            match element.ast_type:
                case ASTType.ConditionalLiteral:
                    pred = self._add_node_and_set_current(element.literal.atom)
                case ASTType.Literal:  # nocoverage
                    pred = self._add_node_and_set_current(element.atom)
                case _:  # nocoverage
                    raise ValueError(f"Unexpected choice element: {element}")

            # a private choice corresponds to a double negation, hence parity 0
            if self._is_private(pred):
                self.graph.add_edge(pred, pred, weight=-1, parity=0)

            self.visit_sequence(node.body)

        return node

    def visit_Literal(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Process body literals: add a edge for body predicates.
        """
        if self.current_head is None:
            return node

        atom = node.atom

        if atom.ast_type != ASTType.SymbolicAtom:
            return node

        body_pred = atom_to_predicate(atom)
        self.graph.add_node(body_pred)

        # add all positive dependencies with weight 0 and parity 0
        if node.sign == Sign.NoSign:
            weight = 0
            parity = 0
        # add negative dependencies of private predicates with weight -1;
        # a single negation has parity 1, a double negation parity 0
        elif self._is_private(body_pred):
            weight = -1
            parity = 1 if node.sign == Sign.Negation else 0
        # ignore negative dependencies of public predicates
        else:
            return node

        self.graph.add_edge(self.current_head, body_pred, weight=weight, parity=parity)

        return node


class AggregateDependencyGraphBuilder(DependencyGraphBuilder):
    """
    Build an aggregate dependency graph.
    """

    def _extend_predicates_by_literal(self, node: AST, predicates: set[Predicate]) -> set[Predicate]:
        """
        Extend a set of predicates by the predicate of a literal.
        """
        if node.ast_type != ASTType.Literal:
            raise ValueError(f"The AST node is not a literal: {node}")  # nocoverage

        atom = node.atom
        if atom.ast_type == ASTType.SymbolicAtom:
            predicates.add(atom_to_predicate(atom))

        return predicates

    def _predicates_in_aggregate(self, node: AST) -> set[Predicate]:
        """
        Get the set of predicates occurring in an aggregate.
        """
        preds: set[Predicate] = set()
        match node.ast_type:
            case ASTType.BodyAggregate:
                for elem in node.elements:
                    for lit in elem.condition:
                        preds = self._extend_predicates_by_literal(lit, preds)
            case ASTType.Aggregate:
                for elem in node.elements:
                    preds = self._extend_predicates_by_literal(elem.literal, preds)

                    for lit in elem.condition:
                        preds = self._extend_predicates_by_literal(lit, preds)
            case _:  # nocoverage
                raise ValueError(f"The AST node is not an aggregate: {node}")

        return preds

    def visit_Literal(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Process body literals: add a edge for each predicate in an aggregate.
        """
        if self.current_head is None:
            return node

        if node.atom.ast_type in (ASTType.BodyAggregate, ASTType.Aggregate):
            preds = self._predicates_in_aggregate(node.atom)
            for pred in preds:
                self.graph.add_edge(self.current_head, pred)

        return node
