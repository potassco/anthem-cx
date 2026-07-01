"""
Tests for RejectDisjunctions transformer.
"""

from unittest import TestCase

from anthem_cx.transformation import RejectDisjunctions
from anthem_cx.utils.errors import AnthemCXError

from . import assert_transform

PASSTHROUGH_CASES = [
    "p(X) :- q(X).",
    ":- q(X).",
    "{ p(X) } :- q(X).",
]

RAISES_CASES = [
    "p(X) ; q(X) :- r(X).",
    "p(X) ; q(X) ; r(X) :- s(X).",
    "p ; q.",
]


class TestRejectDisjunctions(TestCase):
    """Tests for RejectDisjunctions."""

    def test_passthrough(self) -> None:
        """Non-disjunctive rules pass through unchanged."""
        for input_str in PASSTHROUGH_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, RejectDisjunctions(), input_str, input_str)

    def test_raises(self) -> None:
        """Disjunctive rules raise AnthemCXError."""
        for input_str in RAISES_CASES:
            with self.subTest(input=input_str), self.assertRaises(AnthemCXError):
                assert_transform(self, RejectDisjunctions(), input_str, "")
