"""
Module to get counterexample program.
"""

from clingo.ast import AST

from .transformation import (
    ChoiceConditionNormalizer,
    ChoiceElementNormalizer,
    ChoiceGuardNormalizer,
    ChoicePoolNormalizer,
    ChoiceTermNormalizer,
    HeadAggregateNormalizer,
    NormalizeHead,
    RejectClassicalNegation,
    RejectDisjunctions,
    RemoveHeadCondition,
    ReplacePositiveOutputPredicates,
    TransformRuleHeads,
)
from .utils.data import Auxiliaries, Predicate
from .utils.logging import TRACE, get_logger
from .utils.output import atom_str, program_to_str, variable_names
from .utils.transformation import apply_transformer

log = get_logger(__name__)


def normalize_program(prog: list[AST]) -> list[AST]:
    """
    Normalize a logic program.
    """
    for t in [
        RejectDisjunctions,
        RejectClassicalNegation,
        RemoveHeadCondition,
        HeadAggregateNormalizer,
        ChoiceGuardNormalizer,
        ChoiceElementNormalizer,
        ChoicePoolNormalizer,
        ChoiceTermNormalizer,
        ChoiceConditionNormalizer,
        NormalizeHead,
    ]:
        prog = apply_transformer(t(), prog)
        log.log(TRACE, "Program after applying %s", t.__name__)
        log.log(TRACE, program_to_str(prog, True))

    log.debug("Normalized program")
    log.debug(program_to_str(prog, True))

    return prog


def get_public_reduct(prog: list[AST], outputs: set[Predicate], auxiliaries: Auxiliaries) -> list[AST]:
    """
    Compute the public reduct of a program with respect to a set of output predicates.
    """
    for t in [ReplacePositiveOutputPredicates, TransformRuleHeads]:
        prog = apply_transformer(t(outputs, auxiliaries), prog)
        log.log(TRACE, "Program after applying %s", t.__name__)
        log.log(TRACE, program_to_str(prog, True))

    log.debug("Public reduct")
    log.debug(program_to_str(prog, True))

    return prog


def get_generate_program(
    inputs: set[Predicate], assumptions: str | None, aux: Auxiliaries, ground_terms: set[str]
) -> str:
    """
    Get the program to generate inputs.
    """
    # start constructing the program as a list of rules (represented as strings)
    prog = [f"#const {aux.size}=0.", f"{aux.domain}(0..{aux.size}-1)."]

    for term in ground_terms:
        prog.append(f"{aux.domain}({term}).")

    for pred in inputs:
        # add choice rule for the predicate
        if pred.arity == 0:
            prog.append(f"{{ {pred.name} }}.")
        else:
            # body restricts every variable to the domain (i.e. dom(X0), dom(X1), ...)
            body = ", ".join(f"{aux.domain}({var})" for var in variable_names(pred.arity))
            prog.append(f"{{ {atom_str(pred.name, pred.arity)} }} :- {body}.")

    # turn the list into a string
    prog_str = "\n".join(prog)

    if assumptions:
        prog_str += "\n" + assumptions

    log.debug("Generate program")
    log.debug(prog_str + "\n")  # pylint: disable=logging-not-lazy

    return prog_str


def get_difference_constraint(use_gc: bool, aux: Auxiliaries) -> str:
    """
    Get the difference constraint.
    """
    constraint = f":- {aux.diff}." if use_gc else f":- not {aux.diff}."

    log.debug("Difference constraint")
    log.debug(constraint + "\n")  # pylint: disable=logging-not-lazy

    return constraint


def get_difference_program(outputs: set[Predicate], aux: Auxiliaries) -> str:
    """
    Get the program to detect differences in outputs.
    """
    # construct the program as a list of rules (strings)
    prog = []

    for pred in outputs:
        # atom of the predicate and its auxiliary (suffixed) version
        original = atom_str(pred.name, pred.arity)
        auxiliary = atom_str(f"{pred.name}{aux.suffix}", pred.arity)

        # add difference rules
        prog.append(f"{aux.diff} :- {original}, not {auxiliary}.")
        prog.append(f"{aux.diff} :- not {original}, {auxiliary}.")

    # detect the unsat predicate as a difference
    # also add a defined statement for unsat to avoid warnings
    prog.append(f"#defined {aux.unsat}/0.")
    prog.append(f"{aux.diff} :- {aux.unsat}.")

    # represent the program as a string
    prog_str = "\n".join(prog)

    log.debug("Difference program")
    log.debug(prog_str + "\n")  # pylint: disable=logging-not-lazy

    return prog_str
