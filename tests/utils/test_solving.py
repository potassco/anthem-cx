"""
Tests for utils/solving.py.
"""

from unittest import TestCase
from unittest.mock import patch

from anthem_cx.utils.data import Counterexample, Predicate
from anthem_cx.utils.solving import (
    _get_holds,
    _solve_gc_with_size,
    _solve_with_size,
    solve_for_counterexample,
    solve_gc_for_counterexample,
)


class _FakeModel:
    """Minimal stand-in for a clingo Model that yields no symbols."""

    def symbols(self, **_kwargs: object) -> list[object]:
        """Return no symbols."""
        return []


class TestGetHolds(TestCase):
    """Tests for _get_holds."""

    def test_get_holds(self) -> None:
        """Generated holds rules match expected patterns; empty set returns only the #defined declaration."""
        self.assertEqual(_get_holds(set()), "#defined holds/1.")
        for preds, undo, expected in [
            ({Predicate("a", 0)}, False, "holds(a) :- a."),
            ({Predicate("p", 1)}, False, "holds(p(X0)) :- p(X0)."),
            ({Predicate("r", 2)}, False, "holds(r(X0,X1)) :- r(X0,X1)."),
            ({Predicate("a", 0)}, True, "a :- holds(a)."),
            ({Predicate("p", 1)}, True, "p(X0) :- holds(p(X0))."),
            ({Predicate("r", 2)}, True, "r(X0,X1) :- holds(r(X0,X1))."),
            (set(), False, "#defined holds/1."),
        ]:
            self.assertIn(expected, _get_holds(preds, undo=undo))


class TestSolve(TestCase):
    """Tests for solving the counterexample program."""

    def test_solve_with_size(self) -> None:
        """SAT programs return a counterexample, UNSAT return None; domain-size constant is substituted."""
        for prog, size, sat in [
            ("a.", 0, True),
            (":- #true.", 0, False),
            ("#const n=0. a :- n > 1.", 2, True),
        ]:
            result = _solve_with_size(prog, True, size, set(), set(), [], "n")
            if sat:
                self.assertIsInstance(result, Counterexample)
            else:
                self.assertIsNone(result)

        # the returned counterexample carries the size, direction, and matching input atoms
        result = _solve_with_size("a.", True, 0, {Predicate("a", 0)}, set(), [], "n")
        assert result is not None
        self.assertEqual(result.size, 0)
        self.assertTrue(result.is_forward)
        self.assertEqual(result.input, ["a"])

    def test_solve_for_counterexample(self) -> None:
        """The loop returns a counterexample when found and None when the domain size max is exhausted."""
        # no programs: returns None once the domain size max is exceeded, including across several sizes
        for fwd, bwd, start, max_size in [
            (None, None, 2, 1),
            (None, None, 0, 0),
            (None, None, 0, 3),
        ]:
            self.assertIsNone(solve_for_counterexample(fwd, bwd, set(), set(), start, max_size, [], "n"))

        # a satisfiable program yields a counterexample in the corresponding direction
        for fwd, bwd, is_forward in [
            ("a.", None, True),
            (":- #true.", "a.", False),
        ]:
            result = solve_for_counterexample(fwd, bwd, set(), set(), 0, None, [], "n")
            assert result is not None
            self.assertEqual(result.is_forward, is_forward)


class TestSolveGC(TestCase):
    """Tests for solving the guess and check counterexample program."""

    def test_solve_gc_with_size(self) -> None:
        """A counterexample is returned only when the underlying solver reports a model."""
        for model_found in [True, False]:

            def fake_solve(*_args: object, on_model: object = None, **_kwargs: object) -> bool:
                # pylint: disable=cell-var-from-loop
                if model_found and on_model is not None:
                    on_model(_FakeModel())  # type: ignore[operator]
                return model_found

            with patch("anthem_cx.utils.solving.solve_guess_and_check", side_effect=fake_solve):
                result = _solve_gc_with_size("a.", "b.", True, 0, set(), set(), [], "n")
            if model_found:
                self.assertIsInstance(result, Counterexample)
            else:
                self.assertIsNone(result)

    def test_solve_gc_for_counterexample(self) -> None:
        """The loop returns a counterexample when found and None when the domain size max is exhausted."""
        # no programs: returns None once the domain size max is exceeded
        for fg, fc, bg, bc, start, max_size in [
            (None, None, None, None, 2, 1),
            (None, None, None, None, 0, 0),
        ]:
            result = solve_gc_for_counterexample(fg, fc, bg, bc, set(), set(), start, max_size, [], "n")
            self.assertIsNone(result)

        # a found counterexample is returned in the corresponding direction
        cex = Counterexample(0, True, [], [])
        with patch("anthem_cx.utils.solving._solve_gc_with_size", return_value=cex):
            for fg, fc, bg, bc in [
                ("g.", "c.", None, None),
                (None, None, "bg.", "bc."),
            ]:
                result = solve_gc_for_counterexample(fg, fc, bg, bc, set(), set(), 0, None, [], "n")
                self.assertIs(result, cex)

        # nothing found within the domain size max returns None
        with patch("anthem_cx.utils.solving._solve_gc_with_size", return_value=None):
            result = solve_gc_for_counterexample(
                "g.", "c.", "bg.", "bc.", {Predicate("a", 0)}, {Predicate("b", 1)}, 0, 0, [], "n"
            )
        self.assertIsNone(result)
