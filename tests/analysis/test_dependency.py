"""
Tests for analysis/dependency.py.
"""

from unittest import TestCase

from clingo.ast import ASTType

from anthem_cx.analysis.dependency import (
    AggregateDependencyGraphBuilder,
    SignedDependencyGraphBuilder,
    _cycles_to_str,
    _edges_to_str,
    _nodes_to_str,
    _parity_node_to_str,
    has_negative_cycle,
    has_odd_negative_cycle,
    has_recursive_aggregates,
)
from anthem_cx.utils.data import Predicate

from . import parse_program


class TestStringHelpers(TestCase):
    """Tests for _nodes_to_str, _edges_to_str, _cycles_to_str."""

    def test_nodes_to_str(self) -> None:
        """Test conversion of nodes to str."""
        for nodes, expected in [
            ([], "[]"),
            (["a"], "[a]"),
            (["a", "b", "c"], "[a, b, c]"),
        ]:
            self.assertEqual(_nodes_to_str(nodes), expected)

    def test_edges_to_str(self) -> None:
        """Test conversion of edges to str."""
        for edges, data, expected in [
            ([], False, "[]"),
            ([("a", "b"), ("c", "d")], False, "[(a,b), (c,d)]"),
            ([("a", "b", {"weight": -1}), ("c", "d", {"weight": 0})], True, "[((a,b), -1), ((c,d), 0)]"),
        ]:
            self.assertEqual(_edges_to_str(edges, data), expected)

    def test_parity_node_to_str(self) -> None:
        """Test conversion of a parity-doubled node to str."""
        for node, expected in [
            ((Predicate("a", 0), 0), "(a/0, 0)"),
            ((Predicate("b", 2), 1), "(b/2, 1)"),
        ]:
            self.assertEqual(_parity_node_to_str(node), expected)

    def test_edges_to_str_parity_formatter(self) -> None:
        """Test edge conversion using a custom node formatter."""
        edges = [((Predicate("a", 0), 0), (Predicate("b", 0), 1))]
        self.assertEqual(_edges_to_str(edges, to_str=_parity_node_to_str), "[((a/0, 0),(b/0, 1))]")

    def test_cycles_to_str(self) -> None:
        """Test conversion of cycles to str."""
        for cycles, expected in [
            ([], "{}"),
            ([["a", "b"]], "{[a, b]}"),
            ([["a"], ["b", "c"]], "{[a], [b, c]}"),
        ]:
            self.assertEqual(_cycles_to_str(cycles), expected)


class TestHasNegativeCycle(TestCase):
    """Tests for has_negative_cycle (signed dependency graph analysis)."""

    def test_no_negative_cycle(self) -> None:
        """Test cases that do not have a negative cycle."""
        for prog, publics in [
            ("", set()),
            ("a :- not b.", {Predicate("a", 0), Predicate("b", 0)}),
            ("a :- b. b :- a.", set()),
            ("{a}.", {Predicate("a", 0)}),
            ("a :- 1 < 2.", {Predicate("a", 0)}),
            (":- a.", set()),
            ("a :- 1 <= #count{ 1 : b }.", {Predicate("a", 0), Predicate("b", 0)}),
        ]:
            self.assertFalse(has_negative_cycle(parse_program(prog), publics))

    def test_has_negative_cycle(self) -> None:
        """Test cases that have a negative cycle."""
        for prog, publics in [
            ("{a}.", set()),
            ("a :- not b. b :- not a.", set()),
            ("a :- not a. b :- a.", {Predicate("b", 0)}),
        ]:
            self.assertTrue(has_negative_cycle(parse_program(prog), publics))

    def test_signed_builder_visit_literal_null_head(self) -> None:
        """visit_Literal returns the node unchanged when current_head is None."""
        prog = parse_program("a :- b.")
        rules = [n for n in prog if n.ast_type == ASTType.Rule]
        body_literal = rules[0].body[0]
        builder = SignedDependencyGraphBuilder(set())
        result = builder.visit_Literal(body_literal)
        self.assertEqual(result, body_literal)

    def test_raises_on_multi_element_choice(self) -> None:
        """A choice rule with more than one element raises ValueError."""
        prog = parse_program("{a;b}.")
        builder = SignedDependencyGraphBuilder(set())
        with self.assertRaises(ValueError):
            for n in prog:
                builder(n)


class TestHasOddNegativeCycle(TestCase):
    """Tests for has_odd_negative_cycle (parity-doubled dependency graph analysis)."""

    def test_no_odd_negative_cycle(self) -> None:
        """Test cases that do not have an odd negative cycle."""
        for prog, publics in [
            # no cycle at all
            ("", set()),
            ("a :- not b.", {Predicate("a", 0), Predicate("b", 0)}),
            # positive cycle (parity 0)
            ("a :- b. b :- a.", set()),
            # even negative cycle: two single negations sum to parity 0
            ("a :- not b. b :- not a.", set()),
            # double negation counts as two negations -> parity 0
            ("a :- not not a.", set()),
            # private choice corresponds to a double negation -> parity 0
            ("{a}.", set()),
            # negation of a public predicate is ignored
            ("a :- not a.", {Predicate("a", 0)}),
        ]:
            self.assertFalse(has_odd_negative_cycle(parse_program(prog), publics))

    def test_has_odd_negative_cycle(self) -> None:
        """Test cases that have an odd negative cycle."""
        cases: list[tuple[str, set[Predicate]]] = [
            # single negation self-loop
            ("a :- not a.", set()),
            # one single negation, one positive edge -> parity 1
            ("a :- not b. b :- a.", set()),
            # three single negations -> parity 1
            ("a :- not b. b :- not c. c :- not a.", set()),
            # double negation is necessary to close the loop; parity 0 + 1 = 1
            ("a :- not not b. b :- not a.", set()),
        ]
        for prog, publics in cases:
            self.assertTrue(has_odd_negative_cycle(parse_program(prog), publics))


class TestHasRecursiveAggregates(TestCase):
    """Tests for has_recursive_aggregates and AggregateDependencyGraphBuilder internals."""

    def test_success(self) -> None:
        """Test cases with recursive aggregates."""
        for prog in [
            "a :- 1 <= #count{ 1 : a }.",
            "a :- 1 <= { a }.",
            "a :- 1 <= { b : a }.",
        ]:
            self.assertTrue(has_recursive_aggregates(parse_program(prog)))

    def test_failure(self) -> None:
        """Test cases without recursive aggregates."""
        for prog in [
            "",
            "a :- b.",
            "a :- 1 <= #count{ X : b(X) }.",
            "a :- 1 <= #count{ a : b }.",
            "{a} :- a.",
        ]:
            self.assertFalse(has_recursive_aggregates(parse_program(prog)))

    def test_aggregate_builder_visit_literal_null_head(self) -> None:
        """visit_Literal returns the node unchanged when current_head is None."""
        prog = parse_program("a :- b.")
        rules = [n for n in prog if n.ast_type == ASTType.Rule]
        body_literal = rules[0].body[0]
        builder = AggregateDependencyGraphBuilder()
        result = builder.visit_Literal(body_literal)
        self.assertEqual(result, body_literal)

    def test_aggregate_builder_visit_literal_non_aggregate_body(self) -> None:
        """visit_Literal with a non-aggregate body literal returns the node unchanged."""
        prog = parse_program("a :- b.")
        rules = [n for n in prog if n.ast_type == ASTType.Rule]
        body_literal = rules[0].body[0]
        builder = AggregateDependencyGraphBuilder()
        for n in parse_program("a."):
            builder(n)
        result = builder.visit_Literal(body_literal)
        self.assertEqual(result, body_literal)

    def test_aggregate_builder_raises_on_multi_element_choice(self) -> None:
        """A choice rule head with more than one element raises ValueError."""
        prog = parse_program("{a;b}.")
        builder = AggregateDependencyGraphBuilder()
        with self.assertRaises(ValueError):
            for n in prog:
                builder(n)
