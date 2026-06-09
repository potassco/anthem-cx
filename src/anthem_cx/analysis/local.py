"""
Module to check local uniqueness.
"""

from clingo.ast import AST
from clingo.control import Control
from clingo.solving import Model

from ..utils.data import Counterexample
from ..utils.output import program_to_str


def is_locally_unique(prg: list[AST], counterexample: Counterexample) -> bool:
    """
    Check if a program is locally unique for a potential counterexample.

    Test if prg has exactly one stable model under the addition of the facts given by
    the input and output of the counterexample. The program is assumed to have at least
    one stable model, otherwise an error is raised.
    """
    # extract input and output from the counterexample and add them as facts
    facts = "\n".join(f"{atom}." for atom in counterexample.input + counterexample.output)
    program = program_to_str(prg, newline=True) + facts

    # enumerating two stable models is enough to decide local uniqueness
    ctl = Control(["-n", "2"])
    ctl.add(program)
    ctl.ground()

    model_count = 0

    def on_model(_: Model) -> None:
        nonlocal model_count
        model_count += 1

    ctl.solve(on_model=on_model)

    # the program is assumed to have at least one stable model
    if model_count == 0:
        raise ValueError("The program has no stable model under the given counterexample")

    # locally unique exactly when there is a single stable model
    return model_count == 1
