"""
Module for checking for naming conflicts of predicates.
"""

from clingo.ast import AST, ASTType, Transformer
from clingo.symbol import SymbolType

from ..utils.data import Auxiliaries, Predicate
from ..utils.logging import get_logger
from . import collect_privates, get_replacements, replace_predicates

log = get_logger(__name__)


def collect_ground_terms(program: list[AST]) -> set[str]:
    """
    Collect all ground terms occurring in a program.
    """
    collector = GroundTermCollector()
    for node in program:
        collector(node)
    return collector.terms


def check_and_rename_auxiliaries(
    left: list[AST], right: list[AST], publics: set[Predicate], aux: Auxiliaries, ground_terms: set[str]
) -> Auxiliaries:
    """
    Check the auxiliaries for conflicts with the two programs.
    """
    privates = collect_privates(left + right, publics)
    predicates = publics | privates
    conflict_predicates = _conflicting_predicates(predicates, aux.predicates())
    if conflict_predicates:
        replacements = get_replacements(conflict_predicates, predicates)
        aux = aux.replace_values(replacements)

    placeholders = _collect_placeholders(left + right)
    if aux.size in placeholders or aux.size in ground_terms:
        new_placeholder = _get_fresh_placeholder(aux.size, placeholders | ground_terms)
        log.debug("new size placeholder is %s", new_placeholder)
        aux = aux.replace(size=new_placeholder)

    if _contains_suffix(publics | privates, aux.suffix):
        new_suffix = _get_fresh_suffix(aux.suffix, publics | privates)
        log.debug("new predicate suffix is %s", new_suffix)
        aux = aux.replace(suffix=new_suffix)

    return aux


def check_and_rename_privates(
    left: list[AST], right: list[AST], publics: set[Predicate]
) -> tuple[list[AST], list[AST]]:
    """
    Check if the private predicates of the programs are distinct and rename conflicting predicates if necessary.
    """
    privates_left = collect_privates(left, publics)
    privates_right = collect_privates(right, publics)
    conflicts = _conflicting_predicates(privates_left, privates_right)
    if conflicts:
        for pred in conflicts:
            log.warning("found conflicting private predicate %s, applying renaming", pred)

        replacements = get_replacements(conflicts, publics | privates_left | privates_right)

        right = replace_predicates(right, replacements)

    return left, right


def _get_fresh_placeholder(base: str, placeholders: set[str]) -> str:
    i = 0
    new = f"{base}__{i}"
    while new in placeholders:
        i += 1
        new = f"{base}__{i}"

    return new


def _get_fresh_suffix(base: str, predicates: set[Predicate]) -> str:
    i = 0
    new = f"{base}{i}"
    while _contains_suffix(predicates, new):
        i += 1
        new = f"{base}{i}"

    return new


def _collect_placeholders(program: list[AST]) -> set[str]:
    collector = PlaceholderCollector()
    for n in program:
        collector(n)

    return collector.placeholders


def _conflicting_predicates(left: set[Predicate], right: set[Predicate]) -> set[Predicate]:
    return left & right


def _contains_suffix(predicates: set[Predicate], suffix: str) -> bool:
    return any(p.name.endswith(suffix) for p in predicates)


class _VariableChecker(Transformer):
    def __init__(self) -> None:
        super().__init__()
        self.has_variable: bool = False

    def visit_Variable(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """If visiting a variable set the has_variable to True."""
        self.has_variable = True
        return node


def _is_ground(node: AST) -> bool:
    checker = _VariableChecker()
    checker(node)
    return not checker.has_variable


class GroundTermCollector(Transformer):
    """
    Class to collect all ground terms occurring in a program.
    """

    def __init__(self) -> None:
        """Initialize an empty set of ground terms."""
        super().__init__()
        self.terms: set[str] = set()

    def visit_SymbolicAtom(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Explicitly visit only the arguments of the atom to avoid collecting the predicate symbol.
        """
        if node.symbol.ast_type == ASTType.Function:
            for arg in node.symbol.arguments:
                self(arg)
        elif node.symbol.ast_type == ASTType.Pool:
            for func in node.symbol.arguments:
                if func.ast_type == ASTType.Function:
                    for arg in func.arguments:
                        self(arg)
        return node

    def visit_Function(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Collect ground function terms and recurse into arguments.
        """
        if _is_ground(node):
            self.terms.add(str(node))
        self.visit_children(node)
        return node

    def visit_SymbolicTerm(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Collect symbolic terms (numbers and symbolic constants), excluding #inf and #sup.
        """
        if node.symbol.type not in (SymbolType.Infimum, SymbolType.Supremum):
            self.terms.add(str(node))
        return node

    def visit_UnaryOperation(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Collect ground unary operations and recurse into sub-terms.
        """
        if _is_ground(node):
            self.terms.add(str(node))
        self.visit_children(node)
        return node

    def visit_BinaryOperation(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Collect ground binary operations and recurse into sub-terms.
        """
        if _is_ground(node):
            self.terms.add(str(node))
        self.visit_children(node)
        return node


class PlaceholderCollector(Transformer):
    """
    Class to collect placeholders of a program.
    """

    def __init__(self) -> None:
        """Initialize an empty set of placeholders."""
        super().__init__()
        self.placeholders: set[str] = set()

    def visit_Definition(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Add the placeholder to the set of all placeholders.
        """
        self.placeholders.add(node.name)
        return node
