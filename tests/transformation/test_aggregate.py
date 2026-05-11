"""
Tests for HeadAggregateNormalizer transformer.
"""

from unittest import TestCase

from anthem_cx.transformation import HeadAggregateNormalizer

from . import assert_transform

HEAD_AGGREGATE_CASES = [
    (
        "1 <= #count{ X : p(X) } <= 2 :- r.",
        "{ p(X) } :- r. :- r, not 1 <= #count{ X : p(X) } <= 2.",
    ),
    (
        "1 <= #count{ X : p(X) : q(X) } <= 2 :- r.",
        "{ p(X) : q(X) } :- r. :- r, not 1 <= #count{ X : p(X), q(X) } <= 2.",
    ),
    (
        "p(X) :- q(X).",
        "p(X) :- q(X).",
    ),
]


class TestHeadAggregateNormalizer(TestCase):
    """Tests for HeadAggregateNormalizer."""

    def test_cases(self) -> None:
        """Test all HeadAggregateNormalizer cases."""
        for input_str, expected_str in HEAD_AGGREGATE_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, HeadAggregateNormalizer(), input_str, expected_str)
