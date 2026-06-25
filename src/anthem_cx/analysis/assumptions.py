"""
Module for checking the optional assumption program.
"""

from clingo.ast import AST

from ..utils.data import Auxiliaries, Predicate
from ..utils.errors import AnthemCXError
from ..utils.logging import get_logger
from .conflict import _collect_privates, _get_replacements, _replace_predicates

log = get_logger(__name__)


def check_assumptions(  # pylint: disable=too-many-positional-arguments
    assumptions: list[AST],
    inputs: set[Predicate],
    outputs: set[Predicate],
    left: list[AST],
    right: list[AST],
    aux: Auxiliaries,
) -> list[AST]:
    """
    Check the assumption program and rename conflicting private predicates.

    The assumption program may only contain input predicates and (fresh) private predicates.
    Predicates that are not input or output are renamed if they conflict with any private
    predicates of left or right. In addition, the assumptions may use the auxiliary domain predicate.

    Raises an AnthemCXError (causing anthem-cx to exit) if an output predicate occurs in the
    assumption program. Returns the (possibly renamed) assumption program.
    """
    # the domain predicate is allowed
    allowed_publics = inputs | {Predicate(aux.domain, 1)}

    # reject output predicates occurring anywhere in the assumption program
    assumption_privates = _collect_privates(assumptions, allowed_publics)
    output_conflicts = assumption_privates & outputs
    if output_conflicts:
        predicates = ", ".join(str(p) for p in sorted(output_conflicts, key=str))
        raise AnthemCXError(f"output predicate(s) in the assumption program: {predicates}")

    # ensure the assumption privates are distinct from all predicates of the left/right programs
    # and the auxiliaries; rename conflicting ones
    taken = inputs | outputs | _collect_privates(left + right, inputs | outputs) | aux.predicates()
    conflicts = assumption_privates & taken
    if conflicts:
        for pred in conflicts:
            log.warning("found conflicting assumption predicate %s, applying renaming", pred)
        replacements, _ = _get_replacements(conflicts, taken | assumption_privates)
        assumptions = _replace_predicates(assumptions, replacements)

    return assumptions
