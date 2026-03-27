"""
Module for checking for naming conflicts of predicates.
"""

from clingo.ast import AST, Transformer

from . import Auxiliaries, Predicate
from .logging import get_logger
from .transformation import atom_to_predicate

log = get_logger(__name__)


def check_and_rename_auxiliaries(
    left: list[AST], right: list[AST], publics: set[Predicate], aux: Auxiliaries
) -> Auxiliaries:
    privates = _collect_privates(left + right, publics)
    conflict_predicates = _conflicting_predicates(publics | privates, aux.predicates())
    if conflict_predicates:
        log.error("Renaming of conflicting auxiliary predicates not yet supported")
        raise RuntimeError(f"Found conflicting auxiliary predicates {[str(p) for p in conflict_predicates]}")

    placeholders = _collect_placeholders(left + right)
    if aux.size in placeholders:
        log.error("Renaming of size placegolder not yet supported")
        raise RuntimeError("Size placeholder conlficts with a placeholder in the programs")

    if _contains_suffix(publics | privates, aux.suffix):
        log.error("Renaming of the predicate suffix not yet supported")
        raise RuntimeError("Predicate suffix conflicting with some predicate name")

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
        log.error("Renaming of conflicting private predicates not yet supported")
        raise RuntimeError(f"Found conflicting private predicates: {[str(p) for p in conflicts]}")

    return left, right


def _collect_placeholders(program: list[AST]) -> set[str]:
    log.error("Collect placeholder not yet implemented")
    return set()


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
        pred = atom_to_predicate(node)
        if pred not in self.publics:
            self.privates.add(pred)

        return node
