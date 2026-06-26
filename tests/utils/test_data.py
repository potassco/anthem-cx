"""
Tests for utils/data.py: Direction, UniquenessCheck, UniquenessVerdict, Auxiliaries, Predicate.
"""

from unittest import TestCase

from clingo.control import Control

from anthem_cx.utils.data import (
    Auxiliaries,
    Counterexample,
    Direction,
    Predicate,
    UniquenessCheck,
    UniquenessVerdict,
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

    def test_uniqueness_check_parsing(self) -> None:
        """Tests for the UniquenessCheck enum parsing."""
        for string, expected in [
            ("skip", UniquenessCheck.SKIP),
            ("fail", UniquenessCheck.FAIL),
            ("auto", UniquenessCheck.AUTO),
            ("stratification", UniquenessCheck.STRATIFICATION),
            ("local", UniquenessCheck.LOCAL),
        ]:
            self.assertEqual(UniquenessCheck.from_string(string), expected)

        with self.assertRaises(ValueError):
            UniquenessCheck.from_string("test")

    def test_uniqueness_verdict_uses_gc(self) -> None:
        """uses_gc is true only for the guess and check verdict."""
        for verdict, expected in [
            (UniquenessVerdict.DIRECT, False),
            (UniquenessVerdict.GUESS_CHECK, True),
            (UniquenessVerdict.NEEDS_LOCAL_CHECK, False),
        ]:
            self.assertEqual(verdict.uses_gc(), expected)

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
        ctl.add("a. b(1). c(2,3). d(3,4).")
        ctl.ground()

        # inputs include a propositional atom and atoms sharing the constant 3,
        # so the distinct input constants are {2, 3, 4} -> size 3
        inputs = {Predicate("a", 0), Predicate("c", 2), Predicate("d", 2)}
        outputs = {Predicate("b", 1)}
        counterexample: Counterexample | None = None

        def build_counterexample(model: object) -> None:
            nonlocal counterexample
            counterexample = Counterexample.from_model(True, inputs, outputs, model)  # type: ignore[arg-type]

        ctl.solve(on_model=build_counterexample)
        assert counterexample is not None
        self.assertEqual(counterexample.size, 3)
        self.assertTrue(counterexample.is_forward)
        self.assertEqual(counterexample.direction, "forward")
        self.assertEqual(sorted(counterexample.input), ["a", "c(2,3)", "d(3,4)"])
        self.assertEqual(counterexample.output, ["b(1)"])

        # __str__ reports the input and the external behavior of the relevant program
        rep = str(Counterexample(1, True, ["a"], ["b(1)"]))
        self.assertEqual("  Input for the counterexample:\n    a\n  External behavior of left:\n    b(1)", rep)

        # the backward direction reports the right program's behavior
        self.assertIn("right", str(Counterexample(1, False, [], [])))
