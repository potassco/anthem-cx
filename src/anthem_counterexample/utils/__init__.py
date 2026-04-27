"""
Utilities.
"""

from dataclasses import dataclass, fields, replace
from enum import Enum, auto
from typing import Any

from clingo.ast import AST

from .output import program_to_str

PREDICATE_SUFFIX = "__"
UNSAT_PREDICATE = "__bot"
DIFF_PREDICATE = "__diff"
DOMAIN_PREDICATE = "__dom"
SIZE_PLACEHOLDER = "__domain_size"


def build_eqt(generate: str, left: list[AST], public_reduct: list[AST], difference: str, forward: bool = True) -> str:
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
    )

    return eqt


def build_eqt_gc(
    generate: str, left: list[AST], public_reduct: list[AST], difference: str, forward: bool = True
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
    )

    return eqt_guess, eqt_check


@dataclass
class Programs:
    """
    Dataclass storing the program parts of the counterexample program.
    """

    left: list[AST]
    right: list[AST]
    generate: str
    difference: str
    public_reduct_left: list[AST] | None
    public_reduct_right: list[AST] | None


class Direction(Enum):
    """
    Enum representing directions of an equivalence problem.
    """

    UNIVERSAL = auto()
    FORWARD = auto()
    BACKWARD = auto()

    def includes_forward(self) -> bool:
        """Check if the direction includes forward."""
        return self in (Direction.UNIVERSAL, Direction.FORWARD)

    def includes_backward(self) -> bool:
        """Check if the direction includes backward."""
        return self in (Direction.UNIVERSAL, Direction.BACKWARD)

    @classmethod
    def from_string(cls, value: str) -> "Direction":
        """Create a Direction object from a string."""
        match value:
            case "universal":
                return cls.UNIVERSAL
            case "forward":
                return cls.FORWARD
            case "backward":
                return cls.BACKWARD
            case _:
                raise ValueError(f"Invalid direction: {value}")


@dataclass(frozen=True)
class Predicate:
    """
    Dataclass representing a predicate by its name and arity.
    """

    name: str
    arity: int

    def __str__(self) -> str:
        """Returns a string with the name/arity notation."""
        return f"{self.name}/{str(self.arity)}"


@dataclass(frozen=True)
class Auxiliaries:
    """
    Dataclass storing the names of auxiliary predicates, the size placeholder, and the predicate suffix.
    """

    unsat: str
    diff: str
    domain: str
    size: str
    suffix: str

    @classmethod
    def default(cls) -> "Auxiliaries":
        """Get a default Auxiliaries object."""
        return cls(
            unsat=UNSAT_PREDICATE,
            diff=DIFF_PREDICATE,
            domain=DOMAIN_PREDICATE,
            size=SIZE_PLACEHOLDER,
            suffix=PREDICATE_SUFFIX,
        )

    def replace(self, **kwargs: Any) -> "Auxiliaries":
        """
        Get a Auxiliaries object with certain values replaced.

        The arguments specify which key to replace by what value.
        """
        return replace(self, **kwargs)

    def replace_values(self, replacements: dict[Predicate, Predicate]) -> "Auxiliaries":
        """
        Get a Auxiliaries objects with certain values replaced.

        Argument is a dictionary mapping values to new values.
        """
        str_replacements = {}
        for pred in replacements:
            str_replacements[pred.name] = replacements[pred].name
        updates = {
            f.name: str_replacements[getattr(self, f.name)]
            for f in fields(self)
            if getattr(self, f.name) in str_replacements
        }
        return self.replace(**updates)

    def predicates(self) -> set[Predicate]:
        """Get all auxiliary predicates."""
        preds = {
            Predicate(self.unsat, 0),
            Predicate(self.diff, 0),
            Predicate(self.domain, 1),
        }
        return preds


@dataclass
class Options:  # pylint: disable=too-many-instance-attributes
    """
    Dataclass storing the options of the counterexample problem.
    """

    direction: Direction
    out_dir: str | None
    solve: bool
    start: int
    max_size: int | None
    use_gc: bool
    inputs: set[Predicate]
    outputs: set[Predicate]
    clingo_args: list[str]
    auxiliaries: Auxiliaries
