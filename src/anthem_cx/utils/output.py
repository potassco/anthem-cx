"""
Output utilities.
"""

import os

from clingo.ast import AST

from .logging import get_logger

log = get_logger(__name__)


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
        outfile = os.path.join(out_dir, f"{direction}{postfix}.lp")
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
