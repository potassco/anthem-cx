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

from anthem_cx import assemble_and_execute
from anthem_cx.utils.data import (
    Auxiliaries,
    Direction,
    EVAData,
    Options,
    Programs,
)


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
        "eva": EVAData(False, False, False),
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
        difference="__diff :- __bot.\n#defined __bot/0.\n:- not __diff.",
        public_reduct_left=reduct if direction != Direction.FORWARD else None,
        public_reduct_right=reduct if direction != Direction.BACKWARD else None,
    )


class TestAssembleAndExecute(TestCase):
    """Tests for assemble_and_execute."""

    def test_prints_direction(self) -> None:
        """Direction label(s) appear in stdout output for both standard and GC modes."""
        for direction, eva, expected in [
            (Direction.FORWARD, EVAData(False, False, False), ["forward"]),
            (Direction.BACKWARD, EVAData(False, False, False), ["backward"]),
            (Direction.UNIVERSAL, EVAData(False, False, False), ["forward", "backward"]),
            (Direction.FORWARD, EVAData(True, False, False), ["forward"]),
            (Direction.BACKWARD, EVAData(True, False, False), ["backward"]),
            (Direction.UNIVERSAL, EVAData(True, False, False), ["forward", "backward"]),
        ]:
            programs = _make_programs(direction)
            options = _make_options(direction=direction, eva=eva)
            out = StringIO()
            with redirect_stdout(out):
                assemble_and_execute(programs, options)
            text = out.getvalue().lower()
            for label in expected:
                self.assertIn(label, text)

    def test_saves_to_file_when_out_dir_set(self) -> None:
        """When out_dir is set the EQT is written to disk instead of stdout."""
        with tempfile.TemporaryDirectory() as tmpdir:
            for direction, eva, expected_files in [
                (Direction.FORWARD, EVAData(False, False, False), ["forward.lp"]),
                (
                    Direction.UNIVERSAL,
                    EVAData(True, False, False),
                    ["forward_guess.lp", "forward_check.lp", "backward_guess.lp", "backward_check.lp"],
                ),
            ]:
                programs = _make_programs(direction)
                options = _make_options(direction=direction, eva=eva, out_dir=tmpdir)
                assemble_and_execute(programs, options)
                for f in expected_files:
                    self.assertTrue(os.path.exists(os.path.join(tmpdir, f)))

    def test_solve_calls_solver(self) -> None:
        """With solve=True the appropriate solver function is invoked."""
        for eva, patch_target in [
            (EVAData(False, False, False), "anthem_cx.solve_for_counterexample"),
            (EVAData(True, False, False), "anthem_cx.solve_gc_for_counterexample"),
        ]:
            programs = _make_programs(Direction.FORWARD)
            options = _make_options(direction=Direction.FORWARD, solve=True, eva=eva)
            with patch(patch_target) as mock_solve:
                assemble_and_execute(programs, options)
                mock_solve.assert_called_once()
