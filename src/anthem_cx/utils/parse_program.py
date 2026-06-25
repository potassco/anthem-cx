"""
Module to parse a file into an AST.
"""

from clingo.ast import AST, parse_files

from .errors import AnthemCXError
from .logging import get_logger
from .output import program_to_str

log = get_logger(__name__)


def parse_program(filename: str) -> list[AST]:
    """
    Parse a file into a list of ASTs.
    """
    prog: list[AST] = []
    # clingo prints the underlying detail (missing file, syntax error, ...) to
    # stderr and raises a RuntimeError; turn it into a clean user-facing error
    try:
        parse_files([filename], prog.append)
    except RuntimeError as e:
        raise AnthemCXError(f"could not parse program '{filename}': {e}") from e
    log.debug("Parsed program %s", filename)
    log.debug(program_to_str(prog, True))
    return prog
