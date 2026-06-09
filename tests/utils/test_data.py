"""
Tests for utils/data.py: Direction, UniquenessData, Auxiliaries, Predicate.
"""

from unittest import TestCase

from clingo.control import Control

from anthem_cx.utils.data import (
    Auxiliaries,
    Counterexample,
    Direction,
    Predicate,
    UniquenessData,
)


class TestDataUtils(TestCase):
    """Tests for data utils."""

    def test_predicate(self) -> None:
        """Tests for the Predicate dataclass."""
        for pred, expected in [
            (Predicate("p", 2), "p/2"),
            (Predicate("q", 0), "q/0"),
        ]:
            self.assertEqual(str(pred), expected)

    def test_direction_parsing(self) -> None:
        """Tests for the Direction enum parsing."""
        for string, direction in [
            ("universal", Direction.UNIVERSAL),
            ("forward", Direction.FORWARD),
            ("backward", Direction.BACKWARD),
        ]:
            self.assertEqual(Direction.from_string(string), direction)

        with self.assertRaises(ValueError):
            Direction.from_string("test")

    def test_direction_functions(self) -> None:
        """Tests for the Direction enum functions."""
        for direction, forward, backward in [
            (Direction.UNIVERSAL, True, True),
            (Direction.FORWARD, True, False),
            (Direction.BACKWARD, False, True),
        ]:
            self.assertEqual(direction.includes_forward(), forward)
            self.assertEqual(direction.includes_backward(), backward)

    def test_uniqueness_data_parsing(self) -> None:
        """Tests for the UniquenessData dataclass parsing."""
        for string, expected in [
            ("skip", UniquenessData(False, False, False)),
            ("fail", UniquenessData(True, False, False)),
            ("auto", UniquenessData(None, True, True)),
            ("stratification", UniquenessData(None, True, False)),
            ("local", UniquenessData(None, False, True)),
        ]:
            self.assertEqual(UniquenessData.from_string(string), expected)

        with self.assertRaises(ValueError):
            UniquenessData.from_string("test")

    def test_uniqueness_data_functions(self) -> None:
        """Tests for the UniquenessData dataclass functions, which mutate the object in place."""
        for data, update, expected in [
            (UniquenessData(None, True, True), UniquenessData.success, UniquenessData(False, True, True)),
            # a syntax failure does not change the data if the local check is still used
            (UniquenessData(None, True, True), UniquenessData.syntax_failure, UniquenessData(None, True, True)),
            (UniquenessData(None, True, False), UniquenessData.syntax_failure, UniquenessData(True, True, False)),
            (UniquenessData(None, True, True), UniquenessData.local_failure, UniquenessData(True, True, True)),
            (
                UniquenessData(None, True, True),
                UniquenessData.local_condition_failure,
                UniquenessData(True, True, False),
            ),
        ]:
            update(data)
            self.assertEqual(data, expected)

    def test_auxiliaries(self) -> None:
        """Tests for the Auxiliaries dataclass."""
        # default
        aux = Auxiliaries.default()
        for val, expected in [
            (aux.unsat, "__bot"),
            (aux.diff, "__diff"),
            (aux.domain, "__dom"),
            (aux.size, "__domain_size"),
            (aux.suffix, "__"),
        ]:
            self.assertEqual(val, expected)

        new_aux = aux.replace(unsat="my_bot")
        for val, expected in [
            (new_aux.unsat, "my_bot"),
            (new_aux.diff, "__diff"),
            (new_aux.domain, "__dom"),
            (new_aux.size, "__domain_size"),
            (new_aux.suffix, "__"),
        ]:
            self.assertEqual(val, expected)

        new_aux = aux.replace_values({Predicate("__dom", 0): Predicate("domain", 0)})
        for val, expected in [
            (new_aux.unsat, "__bot"),
            (new_aux.diff, "__diff"),
            (new_aux.domain, "domain"),
            (new_aux.size, "__domain_size"),
            (new_aux.suffix, "__"),
        ]:
            self.assertEqual(val, expected)

        new_aux = aux.replace_values({Predicate("p", 1): Predicate("q", 1)})
        self.assertEqual(new_aux, aux)

        preds = aux.predicates()
        self.assertEqual(preds, {Predicate("__bot", 0), Predicate("__diff", 0), Predicate("__dom", 1)})

    def test_counterexample_from_model(self) -> None:
        """from_model collects input and output atoms from the model and __str__ reports them."""
        ctl = Control()
        ctl.add("a. b(1). c(2,3).")
        ctl.ground()

        inputs = {Predicate("a", 0)}
        outputs = {Predicate("b", 1)}
        counterexample: Counterexample | None = None

        def build_counterexample(model: object) -> None:
            nonlocal counterexample
            counterexample = Counterexample.from_model("forward", 2, inputs, outputs, model)  # type: ignore[arg-type]

        ctl.solve(on_model=build_counterexample)
        assert counterexample is not None
        self.assertEqual(counterexample.size, 2)
        self.assertEqual(counterexample.direction, "forward")
        self.assertEqual(counterexample.input, ["a"])
        self.assertEqual(counterexample.output, ["b(1)"])

        rep = str(counterexample)
        self.assertIn("Found a counterexample of size 2 in the forward direction", rep)
        self.assertIn("a", rep)
        self.assertIn("b(1)", rep)
        self.assertIn("left", rep)

        # the backward direction reports the right program's behavior
        self.assertIn("right", str(Counterexample(1, "backward", [], [])))
