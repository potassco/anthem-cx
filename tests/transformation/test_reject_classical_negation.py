"""
Tests for RejectClassicalNegation transformer.
"""

from unittest import TestCase

from anthem_cx.transformation import RejectClassicalNegation
from anthem_cx.utils.errors import AnthemCXError

from . import assert_transform

PASSTHROUGH_CASES = [
    "p(X) :- q(X).",
    ":- q(X).",
    "{ p(X) } :- q(X).",
    # arithmetic negation in an argument is fine
    "p(-X) :- q(X).",
]

RAISES_CASES = [
    # classical negation in a head
    "-p :- q.",
    # classical negation in a choice head
    "{ -p } :- q.",
    # classical negation in a body
    ":- -p.",
]


class TestRejectClassicalNegation(TestCase):
    """Tests for RejectClassicalNegation."""

    def test_passthrough(self) -> None:
        """Atoms without classical negation pass through unchanged."""
        for input_str in PASSTHROUGH_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, RejectClassicalNegation(), input_str, input_str)

    def test_raises(self) -> None:
        """Classically negated atoms raise AnthemCXError."""
        for input_str in RAISES_CASES:
            with self.subTest(input=input_str):
                with self.assertRaises(AnthemCXError):
                    assert_transform(self, RejectClassicalNegation(), input_str, "")
