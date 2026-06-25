"""
Output utilities.
"""

import os

from clingo.ast import AST

from .logging import get_logger

log = get_logger(__name__)


def variable_names(arity: int) -> list[str]:
    """
    Get the list of variable names X0, ..., X{arity-1} for the given arity.
    """
    return [f"X{i}" for i in range(arity)]


def atom_str(name: str, arity: int) -> str:
    """
    Get the string representation of an atom with the given predicate name and arity.

    For arity 0 this is just the name, otherwise it is name(X0,...,X{arity-1}).
    """
    if arity == 0:
        return name
    return f"{name}({','.join(variable_names(arity))})"


def save_cx_program_gc_to_file(
    cx_program_guess: str | None, cx_program_check: str | None, out_dir: str, forward: bool = True
) -> None:
    """
    Save the guess and check CX program to the output directory.
    """
    if cx_program_guess and cx_program_check:
        save_cx_program_to_file(cx_program_guess, out_dir, forward, postfix="_guess")
        save_cx_program_to_file(cx_program_check, out_dir, forward, postfix="_check")


def save_cx_program_to_file(
    cx_program: str | None, out_dir: str, forward: bool = True, postfix: str | None = None
) -> None:
    """
    Save the CX program to the output directory.
    """
    if cx_program:
        direction = "forward" if forward else "backward"
        os.makedirs(out_dir, exist_ok=True)
        outfile = os.path.join(out_dir, f"{direction}{postfix if postfix else ""}.lp")
        log.info("Writing %s program to %s", direction, outfile)
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(cx_program)


def program_to_str(prog: list[AST], newline: bool = False) -> str:
    """
    Turn a program into its string representation.
    """
    string = "\n".join(str(n) for n in prog)

    # optionally add a newline at the end
    if newline:
        string += "\n"

    return string


def build_cx_program(  # pylint: disable=too-many-positional-arguments
    generate: str, left: list[AST], public_reduct: list[AST], difference: str, constraint: str, forward: bool = True
) -> str:
    """
    Build the CX program as a string from the components.
    """
    cx_program = (
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        + f"% CX {'forward' if forward else 'backward'} program\n"
        + "% input generation\n"
        + generate
        + f"\n\n% {'left' if forward else 'right'} program\n"
        + program_to_str(left, True)
        + f"\n% public reduct of {'right' if forward else 'left'} program\n"
        + program_to_str(public_reduct, True)
        + "\n% difference detection\n"
        + difference
        + "\n% enforce counterexample\n"
        + constraint
    )

    return cx_program


def build_cx_program_gc(  # pylint: disable=too-many-positional-arguments
    generate: str, left: list[AST], public_reduct: list[AST], difference: str, constraint: str, forward: bool = True
) -> tuple[str, str]:
    """
    Build the guess and check CX program as a string for the components.
    """
    cx_program_guess = (
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        + f"% CX {'forward' if forward else 'backward'} program guess\n"
        + "% input generation\n"
        + generate
        + f"\n\n% {'left' if forward else 'right'} program\n"
        + program_to_str(left, True)
    )
    cx_program_check = (
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        + f"% CX {'forward' if forward else 'backward'} program check\n"
        + f"% public reduct of {'right' if forward else 'left'} program\n"
        + program_to_str(public_reduct, True)
        + "\n% difference detection\n"
        + difference
        + "\n% enforce counterexample\n"
        + constraint
    )

    return cx_program_guess, cx_program_check
