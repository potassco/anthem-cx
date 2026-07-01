"""
Tests for ReplacePositiveOutputPredicates and TransformRuleHeads transformers.
"""

from unittest import TestCase

from anthem_cx.transformation import (
    ReplacePositiveOutputPredicates,
    TransformRuleHeads,
)
from anthem_cx.utils.data import Auxiliaries, Predicate

from . import assert_transform

AUX = Auxiliaries.default()
OUTPUTS: set[Predicate] = {Predicate("p", 1)}

REPLACE_POSITIVE_CASES = [
    (
        "p(X) :- q(X).",
        "p__(X) :- q(X).",
    ),
    (
        "q(X) :- p(X).",
        "q(X) :- p__(X).",
    ),
    (
        "p(X) :- p(X).",
        "p__(X) :- p__(X).",
    ),
    # negated literal is not replaced
    (
        "q(X) :- not p(X).",
        "q(X) :- not p(X).",
    ),
    (
        "q(X) :- r(X).",
        "q(X) :- r(X).",
    ),
    # BooleanConstant body literal passes through unchanged
    (
        "p(X) :- #true.",
        "p__(X) :- #true.",
    ),
    # Comparison body literal passes through unchanged
    (
        "q(X) :- X < 3.",
        "q(X) :- X < 3.",
    ),
    # output predicate inside a body aggregate is replaced
    (
        "q(X) :- 1 <= #count{ Y : p(Y) }.",
        "q(X) :- 1 <= #count{ Y : p__(Y) }.",
    ),
]

TRANSFORM_RULE_HEADS_CASES = [
    (
        ":- q(X).",
        "__bot :- q(X).",
    ),
    (
        "p(X) :- q(X).",
        "p(X) :- q(X).",
    ),
    (
        "q(X) :- r(X).",
        "q(X) :- r(X).",
    ),
    # mapped predicate in choice head becomes a normal rule with original atom in body
    (
        "{ p__(X) } :- q(X).",
        "p__(X) :- q(X), not not p(X).",
    ),
    # unmapped predicate in choice head passes through unchanged
    (
        "{ p(X) } :- q(X).",
        "{ p(X) } :- q(X).",
    ),
]


class TestReplacePositiveOutputPredicates(TestCase):
    """Tests for ReplacePositiveOutputPredicates."""

    def test_cases(self) -> None:
        """Test all ReplacePositiveOutputPredicates cases."""
        for input_str, expected_str in REPLACE_POSITIVE_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, ReplacePositiveOutputPredicates(OUTPUTS, AUX), input_str, expected_str)


class TestTransformRuleHeads(TestCase):
    """Tests for TransformRuleHeads."""

    def test_cases(self) -> None:
        """Test all TransformRuleHeads cases."""
        for input_str, expected_str in TRANSFORM_RULE_HEADS_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, TransformRuleHeads(OUTPUTS, AUX), input_str, expected_str)

    def test_raises(self) -> None:
        """Heads that violate the normal-form expectations raise RuntimeError."""
        for input_str in [
            # non-empty disjunction head
            "p(X) ; q(X) :- r(X).",
            # negated literal in choice head
            "{ not p__(X) } :- q(X).",
            # multi-element choice head
            "{ p__(X) ; q(X) } :- r.",
        ]:
            with self.subTest(input=input_str), self.assertRaises(RuntimeError):
                assert_transform(self, TransformRuleHeads(OUTPUTS, AUX), input_str, "")
