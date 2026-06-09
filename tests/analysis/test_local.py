"""
Tests for analysis/local.py.
"""

from unittest import TestCase

from anthem_cx.analysis.local import is_locally_unique
from anthem_cx.utils.data import Counterexample

from . import parse_program


def _cx_helper(input_atoms: list[str], output_atoms: list[str]) -> Counterexample:
    return Counterexample(size=0, direction="forward", input=input_atoms, output=output_atoms)


class TestIsLocallyUnique(TestCase):
    """Tests for is_locally_unique."""

    def test_locally_unique(self) -> None:
        """A deterministic program has a single stable model and is locally unique."""
        for prg_str, counterexample in [
            ("b :- a.", _cx_helper(["a"], ["b"])),
            ("{ a }.", _cx_helper([], ["a"])),
            ("{ a } :- b.", _cx_helper([], [])),
            (":- a.", _cx_helper([], [])),
        ]:
            prg = parse_program(prg_str)
            self.assertTrue(is_locally_unique(prg, counterexample))

    def test_not_locally_unique(self) -> None:
        """A program with a choice has multiple stable models and is not locally unique."""
        for prg_str, counterexample in [
            ("{ a } :- b.", _cx_helper(["b"], [])),
        ]:
            prg = parse_program(prg_str)
            self.assertFalse(is_locally_unique(prg, counterexample))

    def test_no_stable_model(self) -> None:
        """A program with no stable model for the counterexample raises a ValueError."""
        for prg_str, counterexample in [
            (":- a.", _cx_helper([], ["a"])),
        ]:
            prg = parse_program(prg_str)
            self.assertRaises(ValueError, is_locally_unique, prg, counterexample)
