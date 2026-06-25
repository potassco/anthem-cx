"""
Module to solve counterexample programs.
"""

from tempfile import NamedTemporaryFile

from clingo.control import Control
from clingo.solving import Model
from guess_and_check import solve_guess_and_check

from .data import Counterexample, Predicate
from .logging import get_logger

log = get_logger(__name__)


def _solve_with_size(  # pylint: disable=too-many-positional-arguments
    eqt: str,
    is_forward: bool,
    size: int,
    inputs: set[Predicate],
    outputs: set[Predicate],
    clingo_args: list[str],
    size_placeholder: str,
) -> Counterexample | None:
    """
    Solve an EQT program with the given domain size and return a counterexample if one is found.
    """
    ctl = Control(["-c", f"{size_placeholder}={size}"] + clingo_args)
    ctl.add(eqt)
    ctl.ground()

    counterexample: Counterexample | None = None

    def on_model(model: Model) -> None:
        nonlocal counterexample
        counterexample = Counterexample.from_model(is_forward, size, inputs, outputs, model)

    ctl.solve(on_model=on_model)

    return counterexample


def solve_for_counterexample(  # pylint: disable=too-many-positional-arguments
    eqt_forward: str | None,
    eqt_backward: str | None,
    inputs: set[Predicate],
    outputs: set[Predicate],
    domain_start: int,
    domain_max: int | None,
    clingo_args: list[str],
    size_placeholder: str,
) -> Counterexample | None:
    """
    Solve the given EQT programs for counterexamples by increasing the domain size from start to max.

    Returns the counterexample if one is found, otherwise None.
    """
    log.debug("solving programs with starting size %s and maximum size %s", domain_start, domain_max)
    log.debug("forward program:\n%s", eqt_forward)
    log.debug("backward program:\n%s", eqt_backward)

    domain_size = domain_start
    while True:
        # stop if the domain size is larger than the limit
        if domain_max is not None and domain_size > domain_max:
            return None

        log.info("Solving for counterexample of domain size %s", domain_size)

        if eqt_forward:
            counterexample = _solve_with_size(
                eqt_forward, True, domain_size, inputs, outputs, clingo_args, size_placeholder
            )
            if counterexample:
                return counterexample

        if eqt_backward:
            counterexample = _solve_with_size(
                eqt_backward, False, domain_size, inputs, outputs, clingo_args, size_placeholder
            )
            if counterexample:
                return counterexample

        domain_size += 1


def _solve_gc_with_size(  # pylint: disable=too-many-positional-arguments
    guess: str,
    check: str,
    is_forward: bool,
    size: int,
    inputs: set[Predicate],
    outputs: set[Predicate],
    clingo_args: list[str],
    size_placeholder: str,
) -> Counterexample | None:
    """
    Solve a guess and check EQT program with the given domain size and return a counterexample if one is found.
    """
    with (
        NamedTemporaryFile(mode="w", delete=False) as guess_file,
        NamedTemporaryFile(mode="w", delete=False) as check_file,
    ):
        guess_file.write(guess)
        check_file.write(check)

    counterexample: Counterexample | None = None

    def on_model(model: Model) -> None:
        nonlocal counterexample
        counterexample = Counterexample.from_model(is_forward, size, inputs, outputs, model)

    solve_guess_and_check(
        ["-c", f"{size_placeholder}={size}"] + clingo_args,
        False,
        False,
        [guess_file.name],
        [check_file.name],
        on_model=on_model,
    )

    return counterexample


def _get_holds(predicates: set[Predicate], undo: bool = False) -> str:
    """
    Get a program mapping all predicates into holds/1, or undoing this mapping.
    """
    prog = ["#defined holds/1."]

    for pred in predicates:
        variables = ""
        for i in range(pred.arity):
            if i > 0:
                variables += ","
            variables += f"X{i}"
        if not undo:
            if pred.arity == 0:
                prog.append(f"holds({pred.name}) :- {pred.name}.")
            else:
                prog.append(f"holds({pred.name}({variables})) :- {pred.name}({variables}).")
        else:
            if pred.arity == 0:
                prog.append(f"{pred.name} :- holds({pred.name}).")
            else:
                prog.append(f"{pred.name}({variables}) :- holds({pred.name}({variables})).")

    prog_str = "\n".join(prog)

    return prog_str


def solve_gc_for_counterexample(  # pylint: disable=too-many-positional-arguments
    forward_guess: str | None,
    forward_check: str | None,
    backward_guess: str | None,
    backward_check: str | None,
    inputs: set[Predicate],
    outputs: set[Predicate],
    domain_start: int,
    domain_max: int | None,
    clingo_args: list[str],
    size_placeholder: str,
) -> Counterexample | None:
    """
    Solve the given guess and check EQT programs for counterexamples by increasing the domain size from start to max.

    Returns the counterexample if one is found, otherwise None.
    """
    log.debug("solving programs with starting size %s and maximum size %s", domain_start, domain_max)
    log.debug("forward program:\n%s\n%s", forward_guess, forward_check)
    log.debug("backward program:\n%s\n%s", backward_guess, backward_check)

    holds = _get_holds(inputs | outputs)
    undo_holds = _get_holds(inputs | outputs, undo=True)

    if forward_guess:
        forward_guess += holds
    if forward_check:
        forward_check += undo_holds
    if backward_guess:
        backward_guess += holds
    if backward_check:
        backward_check += undo_holds

    domain_size = domain_start
    while True:
        # stop if the domain size is larger than the limit
        if domain_max is not None and domain_size > domain_max:
            return None

        log.info("Solving for counterexample of domain size %s", domain_size)

        if forward_guess and forward_check:
            counterexample = _solve_gc_with_size(
                forward_guess,
                forward_check,
                True,
                domain_size,
                inputs,
                outputs,
                clingo_args,
                size_placeholder,
            )
            if counterexample:
                return counterexample

        if backward_guess and backward_check:
            counterexample = _solve_gc_with_size(
                backward_guess,
                backward_check,
                False,
                domain_size,
                inputs,
                outputs,
                clingo_args,
                size_placeholder,
            )
            if counterexample:
                return counterexample

        domain_size += 1
