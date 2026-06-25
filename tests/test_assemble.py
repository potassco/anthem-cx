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

from anthem_cx import assemble_and_execute, run_syntactic_checks
from anthem_cx.utils.data import (
    Auxiliaries,
    Direction,
    Options,
    Programs,
    UniquenessData,
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
        "uniqueness": UniquenessData(False, False, False),
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
        for direction, gc, expected in [
            (Direction.FORWARD, UniquenessData(False, False, False), ["forward"]),
            (Direction.BACKWARD, UniquenessData(False, False, False), ["backward"]),
            (Direction.UNIVERSAL, UniquenessData(False, False, False), ["forward", "backward"]),
            (Direction.FORWARD, UniquenessData(True, False, False), ["forward"]),
            (Direction.BACKWARD, UniquenessData(True, False, False), ["backward"]),
            (Direction.UNIVERSAL, UniquenessData(True, False, False), ["forward", "backward"]),
        ]:
            programs = _make_programs(direction)
            options = _make_options(direction=direction, uniqueness=gc)
            out = StringIO()
            with redirect_stdout(out):
                assemble_and_execute(programs, options)
            text = out.getvalue().lower()
            for label in expected:
                self.assertIn(label, text)

    def test_saves_to_file_when_out_dir_set(self) -> None:
        """When out_dir is set the EQT is written to disk instead of stdout."""
        with tempfile.TemporaryDirectory() as tmpdir:
            for direction, gc, expected_files in [
                (Direction.FORWARD, UniquenessData(False, False, False), ["forward.lp"]),
                (
                    Direction.UNIVERSAL,
                    UniquenessData(True, False, False),
                    ["forward_guess.lp", "forward_check.lp", "backward_guess.lp", "backward_check.lp"],
                ),
            ]:
                programs = _make_programs(direction)
                options = _make_options(direction=direction, uniqueness=gc, out_dir=tmpdir)
                assemble_and_execute(programs, options)
                for f in expected_files:
                    self.assertTrue(os.path.exists(os.path.join(tmpdir, f)))

    def test_solve_calls_solver(self) -> None:
        """With solve=True the appropriate solver function is invoked."""
        for gc, patch_target in [
            (UniquenessData(False, False, False), "anthem_cx.solve_for_counterexample"),
            (UniquenessData(True, False, False), "anthem_cx.solve_gc_for_counterexample"),
        ]:
            programs = _make_programs(Direction.FORWARD)
            options = _make_options(direction=Direction.FORWARD, solve=True, uniqueness=gc)
            with patch(patch_target) as mock_solve:
                assemble_and_execute(programs, options)
                mock_solve.assert_called_once()


class TestRunSyntacticChecks(TestCase):
    """Tests for run_syntactic_checks."""

    def test_rejects_recursive_aggregates(self) -> None:
        """A recursive aggregate in either program raises an AnthemCXError."""
        aggregate = _parse("a :- 1 <= #count{ 1 : a }.")
        for left, right in [(aggregate, _parse("")), (_parse(""), aggregate)]:
            options = _make_options(uniqueness=UniquenessData(None, True, True))
            self.assertRaises(AnthemCXError, run_syntactic_checks, left, right, options, set())

    def test_updates_uniqueness_data(self) -> None:
        """The syntactic checks update opts.uniqueness in place depending on their outcome."""
        # programs and their (negative cycle, odd negative cycle) properties for empty publics:
        #   ""                -> (False, False)
        #   "a :- not a."     -> (True, True)
        #   "{a}."            -> (True, False)
        #   "a :- b. b :- a." -> (False, False)
        for left, right, initial, expected in [
            # auto mode: left has an odd negative cycle -> local precondition fails
            ("a :- not a.", "", UniquenessData(None, True, True), UniquenessData(True, True, False)),
            # auto mode: right has an odd negative cycle -> local precondition fails
            ("", "a :- not a.", UniquenessData(None, True, True), UniquenessData(True, True, False)),
            # auto mode: both stratified -> stratification succeeds, local check skipped
            ("a :- b. b :- a.", "", UniquenessData(None, True, True), UniquenessData(False, True, True)),
            # auto mode: not stratified but no odd negative cycle -> local precondition holds
            ("{a}.", "", UniquenessData(None, True, True), UniquenessData(None, True, True)),
            # stratification mode: negative cycle and no local check -> fall back to guess and check
            ("{a}.", "", UniquenessData(None, True, False), UniquenessData(True, True, False)),
            # use_gc already decided -> no checks are run
            ("a :- not a.", "", UniquenessData(False, False, False), UniquenessData(False, False, False)),
            # local mode (no syntactic checks) -> data is left unchanged
            ("a :- not a.", "", UniquenessData(None, False, True), UniquenessData(None, False, True)),
        ]:
            options = _make_options(uniqueness=initial)
            run_syntactic_checks(_parse(left), _parse(right), options, set())
            self.assertEqual(options.uniqueness, expected)
