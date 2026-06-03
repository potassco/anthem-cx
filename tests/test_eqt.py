"""
Tests for eqt.py: normalize_program, get_generate_program,
get_difference_program, and get_public_reduct.
"""

from unittest import TestCase

from clingo.ast import AST, parse_string

from anthem_cx.eqt import (
    get_difference_program,
    get_generate_program,
    get_public_reduct,
    normalize_program,
)
from anthem_cx.utils.data import Auxiliaries, Predicate


def _parse(src: str) -> list[AST]:
    nodes: list[AST] = []
    parse_string(src, nodes.append)
    return nodes


AUX = Auxiliaries.default()


class TestNormalizeProgram(TestCase):
    """Tests for normalize_program."""

    def test_normalize_program(self) -> None:
        """Test program normalization."""
        for prg, expected in [
            ("p :- q.", ["p :- q."]),
            ("1 { p(X) } 1.", ["{ p(X) }.", " :- not 1 <= { p(X) } <= 1."]),
        ]:
            result = normalize_program(_parse(prg))
            for e in expected:
                self.assertIn(e, [str(n) for n in result])

        with self.assertRaises(RuntimeError):
            normalize_program(_parse("p ; q."))


class TestCounterexampleProgramComponents(TestCase):
    """Tests for the componentes of the counterexample program."""

    def test_get_generate_program(self):
        """Tests for get_generate_program."""
        for inputs, assumptions, terms, expected in [
            ({Predicate("a", 0)}, None, set(), f"#const {AUX.size}=0.\n{AUX.domain}(0..{AUX.size}-1).\n{{ a }}."),
            ({Predicate("p", 1)}, None, set(), f"{{ p(X0) }} :- {AUX.domain}(X0)."),
            ({Predicate("r", 2)}, None, set(), f"{{ r(X0,X1) }} :- {AUX.domain}(X0), {AUX.domain}(X1)."),
            (set(), None, {"42"}, f"{AUX.domain}(42)"),
            (set(), ":- p.", set(), ":- p."),
        ]:
            result = get_generate_program(inputs, assumptions, AUX, terms)
            self.assertIn(expected, result)

    def test_get_difference_program(self):
        """Tests for get_difference_program."""
        for outputs, expected in [
            (set(), [f":- not {AUX.diff}.", f"#defined {AUX.unsat}/0.", f"{AUX.diff} :- {AUX.unsat}."]),
            (
                {Predicate("a", 0)},
                [f"{AUX.diff} :- a, not a{AUX.suffix}.", f"{AUX.diff} :- not a, a{AUX.suffix}."],
            ),
            (
                {Predicate("p", 2)},
                [
                    f"{AUX.diff} :- p(X0,X1), not p{AUX.suffix}(X0,X1).",
                    f"{AUX.diff} :- not p(X0,X1), p{AUX.suffix}(X0,X1).",
                ],
            ),
        ]:
            result = get_difference_program(outputs, False, AUX)
            for e in expected:
                self.assertIn(e, result)

        # test gc
        self.assertIn(f":- {AUX.diff}.", get_difference_program(set(), True, AUX))
        self.assertNotIn(f":- not {AUX.diff}.", get_difference_program(set(), True, AUX))

    def test_get_public_reduct(self):
        """Tests for get_public_reduct."""
        for prg, outputs, expected in [
            ("p(X) :- q(X).", {Predicate("p", 1)}, "p__(X) :- q(X)."),
            (":- q.", {Predicate("q", 0)}, "__bot :- q__."),
            ("q(X) :- not p(X).", {Predicate("p", 1)}, "q(X) :- not p(X)."),
        ]:
            result = get_public_reduct(_parse(prg), outputs, AUX)
            self.assertIn(expected, [str(n) for n in result])
