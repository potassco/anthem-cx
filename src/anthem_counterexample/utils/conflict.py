"""
Module for checking for naming conflicts of predicates.
"""

from clingo.ast import AST, ASTType, Transformer

from . import Auxiliaries, Predicate
from .logging import get_logger
from .output import program_to_str
from .transformation import apply_transformer, atom_to_predicate, replace_predicate

log = get_logger(__name__)


def check_and_rename_auxiliaries(
    left: list[AST], right: list[AST], publics: set[Predicate], aux: Auxiliaries
) -> Auxiliaries:
    """
    Check the auxiliaries for conflicts with the two programs.
    """
    privates = _collect_privates(left + right, publics)
    predicates = publics | privates
    conflict_predicates = _conflicting_predicates(predicates, aux.predicates())
    if conflict_predicates:
        replacements, predicates = _get_replacements(conflict_predicates, predicates)
        aux = aux.replace_values(replacements)

    placeholders = _collect_placeholders(left + right)
    if aux.size in placeholders:
        new_placeholder = _get_fresh_placeholder(aux.size, placeholders)
        log.debug("new size placegolder is %s", new_placeholder)
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
    privates_left = _collect_privates(left, publics)
    privates_right = _collect_privates(right, publics)
    conflicts = _conflicting_predicates(privates_left, privates_right)
    if conflicts:
        for pred in conflicts:
            log.warning("found conflicting private predicate %s", pred)

        replacements, _ = _get_replacements(conflicts, publics | privates_left | privates_right)

        right = _replace_predicates(right, replacements)

    return left, right


def _get_replacements(
    conflicts: set[Predicate], predicates: set[Predicate]
) -> tuple[dict[Predicate, Predicate], set[Predicate]]:
    pred_replacements = {}
    for pred in conflicts:
        new = _get_replacement_predicate(pred, predicates)
        pred_replacements[pred] = new
        predicates.add(new)
        log.debug("Replacement for %s is %s", pred, new)
    return pred_replacements, predicates


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


def _get_replacement_predicate(base: Predicate, predicates: set[Predicate]) -> Predicate:
    """
    Get a replacement predicate for base that does not conflict with predicates.
    """
    i = 0
    new = Predicate(base.name + f"__{i}", base.arity)
    while new in predicates:
        i += 1
        new = Predicate(base.name + f"__{i}", base.arity)

    return new


def _replace_predicates(program: list[AST], replacements: dict[Predicate, Predicate]) -> list[AST]:
    """
    Replace all predicates that are part of the replacement dictionary.
    """
    program = apply_transformer(PredicateReplacer(replacements), program)
    log.debug("Program after replacing conflicting predicates")
    log.debug(program_to_str(program, True))
    return program


def _collect_placeholders(program: list[AST]) -> set[str]:
    collector = PlaceholderCollector()
    for n in program:
        collector(n)

    return collector.placeholders


def _collect_privates(program: list[AST], publics: set[Predicate]) -> set[Predicate]:
    collector = PrivatePredicateCollector(publics)
    for n in program:
        collector(n)

    return collector.privates


def _conflicting_predicates(left: set[Predicate], right: set[Predicate]) -> set[Predicate]:
    return left & right


def _contains_suffix(predicates: set[Predicate], suffix: str) -> bool:
    for p in predicates:
        if p.name.endswith(suffix):
            return True
    return False


class PlaceholderCollector(Transformer):
    """
    Class to collect placeholders of a program.
    """

    def __init__(self) -> None:
        super().__init__()
        self.placeholders: set[str] = set()

    def visit_Definition(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Add the placeholder to the set of all placeholders.
        """
        self.placeholders.add(node.name)
        return node


class PrivatePredicateCollector(Transformer):
    """
    Class to collect the private predicates of a program.
    """

    def __init__(self, publics: set[Predicate]) -> None:
        super().__init__()
        self.publics = publics
        self.privates: set[Predicate] = set()

    def visit_SymbolicAtom(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Add the predicate of a symbolic atom to the privates if it is not public.
        """
        if node.symbol.ast_type in [ASTType.Function, ASTType.Pool]:
            pred = atom_to_predicate(node)
            if pred not in self.publics:
                self.privates.add(pred)

        return node


class PredicateReplacer(Transformer):
    """
    Class to replace predicates according to a replacement dictionary.
    """

    def __init__(self, replacements: dict[Predicate, Predicate]) -> None:
        super().__init__()
        self.replacements = replacements

    def visit_SymbolicAtom(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Replace the predicate of a symbolic atom if it is part of the replacements.
        """
        if node.symbol.ast_type in [ASTType.Function, ASTType.Pool]:
            pred = atom_to_predicate(node)
            if pred in self.replacements:
                return replace_predicate(node, self.replacements[pred])

        return node
