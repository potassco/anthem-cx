"""
Tests for utils/output.py: program_to_str, save_eqt_to_file, save_eqt_gc_to_file.
"""

import os
import tempfile
from unittest import TestCase

from clingo.ast import AST, parse_string

from anthem_cx.utils.output import build_eqt, build_eqt_gc, program_to_str, save_eqt_gc_to_file, save_eqt_to_file


def _parse(src: str) -> list[AST]:
    nodes: list[AST] = []
    parse_string(src, nodes.append)
    return nodes


class TestBuild(TestCase):
    """Tests for function building the counterexample programs."""

    def setUp(self) -> None:
        """Parse simple programs for use in tests."""
        self.left = _parse("a :- b.")
        self.right = _parse("b :- a.")

    def test_build_eqt(self) -> None:
        """Test building counterexample programs."""
        for forward, expected in [
            (
                True,
                (
                    "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
                    "% EQT forward\n"
                    "% input generation\n\n\n"
                    "% left program\n"
                    "#program base.\na :- b.\n\n"
                    "% public reduct of right program\n"
                    "#program base.\nb :- a.\n\n"
                    "% difference detection\n"
                    "\n% enforce counterexample\n"
                    ":- not __diff."
                ),
            ),
            (
                False,
                (
                    "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
                    "% EQT backward\n"
                    "% input generation\n\n\n"
                    "% right program\n"
                    "#program base.\na :- b.\n\n"
                    "% public reduct of left program\n"
                    "#program base.\nb :- a.\n\n"
                    "% difference detection\n"
                    "\n% enforce counterexample\n"
                    ":- not __diff."
                ),
            ),
        ]:
            result = build_eqt("", self.left, self.right, "", ":- not __diff.", forward=forward)
            self.assertEqual(result, expected)

    def test_build_eqt_gc(self) -> None:
        """Test building guess and check counterexample programs."""
        for forward, expected_guess, expected_check in [
            (
                True,
                (
                    "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
                    "% EQT forward guess\n"
                    "% input generation\n\n\n"
                    "% left program\n"
                    "#program base.\na :- b.\n"
                ),
                (
                    "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
                    "% EQT forward check\n"
                    "% public reduct of right program\n"
                    "#program base.\nb :- a.\n\n"
                    "% difference detection\n"
                    "\n% enforce counterexample\n"
                    ":- __diff."
                ),
            ),
            (
                False,
                (
                    "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
                    "% EQT backward guess\n"
                    "% input generation\n\n\n"
                    "% right program\n"
                    "#program base.\na :- b.\n"
                ),
                (
                    "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
                    "% EQT backward check\n"
                    "% public reduct of left program\n"
                    "#program base.\nb :- a.\n\n"
                    "% difference detection\n"
                    "\n% enforce counterexample\n"
                    ":- __diff."
                ),
            ),
        ]:
            guess, check = build_eqt_gc("", self.left, self.right, "", ":- __diff.", forward=forward)
            self.assertEqual(guess, expected_guess)
            self.assertEqual(check, expected_check)


class TestOutput(TestCase):
    """Tests for output functions."""

    def test_program_to_str(self) -> None:
        """Test output of program as str."""

        # test empty list of AST
        self.assertEqual(program_to_str([]), "")
        self.assertEqual(program_to_str([], newline=True), "\n")

        base_str = "#program base.\n"
        for prg, out in [
            ("a :- b.", "a :- b."),
            ("a. b :- a.", "a.\nb :- a."),
        ]:
            prg_parsed = _parse(prg)
            prg_out = program_to_str(prg_parsed)
            self.assertEqual(prg_out, base_str + out)

    def test_save_eqt_to_file(self) -> None:
        """Test saving counterexample program to file."""
        with tempfile.TemporaryDirectory() as tmp:
            # skip if no program provided
            save_eqt_to_file(None, tmp)
            self.assertEqual(os.listdir(tmp), [])

            for prg, forward, postfix, expected in [
                ("p.", True, None, "forward.lp"),
                ("p.", False, None, "backward.lp"),
                ("p.", True, "_test", "forward_test.lp"),
                ("p.", False, "_test", "backward_test.lp"),
            ]:
                save_eqt_to_file(prg, tmp, forward, postfix)
                expected = os.path.join(tmp, expected)
                self.assertTrue(os.path.exists(expected))
                with open(expected, encoding="utf-8") as f:
                    self.assertEqual(f.read(), prg)

            # create output directory
            new_dir = os.path.join(tmp, "nested", "out")
            save_eqt_to_file("a.", new_dir)
            self.assertTrue(os.path.exists(os.path.join(new_dir, "forward.lp")))

    def test_save_eqt_gc_to_file(self) -> None:
        """Test saving guess and check counterexample program to file."""
        with tempfile.TemporaryDirectory() as tmp:
            # skip if guess or check program not provided
            save_eqt_gc_to_file(None, "q.", tmp)
            self.assertEqual(os.listdir(tmp), [])
            save_eqt_gc_to_file("p.", None, tmp)
            self.assertEqual(os.listdir(tmp), [])

            for guess, check, forward, expected_guess, expected_check in [
                ("p.", "q.", True, "forward_guess.lp", "forward_check.lp"),
                ("p.", "q.", False, "backward_guess.lp", "backward_check.lp"),
            ]:
                save_eqt_gc_to_file(guess, check, tmp, forward)
                expected_guess = os.path.join(tmp, expected_guess)
                expected_check = os.path.join(tmp, expected_check)
                self.assertTrue(os.path.exists(expected_guess))
                self.assertTrue(os.path.exists(expected_check))
