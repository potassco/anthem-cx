"""
Module to check that programs do not contain inputs in their rule heads.
"""

from clingo.ast import AST, Transformer

from ..utils.data import Predicate
from ..utils.errors import AnthemCXError
from ..utils.logging import get_logger
from ..utils.transformation import atom_to_predicate, head_atom

log = get_logger(__name__)


def check_inputs_not_in_heads(left: list[AST], right: list[AST], inputs: set[Predicate]) -> None:
    """
    Check that neither program contains an input predicate in a rule head.

    Raises an AnthemCXError (causing anthem-cx to exit) if an input predicate occurs in a head.
    The programs are expected to be normalized.
    """
    for program, name in [(left, "left"), (right, "right")]:
        conflicts = inputs_in_heads(program, inputs)
        if conflicts:
            predicates = ", ".join(str(p) for p in sorted(conflicts, key=str))
            raise AnthemCXError(f"input predicate(s) in the head of the {name} program: {predicates}")


def inputs_in_heads(program: list[AST], inputs: set[Predicate]) -> set[Predicate]:
    """
    Get the input predicates occurring in the rule heads of a program.

    Returns the set of input predicates that occur in a head (empty if the program is valid).
    The program is expected to be normalized.
    """
    return collect_head_predicates(program) & inputs


def collect_head_predicates(program: list[AST]) -> set[Predicate]:
    """
    Collect all predicates occurring in the rule heads of a normalized program.
    """
    collector = HeadPredicateCollector()
    for node in program:
        collector(node)
    return collector.predicates


class HeadPredicateCollector(Transformer):
    """
    Class to collect the head predicates of a normalized program.
    """

    def __init__(self) -> None:
        """Initialize an empty set of head predicates."""
        super().__init__()
        self.predicates: set[Predicate] = set()

    def visit_Rule(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Collect the head predicate of a rule.

        Handles literal heads and (normalized) choice heads; empty heads
        (constraints) contribute no predicate.
        """
        atom = head_atom(node)
        if atom is not None:
            self.predicates.add(atom_to_predicate(atom))

        return node
