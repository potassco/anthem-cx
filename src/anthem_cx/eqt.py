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
    RejectDisjunctions,
    RemoveHeadCondition,
    ReplacePositiveOutputPredicates,
    TransformRuleHeads,
)
from .utils.data import Auxiliaries, Predicate
from .utils.logging import get_logger
from .utils.output import program_to_str
from .utils.transformation import apply_transformer

log = get_logger(__name__)


def normalize_program(prog: list[AST]) -> list[AST]:
    """
    Normalize a logic program.
    """
    for t in [
        RejectDisjunctions,
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
        log.debug("Program after applying %s", t.__name__)
        log.debug(program_to_str(prog, True))

    return prog


def _public_reduct(prog: list[AST], outputs: set[Predicate], auxiliaries: Auxiliaries) -> list[AST]:
    """
    Compute the public reduct of a program with respest to a set of output predicates.
    """
    for t in [ReplacePositiveOutputPredicates, TransformRuleHeads]:
        prog = apply_transformer(t(outputs, auxiliaries), prog)
        log.debug("Program after applying %s", t.__name__)
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
        # construct list of variables (i.e. X0, X1, ...) and body (i.e. dom(X0), dom(X1), ...)
        body = ""
        variables = ""
        for i in range(pred.arity):
            var = f"X{i}"
            if i > 0:
                body += ", "
                variables += ","
            body += f"{aux.domain}({var})"
            variables += var

        # add choice rule for the predicate
        if pred.arity == 0:
            prog.append(f"{{ {pred.name} }}.")
        else:
            prog.append(f"{{ {pred.name}({variables}) }} :- {body}.")

    # turn the list into a string
    prog_str = "\n".join(prog)

    if assumptions:
        prog_str += assumptions

    log.debug("Generate program")
    log.debug(prog_str + "\n")  # pylint: disable=logging-not-lazy

    return prog_str


def get_difference_program(outputs: set[Predicate], use_gc: bool, aux: Auxiliaries) -> str:
    """
    Get the program to detect differences in outputs.
    """
    # construct the program as a list of rules (strings)
    prog = []

    for pred in outputs:
        if pred.arity == 0:
            # add propositional difference rules
            prog.append(f"{aux.diff} :- {pred.name}, not {pred.name}{aux.suffix}.")
            prog.append(f"{aux.diff} :- not {pred.name}, {pred.name}{aux.suffix}.")
        else:
            # get a list of variables matching the arity of pred
            variables = ""
            for i in range(pred.arity):
                var = f"X{i}"
                if i > 0:
                    variables += ","
                variables += var

            # add difference rules with variables
            prog.append(f"{aux.diff} :- {pred.name}({variables}), not {pred.name}{aux.suffix}({variables}).")
            prog.append(f"{aux.diff} :- not {pred.name}({variables}), {pred.name}{aux.suffix}({variables}).")

    # detect the unsat predicate as a difference
    # also add a defined statement for unsat to avoid warnings
    prog.append(f"#defined {aux.unsat}/0.")
    prog.append(f"{aux.diff} :- {aux.unsat}.")

    # enforce a counterexample
    if not use_gc:
        prog.append(f":- not {aux.diff}.")
    else:
        prog.append(f":- {aux.diff}.")

    # represent the program as a string
    prog_str = "\n".join(prog)

    log.debug("Difference program")
    log.debug(prog_str + "\n")  # pylint: disable=logging-not-lazy

    return prog_str


def get_public_reduct(prog: list[AST], outputs: set[Predicate], auxiliaries: Auxiliaries) -> list[AST]:
    """
    Get the public reduct of the program in filename.
    """
    return _public_reduct(prog, outputs, auxiliaries)
