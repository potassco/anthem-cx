"""
Utility data structures.
"""

from dataclasses import dataclass, fields, replace
from enum import Enum, auto
from typing import Any

from clingo.ast import AST
from clingo.solving import Model

PREDICATE_SUFFIX = "__"
UNSAT_PREDICATE = "__bot"
DIFF_PREDICATE = "__diff"
DOMAIN_PREDICATE = "__dom"
SIZE_PLACEHOLDER = "__domain_size"


@dataclass
class Programs:
    """
    Dataclass storing the program parts of the counterexample program.
    """

    left: list[AST]
    right: list[AST]
    generate: str
    difference: str
    constraint: str
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


@dataclass
class UniquenessData:
    """
    Dataclass storing info about uniqueness and uniqueness checks

    use_gc determines whether GC should be used (bool) or if checks need to be run (None).
    The use of which checks is determined by use_syntax and use_local.
    """

    use_gc: bool | None
    use_syntax: bool
    use_local: bool

    @classmethod
    def from_string(cls, value: str) -> "UniquenessData":
        """Create a UniquenessData object from a string."""
        match value:
            case "skip":
                return cls(False, False, False)
            case "fail":
                return cls(True, False, False)
            case "auto":
                return cls(None, True, True)
            case "stratification":
                return cls(None, True, False)
            case "local":
                return cls(None, False, True)
            case _:
                raise ValueError(f"Invalid uniqueness data value: {value}")

    def success(self) -> None:
        """Update data after successful check."""
        self.use_gc = False

    def syntax_failure(self) -> None:
        """Update data after failed syntactic check."""
        # failure of syntax check only relevant if we do not use the local check
        if not self.use_local:
            self.use_gc = True

    def local_condition_failure(self) -> None:
        """Update data after failed check for local precondition (no odd cycles)."""
        self.use_gc = True
        self.use_local = False

    def local_failure(self) -> None:
        """Update data after failed local check."""
        self.use_gc = True


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
    gc: UniquenessData
    inputs: set[Predicate]
    outputs: set[Predicate]
    clingo_args: list[str]
    auxiliaries: Auxiliaries


@dataclass
class Counterexample:
    """
    Dataclass representing counterexamples.
    """

    size: int
    direction: str
    input: list[str]
    output: list[str]

    def __str__(self) -> str:
        """Obtain a string representation of the counterexample."""
        rep = "  Input for the counterexample:\n"
        rep += "    " + ", ".join(self.input) + "\n"
        rep += f"  External behavior of {'left' if self.direction == 'forward' else 'right'}:\n"
        rep += "    " + ", ".join(self.output)

        return rep

    @classmethod
    def from_model(  # pylint: disable=too-many-positional-arguments
        cls, direction: str, size: int, inputs: set[Predicate], outputs: set[Predicate], model: Model
    ) -> "Counterexample":
        """Create a Counterexample object from a model."""
        symbols = model.symbols(atoms=True)
        input_atoms = []
        output_atoms = []

        for symbol in symbols:
            pred = Predicate(symbol.name, len(symbol.arguments))

            if pred in inputs:
                input_atoms.append(str(symbol))

            if pred in outputs:
                output_atoms.append(str(symbol))

        return Counterexample(size, direction, input_atoms, output_atoms)
