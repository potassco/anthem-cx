"""
Shared analysis utilities.
"""

from clingo.ast import AST, ASTType, Transformer

from ..utils.data import Predicate
from ..utils.logging import get_logger
from ..utils.output import program_to_str
from ..utils.transformation import apply_transformer, atom_to_predicate, replace_predicate

log = get_logger(__name__)


def collect_privates(program: list[AST], publics: set[Predicate]) -> set[Predicate]:
    """
    Collect the private predicates of a program (those not in publics).
    """
    collector = PrivatePredicateCollector(publics)
    for n in program:
        collector(n)

    return collector.privates


def replace_predicates(program: list[AST], replacements: dict[Predicate, Predicate]) -> list[AST]:
    """
    Replace all predicates that are part of the replacement dictionary.
    """
    program = apply_transformer(PredicateReplacer(replacements), program)
    log.debug("Program after replacing conflicting predicates")
    log.debug(program_to_str(program, True))
    return program


def get_replacements(conflicts: set[Predicate], predicates: set[Predicate]) -> dict[Predicate, Predicate]:
    """
    Get fresh replacement predicates for all conflicts, avoiding predicates.
    """
    pred_replacements = {}
    for pred in conflicts:
        new = get_replacement_predicate(pred, predicates)
        pred_replacements[pred] = new
        # extend the set of predicates avoid collision with new replacements
        predicates.add(new)
        log.debug("Replacement for %s is %s", pred, new)
    return pred_replacements


def get_replacement_predicate(base: Predicate, predicates: set[Predicate]) -> Predicate:
    """
    Get a replacement predicate for base that does not conflict with predicates.
    """
    i = 0
    new = Predicate(base.name + f"__{i}", base.arity)
    while new in predicates:
        i += 1
        new = Predicate(base.name + f"__{i}", base.arity)

    return new


class PrivatePredicateCollector(Transformer):
    """
    Class to collect the private predicates of a program.
    """

    def __init__(self, publics: set[Predicate]) -> None:
        """Store the public predicates and prepare the private set."""
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
        """Store the predicate replacement mapping."""
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
