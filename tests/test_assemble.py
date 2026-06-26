"""
Tests for anthem_cx/__init__.py: assemble_and_execute and helpers.
"""

import os
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from typing import Any
from unittest import TestCase
from unittest.mock import patch

from clingo.ast import AST, parse_string

from anthem_cx import assemble_and_execute, determine_uniqueness, reject_recursive_aggregates
from anthem_cx.utils.data import (
    Auxiliaries,
    Direction,
    Options,
    Programs,
    UniquenessCheck,
    UniquenessVerdict,
)
from anthem_cx.utils.errors import AnthemCXError


def _parse(src: str) -> list[AST]:
    nodes: list[AST] = []
    parse_string(src, nodes.append)
    return nodes


def _make_options(**kwargs: Any) -> Options:
    defaults: dict[str, Any] = {
        "direction": Direction.FORWARD,
        "out_dir": None,
        "solve": False,
        "start": 0,
        "max_size": 0,
        "uniqueness": UniquenessCheck.SKIP,
        "inputs": set(),
        "outputs": set(),
        "clingo_args": [],
        "auxiliaries": Auxiliaries.default(),
    }
    defaults.update(kwargs)
    return Options(**defaults)


def _make_programs(direction: Direction = Direction.FORWARD) -> Programs:
    left = _parse("a :- b.")
    right = _parse("b :- a.")
    reduct = _parse("c :- d.")
    return Programs(
        left=left,
        right=right,
        generate="#const __domain_size=0.\n__dom(0..__domain_size-1).\n",
        difference="__diff :- __bot.\n#defined __bot/0.",
        constraint=":- not __diff.",
        public_reduct_left=reduct if direction != Direction.FORWARD else None,
        public_reduct_right=reduct if direction != Direction.BACKWARD else None,
    )


class TestAssembleAndExecute(TestCase):
    """Tests for assemble_and_execute."""

    def test_prints_direction(self) -> None:
        """Direction label(s) appear in stdout output for both standard and GC modes."""
        for direction, verdict, expected in [
            (Direction.FORWARD, UniquenessVerdict.DIRECT, ["forward"]),
            (Direction.BACKWARD, UniquenessVerdict.DIRECT, ["backward"]),
            (Direction.UNIVERSAL, UniquenessVerdict.DIRECT, ["forward", "backward"]),
            (Direction.FORWARD, UniquenessVerdict.GUESS_CHECK, ["forward"]),
            (Direction.BACKWARD, UniquenessVerdict.GUESS_CHECK, ["backward"]),
            (Direction.UNIVERSAL, UniquenessVerdict.GUESS_CHECK, ["forward", "backward"]),
        ]:
            programs = _make_programs(direction)
            options = _make_options(direction=direction)
            out = StringIO()
            with redirect_stdout(out):
                assemble_and_execute(programs, options, verdict)
            text = out.getvalue().lower()
            for label in expected:
                self.assertIn(label, text)

    def test_saves_to_file_when_out_dir_set(self) -> None:
        """When out_dir is set the CX program is written to disk instead of stdout."""
        with tempfile.TemporaryDirectory() as tmpdir:
            for direction, verdict, expected_files in [
                (Direction.FORWARD, UniquenessVerdict.DIRECT, ["forward.lp"]),
                (
                    Direction.UNIVERSAL,
                    UniquenessVerdict.GUESS_CHECK,
                    ["forward_guess.lp", "forward_check.lp", "backward_guess.lp", "backward_check.lp"],
                ),
            ]:
                programs = _make_programs(direction)
                options = _make_options(direction=direction, out_dir=tmpdir)
                assemble_and_execute(programs, options, verdict)
                for f in expected_files:
                    self.assertTrue(os.path.exists(os.path.join(tmpdir, f)))

    def test_solve_calls_solver(self) -> None:
        """With solve=True the appropriate solver function is invoked."""
        for verdict, patch_target in [
            (UniquenessVerdict.DIRECT, "anthem_cx.solve_for_counterexample"),
            (UniquenessVerdict.GUESS_CHECK, "anthem_cx.solve_gc_for_counterexample"),
        ]:
            programs = _make_programs(Direction.FORWARD)
            options = _make_options(direction=Direction.FORWARD, solve=True)
            with patch(patch_target) as mock_solve:
                assemble_and_execute(programs, options, verdict)
                mock_solve.assert_called_once()


class TestRejectRecursiveAggregates(TestCase):
    """Tests for reject_recursive_aggregates."""

    def test_rejects_recursive_aggregates(self) -> None:
        """A recursive aggregate in either program raises an AnthemCXError."""
        aggregate = _parse("a :- 1 <= #count{ 1 : a }.")
        for left, right in [(aggregate, _parse("")), (_parse(""), aggregate)]:
            self.assertRaises(AnthemCXError, reject_recursive_aggregates, left, right)


class TestDetermineUniqueness(TestCase):
    """Tests for determine_uniqueness."""

    def test_returns_verdict(self) -> None:
        """determine_uniqueness returns the verdict for the selected check."""
        # programs and their (negative cycle, odd negative cycle) properties for empty publics:
        #   ""                -> (False, False)
        #   "a :- not a."     -> (True, True)
        #   "{a}."            -> (True, False)
        #   "a :- b. b :- a." -> (False, False)
        for left, right, check, expected in [
            # skip / fail decide directly, independent of the programs
            ("a :- not a.", "", UniquenessCheck.SKIP, UniquenessVerdict.DIRECT),
            ("a :- b. b :- a.", "", UniquenessCheck.FAIL, UniquenessVerdict.GUESS_CHECK),
            # auto mode: left has an odd negative cycle -> local precondition fails -> guess and check
            ("a :- not a.", "", UniquenessCheck.AUTO, UniquenessVerdict.GUESS_CHECK),
            # auto mode: right has an odd negative cycle -> local precondition fails -> guess and check
            ("", "a :- not a.", UniquenessCheck.AUTO, UniquenessVerdict.GUESS_CHECK),
            # auto mode: both stratified -> stratification succeeds -> solve directly
            ("a :- b. b :- a.", "", UniquenessCheck.AUTO, UniquenessVerdict.DIRECT),
            # auto mode: not stratified but no odd negative cycle -> defer to local check
            ("{a}.", "", UniquenessCheck.AUTO, UniquenessVerdict.NEEDS_LOCAL_CHECK),
            # stratification mode: negative cycle -> fall back to guess and check
            ("{a}.", "", UniquenessCheck.STRATIFICATION, UniquenessVerdict.GUESS_CHECK),
            # stratification mode: stratified -> solve directly
            ("a :- b. b :- a.", "", UniquenessCheck.STRATIFICATION, UniquenessVerdict.DIRECT),
            # local mode: odd negative cycle -> precondition fails -> guess and check
            ("a :- not a.", "", UniquenessCheck.LOCAL, UniquenessVerdict.GUESS_CHECK),
            # local mode: no odd negative cycle -> defer to local check
            ("{a}.", "", UniquenessCheck.LOCAL, UniquenessVerdict.NEEDS_LOCAL_CHECK),
        ]:
            verdict = determine_uniqueness(_parse(left), _parse(right), set(), check)
            self.assertEqual(verdict, expected)
