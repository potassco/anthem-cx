"""
Tests for analysis/inputs.py.
"""

from unittest import TestCase

from anthem_cx.analysis.inputs import check_inputs_not_in_heads, collect_head_predicates, inputs_in_heads
from anthem_cx.utils.data import Predicate
from anthem_cx.utils.errors import AnthemCXError

from . import parse_program


class TestCollectHeadPredicates(TestCase):
    """Tests for collect_head_predicates."""

    def test_collect_head_predicates(self) -> None:
        """Test cases for collecting head predicates."""
        for prg, result in [
            ("", set()),
            ("p(X) :- q(X).", {Predicate("p", 1)}),
            ("{ p(X) } :- q(X).", {Predicate("p", 1)}),
            (":- q(X).", set()),
            ("p. p(X) :- q(X).", {Predicate("p", 0), Predicate("p", 1)}),
        ]:
            self.assertEqual(collect_head_predicates(parse_program(prg)), result)

    def test_multiple_choice_elements_raises(self) -> None:
        """A choice head with more than one element raises."""
        self.assertRaises(ValueError, collect_head_predicates, parse_program("{ p(X); q(X) } :- r(X)."))


class TestInputsInHeads(TestCase):
    """Tests for inputs_in_heads."""

    def test_inputs_in_heads(self) -> None:
        """Test cases for detecting input predicates in heads."""
        inputs = {Predicate("q", 1)}
        for prg, result in [
            ("p(X) :- q(X).", set()),
            ("q(X) :- p(X).", {Predicate("q", 1)}),
            ("{ q(X) } :- p(X).", {Predicate("q", 1)}),
            (":- q(X).", set()),
        ]:
            self.assertEqual(inputs_in_heads(parse_program(prg), inputs), result)


class TestCheckInputsNotInHeads(TestCase):
    """Tests for check_inputs_not_in_heads."""

    def test_passes(self) -> None:
        """A program with no input predicate in a head passes."""
        inputs = {Predicate("q", 1)}
        left = parse_program("p(X) :- q(X).")
        right = parse_program(":- q(X).")
        check_inputs_not_in_heads(left, right, inputs)

    def test_left_fails(self) -> None:
        """An input predicate in the left program head raises."""
        inputs = {Predicate("q", 1)}
        left = parse_program("q(X) :- p(X).")
        right = parse_program("")
        self.assertRaises(AnthemCXError, check_inputs_not_in_heads, left, right, inputs)

    def test_right_fails(self) -> None:
        """An input predicate in the right program head raises."""
        inputs = {Predicate("q", 1)}
        left = parse_program("")
        right = parse_program("{ q(X) } :- p(X).")
        self.assertRaises(AnthemCXError, check_inputs_not_in_heads, left, right, inputs)
