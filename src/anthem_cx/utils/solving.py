"""
Module to solve counterexample programs.
"""

from tempfile import NamedTemporaryFile

from clingo.control import Control
from clingo.solving import Model
from clingo.symbol import Symbol
from guess_and_check import solve_guess_and_check

from . import Predicate
from .logging import get_logger

log = get_logger(__name__)


def _symbol_to_predicate(symbol: Symbol) -> Predicate:
    return Predicate(symbol.name, len(symbol.arguments))


def _on_model(direction: str, size: int, inputs: set[Predicate], outputs: set[Predicate], model: Model) -> None:
    print(f"Found a counterexample of size {size} in the {direction} direction")
    symbols = model.symbols(atoms=True)
    counterexample_input = []
    stable_model = []

    for symbol in symbols:
        pred = _symbol_to_predicate(symbol)

        if pred in inputs:
            counterexample_input.append(str(symbol))

        if pred in outputs:
            stable_model.append(str(symbol))

    print("  Input for the counterexample:")
    print("    " + ", ".join(counterexample_input))

    print(f"  External behavior of {'left' if direction == 'forward' else 'right'}:")
    print("    " + ", ".join(stable_model))


def _solve_with_size(  # pylint: disable=too-many-positional-arguments
    eqt: str,
    direction: str,
    size: int,
    inputs: set[Predicate],
    outputs: set[Predicate],
    clingo_args: list[str],
    size_placeholder: str,
) -> bool:
    """
    Solve an EQT program with the given domain size and return whether a counterexample was found.
    """
    ctl = Control(["-c", f"{size_placeholder}={size}"] + clingo_args)
    ctl.add(eqt)
    ctl.ground()
    ret = ctl.solve(on_model=lambda m: _on_model(direction, size, inputs, outputs, m))

    return bool(ret.satisfiable)


def solve_for_counterexample(  # pylint: disable=too-many-positional-arguments
    eqt_forward: str | None,
    eqt_backward: str | None,
    inputs: set[Predicate],
    outputs: set[Predicate],
    domain_start: int,
    domain_max: int | None,
    clingo_args: list[str],
    size_placeholder: str,
) -> None:
    """
    Solve the given EQT programs for counterexamples by increasing the domain size from start to max.
    """
    log.info("solving programs with starting size %s and maximum size %s", domain_start, domain_max)
    log.info("forward program:\n%s", eqt_forward)
    log.info("backward program:\n%s", eqt_backward)

    domain_size = domain_start
    while True:
        # stop if the domain size is larger than the limit
        if domain_max is not None and domain_size > domain_max:
            print(f"No counterexample was found for the domain size max of {domain_max}")
            break

        print(f"Solving for counterexample of domain size {domain_size}")

        if eqt_forward:
            if _solve_with_size(eqt_forward, "forward", domain_size, inputs, outputs, clingo_args, size_placeholder):
                break

        if eqt_backward:
            if _solve_with_size(eqt_backward, "backward", domain_size, inputs, outputs, clingo_args, size_placeholder):
                break

        domain_size += 1


def _solve_gc_with_size(  # pylint: disable=too-many-positional-arguments
    guess: str,
    check: str,
    direction: str,
    size: int,
    inputs: set[Predicate],
    outputs: set[Predicate],
    clingo_args: list[str],
    size_placeholder: str,
) -> bool:
    with (
        NamedTemporaryFile(mode="w", delete=False) as guess_file,
        NamedTemporaryFile(mode="w", delete=False) as check_file,
    ):
        guess_file.write(guess)
        check_file.write(check)

    return solve_guess_and_check(  # type: ignore[no-any-return]
        ["-c", f"{size_placeholder}={size}"] + clingo_args,
        False,
        False,
        [guess_file.name],
        [check_file.name],
        on_model=lambda m: _on_model(direction, size, inputs, outputs, m),
    )


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
) -> None:
    """
    Solve the given guess and check EQT programs for counterexamples by increasing the domain size from start to max.
    """
    log.info("solving programs with starting size %s and maximum size %s", domain_start, domain_max)
    log.info("forward program:\n%s\n%s", forward_guess, forward_check)
    log.info("backward program:\n%s\n%s", backward_guess, forward_check)

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
            print(f"No counterexample was found for the domain size max of {domain_max}")
            break

        print(f"Solving for counterexample of domain size {domain_size}")

        if forward_guess and forward_check:
            if _solve_gc_with_size(
                forward_guess, forward_check, "forward", domain_size, inputs, outputs, clingo_args, size_placeholder
            ):
                break

        if backward_guess and backward_check:
            if _solve_gc_with_size(
                backward_guess, backward_check, "backward", domain_size, inputs, outputs, clingo_args, size_placeholder
            ):
                break

        domain_size += 1
