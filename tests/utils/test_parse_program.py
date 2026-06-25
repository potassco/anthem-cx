"""
Tests for utils/parse_program.py: parse_program.
"""

import os
import tempfile
from unittest import TestCase

from anthem_cx.utils.errors import AnthemCXError
from anthem_cx.utils.parse_program import parse_program


def _write_program(content: str) -> str:
    """Write content to a temp file and return the path."""
    fd, path = tempfile.mkstemp(suffix=".lp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


class TestParseProgram(TestCase):
    """Tests for program parsing."""

    def test_parse_program(self) -> None:
        """Test parsing programs."""
        for prg, num_rules in [
            ("a. b.", 2),
            ("a :- b.", 1),
            ("", 0),
        ]:
            path = _write_program(prg)
            try:
                prg_parsed = parse_program(path)
                prg_str = " ".join(str(n) for n in prg_parsed)
                self.assertEqual(len(prg_parsed), num_rules + 1)
                self.assertIn("#program base.", prg_str)
                self.assertIn(prg, prg_str)
            finally:
                os.unlink(path)

    def test_syntax_error_raises_anthem_error(self) -> None:
        """A program with a syntax error raises an AnthemCXError, not a bare RuntimeError."""
        path = _write_program("p :- :- q.")
        try:
            with self.assertRaises(AnthemCXError):
                parse_program(path)
        finally:
            os.unlink(path)

    def test_missing_file_raises_anthem_error(self) -> None:
        """A missing file raises an AnthemCXError."""
        with self.assertRaises(AnthemCXError):
            parse_program("/nonexistent/does-not-exist.lp")
