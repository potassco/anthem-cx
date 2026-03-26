"""
Module for parsing user guides.
"""

import re

from . import Predicate
from .logging import get_logger

log = get_logger(__name__)

SYMBOL_PATTERN = r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)"
ARITY_PATTERN = r"(?P<arity>[0-9]+)"

INPUT_OUTPUT_RE = re.compile(rf"^(input|output)\s*:\s*{SYMBOL_PATTERN}\s*/\s*{ARITY_PATTERN}$")

PLACEHOLDER_RE = re.compile(rf"^input\s*:\s*{SYMBOL_PATTERN}\s*->")

ASSUMPTION_RE = re.compile(r"^assumption\s*:")


def _split_entries(text: str) -> list[str]:
    """
    Split a user guide into its entries.
    """
    return [e.strip() for e in text.split(".") if e.strip()]


def parse_user_guide(filename: str) -> tuple[set[Predicate], set[Predicate]]:
    """
    Parse a user guide into sets of input and output predicates.
    """
    with open(filename, "r", encoding="utf-8") as f:
        text = f.read()

    input_preds = set()
    output_preds = set()

    for raw in _split_entries(text):
        # normalize whitespace
        entry = " ".join(raw.split())

        m = INPUT_OUTPUT_RE.match(entry)
        if m:
            pred = Predicate(name=m.group("name"), arity=int(m.group("arity")))
            if m.group(1) == "input":
                input_preds.add(pred)
                log.debug("Adding input predicate %s", pred)
            else:
                output_preds.add(pred)
                log.debug("Adding output predicate %s", pred)

            continue

        if ASSUMPTION_RE.match(entry):
            log.warning(
                (
                    "Assumptions in the user guide are not supported: %s."
                    " Consider using the option --assumptions to pass an assumption program."
                ),
                entry,
            )
            continue

        if PLACEHOLDER_RE.match(entry):
            log.warning("Placeholders are currently not supported: %s.", entry)
            continue

        log.warning("Unrecognized user guide entry: %s.", entry)

    return input_preds, output_preds
