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


def save_eqt_gc_to_file(eqt_guess: str | None, eqt_check: str | None, out_dir: str, forward: bool = True) -> None:
    """
    Save the guess and check EQT program to the output directory.
    """
    if eqt_guess and eqt_check:
        save_eqt_to_file(eqt_guess, out_dir, forward, postfix="_guess")
        save_eqt_to_file(eqt_check, out_dir, forward, postfix="_check")


def save_eqt_to_file(eqt: str | None, out_dir: str, forward: bool = True, postfix: str | None = None) -> None:
    """
    Save the EQT program to the output directory.
    """
    if eqt:
        direction = "forward" if forward else "backward"
        os.makedirs(out_dir, exist_ok=True)
        outfile = os.path.join(out_dir, f"{direction}{postfix if postfix else ""}.lp")
        log.info("Writing %s program to %s", direction, outfile)
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(eqt)


def program_to_str(prog: list[AST], newline: bool = False) -> str:
    """
    Turn a program into its string representation.
    """
    string = "\n".join(str(n) for n in prog)

    # optionally add a newline at the end
    if newline:
        string += "\n"

    return string


def build_eqt(  # pylint: disable=too-many-positional-arguments
    generate: str, left: list[AST], public_reduct: list[AST], difference: str, constraint: str, forward: bool = True
) -> str:
    """
    Build the EQT program as a string from the components.
    """
    eqt = (
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        + f"% EQT {'forward' if forward else 'backward'}\n"
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

    return eqt


def build_eqt_gc(  # pylint: disable=too-many-positional-arguments
    generate: str, left: list[AST], public_reduct: list[AST], difference: str, constraint: str, forward: bool = True
) -> tuple[str, str]:
    """
    Build the guess and check EQT program as a string for the components.
    """
    eqt_guess = (
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        + f"% EQT {'forward' if forward else 'backward'} guess\n"
        + "% input generation\n"
        + generate
        + f"\n\n% {'left' if forward else 'right'} program\n"
        + program_to_str(left, True)
    )
    eqt_check = (
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        + f"% EQT {'forward' if forward else 'backward'} check\n"
        + f"% public reduct of {'right' if forward else 'left'} program\n"
        + program_to_str(public_reduct, True)
        + "\n% difference detection\n"
        + difference
        + "\n% enforce counterexample\n"
        + constraint
    )

    return eqt_guess, eqt_check
