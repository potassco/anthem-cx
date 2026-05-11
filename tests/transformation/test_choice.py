"""
Tests for choice rule transformers.
"""

from unittest import TestCase

from anthem_cx.transformation import (
    ChoiceConditionNormalizer,
    ChoiceElementNormalizer,
    ChoiceGuardNormalizer,
    ChoicePoolNormalizer,
    ChoiceTermNormalizer,
)

from . import assert_transform

CHOICE_GUARD_CASES = [
    (
        "1 <= { p(X) } <= 2 :- r(X).",
        "{ p(X) } :- r(X). :- r(X), not 1 <= { p(X) } <= 2.",
    ),
    (
        "1 <= { p(X) : q(X) } :- r(X).",
        "{ p(X) : q(X) } :- r(X). :- r(X), not 1 <= { p(X) : q(X) }.",
    ),
    (
        "{ p(X) } :- r(X).",
        "{ p(X) } :- r(X).",
    ),
    # non-choice rule passes through unchanged
    (
        "p(X) :- q(X).",
        "p(X) :- q(X).",
    ),
]

CHOICE_ELEMENT_CASES = [
    (
        "{ p(X) ; q(Y) } :- r.",
        "{ p(X) } :- r. { q(Y) } :- r.",
    ),
    (
        "{ p(X) : q(X) } :- r.",
        "{ p(X) : q(X) } :- r.",
    ),
    # non-choice rule passes through unchanged
    (
        "p(X) :- q(X).",
        "p(X) :- q(X).",
    ),
]

CHOICE_POOL_CASES = [
    ("{ p(1;a,b) }.", "{ p(1) }. { p(a,b) }."),
    (
        "{ p(1;2) } :- r.",
        "{ p(1) } :- r. { p(2) } :- r.",
    ),
    (
        "{ p(a;b) } :- r.",
        "{ p(a) } :- r. { p(b) } :- r.",
    ),
    (
        "{ p(X) } :- r.",
        "{ p(X) } :- r.",
    ),
    # non-choice rule passes through unchanged
    (
        "p(X) :- q(X).",
        "p(X) :- q(X).",
    ),
]

CHOICE_TERM_CASES = [
    (
        "{ p(1..3) } :- r.",
        "{ p(_X1) : _X1 = 1..3 } :- r.",
    ),
    (
        "{ p(1..3) : q(X) } :- r.",
        "{ p(_X1) : q(X), _X1 = 1..3 } :- r.",
    ),
    # function argument: _rewrite_term recurses into function args
    (
        "{ p(f(1..5)) } :- r.",
        "{ p(f(_X1)) : _X1 = 1..5 } :- r.",
    ),
    # unary operation argument: _rewrite_term recurses into unary operand
    (
        "{ p(-X) : X = 1..3 } :- r.",
        "{ p(-X) : X = 1..3 } :- r.",
    ),
    # binary operation argument: _rewrite_term recurses into both operands
    (
        "{ p((1..3)+1) } :- r.",
        "{ p(_X1+1) : _X1 = 1..3 } :- r.",
    ),
    (
        "{ p(X) } :- r.",
        "{ p(X) } :- r.",
    ),
    # non-choice rule passes through unchanged
    (
        "p(X) :- q(X).",
        "p(X) :- q(X).",
    ),
]

CHOICE_CONDITION_CASES = [
    (
        "{ p(X) : q(X) } :- r(X).",
        "{ p(X) } :- r(X), q(X).",
    ),
    (
        "{ p(X) : q(X), s(X) } :- r(X).",
        "{ p(X) } :- r(X), q(X), s(X).",
    ),
    (
        "{ p(X) } :- r(X).",
        "{ p(X) } :- r(X).",
    ),
    # non-choice rule passes through unchanged
    (
        "p(X) :- q(X).",
        "p(X) :- q(X).",
    ),
]


class TestChoiceGuardNormalizer(TestCase):
    """Tests for ChoiceGuardNormalizer."""

    def test_cases(self) -> None:
        """Test all ChoiceGuardNormalizer cases."""
        for input_str, expected_str in CHOICE_GUARD_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, ChoiceGuardNormalizer(), input_str, expected_str)


class TestChoiceElementNormalizer(TestCase):
    """Tests for ChoiceElementNormalizer."""

    def test_cases(self) -> None:
        """Test all ChoiceElementNormalizer cases."""
        for input_str, expected_str in CHOICE_ELEMENT_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, ChoiceElementNormalizer(), input_str, expected_str)


class TestChoicePoolNormalizer(TestCase):
    """Tests for ChoicePoolNormalizer."""

    def test_cases(self) -> None:
        """Test all ChoicePoolNormalizer cases."""
        for input_str, expected_str in CHOICE_POOL_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, ChoicePoolNormalizer(), input_str, expected_str)

    def test_raises_multi_element(self) -> None:
        """Multi-element choice raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            assert_transform(self, ChoicePoolNormalizer(), "{ p(X) ; q(X) } :- r.", "")


class TestChoiceTermNormalizer(TestCase):
    """Tests for ChoiceTermNormalizer."""

    def test_cases(self) -> None:
        """Test all ChoiceTermNormalizer cases."""
        for input_str, expected_str in CHOICE_TERM_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, ChoiceTermNormalizer(), input_str, expected_str)

    def test_raises_pool_symbol(self) -> None:
        """Choice element with pool symbol raises RuntimeError."""
        # { p(1;2) } has a Pool as the SymbolicAtom symbol, which ChoiceTermNormalizer rejects.
        with self.assertRaises(RuntimeError):
            assert_transform(self, ChoiceTermNormalizer(), "{ p(1;2) } :- r.", "")


class TestChoiceConditionNormalizer(TestCase):
    """Tests for ChoiceConditionNormalizer."""

    def test_cases(self) -> None:
        """Test all ChoiceConditionNormalizer cases."""
        for input_str, expected_str in CHOICE_CONDITION_CASES:
            with self.subTest(input=input_str):
                assert_transform(self, ChoiceConditionNormalizer(), input_str, expected_str)

    def test_raises_multi_element(self) -> None:
        """Multi-element choice raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            assert_transform(self, ChoiceConditionNormalizer(), "{ p(X) ; q(X) } :- r.", "")
