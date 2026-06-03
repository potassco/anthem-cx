"""
Tests for utils/solving.py.
"""

from contextlib import redirect_stdout
from functools import partial
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from clingo.control import Control
from clingo.symbol import Function as SymFunction

from anthem_cx.utils.data import Predicate
from anthem_cx.utils.solving import (
    _get_holds,
    _on_model,
    _solve_gc_with_size,
    _solve_with_size,
    _symbol_to_predicate,
    solve_for_counterexample,
    solve_gc_for_counterexample,
)


class TestSymbolToPredicate(TestCase):
    """Tests for _symbol_to_predicate."""

    def test_symbol_to_predicate(self) -> None:
        """Symbol maps to Predicate with matching arity."""
        for name, args, expected in [
            ("fact", [], Predicate("fact", 0)),
            ("p", [SymFunction("a", [], True)], Predicate("p", 1)),
        ]:
            sym = SymFunction(name, args, True)
            self.assertEqual(_symbol_to_predicate(sym), expected)


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


class TestOnModel(TestCase):
    """Tests for _on_model via a real Clingo solve."""

    def test_on_model(self) -> None:
        """Model output contains counterexample size, direction label, and predicate values."""
        for direction, size, program, inputs, outputs, expected in [
            ("forward", 1, "a.", set(), set(), ["Found a counterexample of size 1 in the forward direction", "left"]),
            ("backward", 1, "a.", set(), set(), ["right"]),
            (
                "forward",
                3,
                "a. b(1). b(2).",
                {Predicate("a", 0)},
                {Predicate("b", 1)},
                ["Found a counterexample of size 3 in the forward direction", "a", "b(1)"],
            ),
        ]:
            ctl = Control(["0"])
            ctl.add(program)
            ctl.ground()
            out = StringIO()
            with redirect_stdout(out):
                ctl.solve(on_model=partial(_on_model, direction, size, inputs, outputs))
            text = out.getvalue()
            for label in expected:
                self.assertIn(label, text)


class TestSolve(TestCase):
    """Tests for solving the counterexample program."""

    def test_solve_with_size(self) -> None:
        """Tests for _solve_with_size."""
        # SAT programs return True, UNSAT return False; domain-size constant is substituted
        for prog, size, expected in [
            ("a.", 0, True),
            (":- #true.", 0, False),
            ("#const n=0. a :- n > 1.", 2, True),
        ]:
            self.assertEqual(_solve_with_size(prog, "forward", size, set(), set(), [], "n"), expected)

        out = StringIO()
        with redirect_stdout(out):
            _solve_with_size("a.", "forward", 0, {Predicate("a", 0)}, set(), [], "n")
        self.assertIn("Found a counterexample", out.getvalue())

    def test_solve_for_counterexample(self) -> None:
        """Tests for solve_for_counterexample."""
        # loop exits or finds counterexample depending on programs and domain size bounds
        for fwd, bwd, start, max_size, expected in [
            (None, None, 2, 1, ["No counterexample"]),
            (None, None, 0, 0, ["No counterexample"]),
            (None, None, 0, 1, ["No counterexample", "Solving for counterexample of domain size 0"]),
            ("a.", None, 0, None, ["Solving for counterexample of domain size 0"]),
            (":- #true.", "a.", 0, None, ["Solving for counterexample of domain size 0"]),
        ]:
            out = StringIO()
            with redirect_stdout(out):
                solve_for_counterexample(fwd, bwd, set(), set(), start, max_size, [], "n")
            text = out.getvalue()
            for e in expected:
                self.assertIn(e, text)


class TestSolveGC(TestCase):
    """Tests for solving the guess and check counterexample program."""

    def test_solve_gc_with_size(self) -> None:
        """Tests for _solve_gc_with_size."""
        # return value mirrors the underlying solver's SAT/UNSAT result
        for sat, expected in [
            (True, True),
            (False, False),
        ]:
            with patch("anthem_cx.utils.solving.solve_guess_and_check", return_value=sat):
                self.assertEqual(_solve_gc_with_size("a.", "b.", "forward", 0, set(), set(), [], "n"), expected)

    def test_solve_gc_for_counterexample(self) -> None:
        """Tests for solve_gc_for_counterexample."""
        # loop exits or finds counterexample based on programs and domain size bounds
        for fg, fc, bg, bc, start, max_size, expected in [
            (None, None, None, None, 2, 1, "No counterexample"),
            (None, None, None, None, 0, 0, "No counterexample"),
        ]:
            out = StringIO()
            with redirect_stdout(out):
                solve_gc_for_counterexample(fg, fc, bg, bc, set(), set(), start, max_size, [], "n")
            self.assertIn(expected, out.getvalue())

        with patch("anthem_cx.utils.solving._solve_gc_with_size", return_value=True):
            for fg, fc, bg, bc in [
                ("g.", "c.", None, None),
                (None, None, "bg.", "bc."),
            ]:
                out = StringIO()
                with redirect_stdout(out):
                    solve_gc_for_counterexample(fg, fc, bg, bc, set(), set(), 0, None, [], "n")
                self.assertIn("Solving for counterexample of domain size 0", out.getvalue())

        with patch("anthem_cx.utils.solving._solve_gc_with_size", return_value=False):
            out = StringIO()
            with redirect_stdout(out):
                solve_gc_for_counterexample(
                    "g.", "c.", "bg.", "bc.", {Predicate("a", 0)}, {Predicate("b", 1)}, 0, 0, [], "n"
                )
            self.assertIn("No counterexample", out.getvalue())
