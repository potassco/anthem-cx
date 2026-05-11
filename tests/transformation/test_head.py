"""
Tests for RemoveHeadCondition and NormalizeHead transformers.
"""

from unittest import TestCase

from anthem_cx.transformation import NormalizeHead, RemoveHeadCondition
from anthem_cx.utils.transformation import apply_transformer

from . import assert_transform, parse_program

REMOVE_HEAD_CONDITION_CASES = [
    (
        "p(X) : q(X) :- r(X).",
        "p(X) :- r(X), q(X).",
    ),
    (
        "p(X) :- r(X).",
        "p(X) :- r(X).",
    ),
]

NORMALIZE_HEAD_CASES = [
    (
        "not p(X) :- q(X).",
        ":- q(X), p(X).",
    ),
    (
        "not not p(X) :- q(X).",
        ":- q(X), not p(X).",
    ),
    (
        "X < Y :- q(X, Y).",
        ":- q(X, Y), not X < Y.",
    ),
    (
        "p(X) :- q(X).",
        "p(X) :- q(X).",
    ),
    # non-Literal head passes through unchanged
    (
        "{ p(X) } :- q(X).",
        "{ p(X) } :- q(X).",
    ),
]


class TestRemoveHeadCondition(TestCase):
    """Tests for RemoveHeadCondition."""

    def test_cases(self) -> None:
        """Test all RemoveHeadCondition cases."""
        for input_str, expected_str in REMOVE_HEAD_CONDITION_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, RemoveHeadCondition(), input_str, expected_str)

    def test_raises_on_disjunction(self) -> None:
        """Disjunctive head raises an exception."""
        with self.assertRaises(RuntimeError):
            assert_transform(self, RemoveHeadCondition(), "p(X) ; q(X) :- r(X).", "")

    def test_empty_disjunction_passthrough(self) -> None:
        """Empty Disjunction head (produced by NormalizeHead) passes through unchanged."""
        # NormalizeHead transforms negated heads into rules with empty Disjunction heads.
        # RemoveHeadCondition must pass those through without touching them.
        normalized = apply_transformer(NormalizeHead(), parse_program("not p(X) :- q(X)."))
        result = apply_transformer(RemoveHeadCondition(), normalized)
        self.assertEqual([str(n) for n in result], [str(n) for n in normalized])


class TestNormalizeHead(TestCase):
    """Tests for NormalizeHead."""

    def test_cases(self) -> None:
        """Test all NormalizeHead cases."""
        for input_str, expected_str in NORMALIZE_HEAD_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, NormalizeHead(), input_str, expected_str)
