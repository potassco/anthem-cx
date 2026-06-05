"""
Tests for utils/parse_user_guide.py.
"""

import logging
import os
import tempfile
from unittest import TestCase

from anthem_cx.utils.data import Predicate
from anthem_cx.utils.parse_user_guide import _split_entries, parse_user_guide


def _write_guide(content: str) -> str:
    """Write content to a temp file and return the path."""
    fd, path = tempfile.mkstemp(suffix=".ug")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


class TestSplitEntries(TestCase):
    """Tests for _split_entries."""

    def test_split_entries(self) -> None:
        """Test cases for split entries."""
        for entries, expected in [
            ("", []),
            ("input: p/1.", ["input: p/1"]),
            ("input: p/1. output: q/0.", ["input: p/1", "output: q/0"]),
            ("    input: p/1  .     . output: q/0.    ", ["input: p/1", "output: q/0"]),
        ]:
            self.assertEqual(_split_entries(entries), expected)


class TestParseUserGuide(TestCase):
    """Tests for parse_user_guide."""

    def test_supported_userguides(self) -> None:
        """Test cases with fully supported userguides."""
        for content, inputs, outputs in [
            ("", set(), set()),
            ("input: p/2.", {Predicate("p", 2)}, set()),
            ("output: q/1.", set(), {Predicate("q", 1)}),
            ("input: p/1. input: q/2. output: r/3.", {Predicate("p", 1), Predicate("q", 2)}, {Predicate("r", 3)}),
            ("  input :   p    /   4   .   output:    q / 0.", {Predicate("p", 4)}, {Predicate("q", 0)}),
        ]:
            path = _write_guide(content)
            try:
                ins, outs = parse_user_guide(path)
                self.assertEqual(ins, inputs)
                self.assertEqual(outs, outputs)
            finally:
                os.unlink(path)

    def test_unsupported_features(self) -> None:
        """Unsupported user guide features are skipped, keeping only the recognized predicates."""
        # silence the warnings emitted for the unsupported entries
        logging.disable(logging.WARNING)
        self.addCleanup(logging.disable, logging.NOTSET)
        for content, inputs, outputs in [
            ("assumption: a > b.", set(), set()),
            ("input: n -> int.", set(), set()),
            ("unknown.", set(), set()),
            ("input: p/1. input: n -> int. output: q/2.", {Predicate("p", 1)}, {Predicate("q", 2)}),
        ]:
            path = _write_guide(content)
            try:
                ins, outs = parse_user_guide(path)
                self.assertEqual(ins, inputs)
                self.assertEqual(outs, outputs)
            finally:
                os.unlink(path)
