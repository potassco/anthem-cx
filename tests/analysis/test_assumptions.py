"""
Tests for analysis/assumptions.py.
"""

from unittest import TestCase

from anthem_cx.analysis import collect_privates
from anthem_cx.analysis.assumptions import check_assumptions
from anthem_cx.utils.data import Auxiliaries, Predicate
from anthem_cx.utils.errors import AnthemCXError

from . import parse_program


class TestCheckAssumptions(TestCase):
    """Tests for check_assumptions."""

    def setUp(self) -> None:
        """Set up inputs, outputs, and auxiliaries for the tests."""
        self.inputs = {Predicate("in", 1)}
        self.outputs = {Predicate("out", 1)}
        self.aux = Auxiliaries.default()

    def test_unchanged(self) -> None:
        """Assumption programs without conflicting privates are returned unchanged."""
        for prg, left in [
            # only input predicates
            (":- in(X), not in(0).", ""),
            # a private predicate that does not clash with left/right
            ("aux(X) :- in(X). :- not aux(0).", ""),
            # the auxiliary domain predicate is allowed
            (f":- in(X), not {self.aux.domain}(X).", ""),
        ]:
            assumptions = parse_program(prg)
            result = check_assumptions(assumptions, self.inputs, self.outputs, parse_program(left), [], self.aux)
            self.assertEqual(result, parse_program(prg))

    def test_private_renamed_on_clash(self) -> None:
        """A private predicate clashing with a left/right predicate is renamed."""
        for prg, left, right, renamed in [
            ("aux(X) :- in(X). :- not aux(0).", "aux(X) :- p(X).", "", Predicate("aux", 1)),
            (":- in(X), q(X).", "", "q(X) :- r(X).", Predicate("q", 1)),
        ]:
            assumptions = parse_program(prg)
            result = check_assumptions(
                assumptions, self.inputs, self.outputs, parse_program(left), parse_program(right), self.aux
            )
            # the clashing private must no longer occur in the assumptions
            self.assertNotIn(renamed, collect_privates(result, self.inputs | self.outputs))

    def test_output_rejected(self) -> None:
        """An output predicate in the assumption program raises."""
        for prg in [
            ":- out(X).",
            "out(X) :- in(X).",
        ]:
            self.assertRaises(
                AnthemCXError, check_assumptions, parse_program(prg), self.inputs, self.outputs, [], [], self.aux
            )
