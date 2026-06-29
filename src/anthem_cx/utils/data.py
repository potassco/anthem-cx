"""
Utility data structures.
"""

from dataclasses import dataclass, fields, replace
from enum import Enum, auto

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


class UniquenessCheck(Enum):
    """
    The uniqueness check selected on the command line.

    The decision on whether to use guess-and-check is stored separately in UniquenessVerdict.
    """

    SKIP = auto()  # assume uniqueness, solve directly
    FAIL = auto()  # assume non-uniqueness, force guess and check
    AUTO = auto()  # stratification, then local
    STRATIFICATION = auto()  # stratification only
    LOCAL = auto()  # local only

    @classmethod
    def from_string(cls, value: str) -> "UniquenessCheck":
        """Create a UniquenessCheck object from a string."""
        match value:
            case "skip":
                return cls.SKIP
            case "fail":
                return cls.FAIL
            case "auto":
                return cls.AUTO
            case "stratification":
                return cls.STRATIFICATION
            case "local":
                return cls.LOCAL
            case _:
                raise ValueError(f"Invalid uniqueness check value: {value}")


class UniquenessVerdict(Enum):
    """
    The outcome of the uniqueness analysis.
    """

    DIRECT = auto()  # solve directly, no further checks
    GUESS_CHECK = auto()  # use the guess and check approach
    NEEDS_LOCAL_CHECK = auto()  # solve directly; if a potential counterexample is found, run the local check

    def uses_gc(self) -> bool:
        """Check whether the verdict requires the guess and check approach."""
        return self is UniquenessVerdict.GUESS_CHECK


@dataclass(frozen=True)
class Predicate:
    """
    Dataclass representing a predicate by its name and arity.
    """

    name: str
    arity: int

    def __str__(self) -> str:
        """Return the name/arity notation as a string."""
        return f"{self.name}/{self.arity}"


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

    def replace(self, **kwargs: str) -> "Auxiliaries":
        """
        Get an Auxiliaries object with certain values replaced.

        The arguments specify which key to replace by what value.
        """
        return replace(self, **kwargs)

    def replace_values(self, replacements: dict[Predicate, Predicate]) -> "Auxiliaries":
        """
        Get an Auxiliaries object with certain values replaced.

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


@dataclass(frozen=True)
class Options:  # pylint: disable=too-many-instance-attributes
    """
    Dataclass storing the options of the counterexample problem.
    """

    direction: Direction
    out_dir: str | None
    solve: bool
    start: int
    max_size: int | None
    uniqueness: UniquenessCheck
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
    is_forward: bool
    input: list[str]
    output: list[str]

    @property
    def direction(self) -> str:
        """The direction label of the counterexample ('forward' or 'backward')."""
        return "forward" if self.is_forward else "backward"

    def __str__(self) -> str:
        """Obtain a string representation of the counterexample."""
        rep = "  Input for the counterexample:\n"
        rep += "    " + ", ".join(self.input) + "\n"
        rep += f"  External behavior of {'left' if self.is_forward else 'right'}:\n"
        rep += "    " + ", ".join(self.output)

        return rep

    @classmethod
    def from_model(
        cls, is_forward: bool, inputs: set[Predicate], outputs: set[Predicate], model: Model
    ) -> "Counterexample":
        """
        Create a Counterexample object from a model.

        The size is the number of distinct constants actually used in the input atoms, which may
        differ from the domain size parameter used while solving (e.g. when constants occurring in
        the programs are added to the domain or when not all domain elements are used).
        """
        symbols = model.symbols(atoms=True)
        input_atoms = []
        output_atoms = []
        input_constants = set()

        for symbol in symbols:
            pred = Predicate(symbol.name, len(symbol.arguments))

            if pred in inputs:
                input_atoms.append(str(symbol))
                input_constants.update(symbol.arguments)

            if pred in outputs:
                output_atoms.append(str(symbol))

        return Counterexample(len(input_constants), is_forward, input_atoms, output_atoms)
