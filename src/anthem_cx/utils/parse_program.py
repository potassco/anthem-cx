"""
Module to parse a file into an AST.
"""

from clingo.ast import AST, parse_files

from .logging import get_logger
from .output import program_to_str

log = get_logger(__name__)


def parse_program(filename: str) -> list[AST]:
    """
    Parse a file into a list of ASTs.
    """
    prog: list[AST] = []
    parse_files([filename], prog.append)
    log.debug("Parsed program %s", filename)
    log.debug(program_to_str(prog, True))
    return prog
