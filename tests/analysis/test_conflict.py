"""
Tests for analysis/conflict.py.
"""

from unittest import TestCase

from clingo.ast import Function, Variable

from anthem_cx.analysis import PredicateReplacer, collect_privates, get_replacement_predicate
from anthem_cx.analysis.conflict import (
    _collect_placeholders,
    _conflicting_predicates,
    _contains_suffix,
    _get_fresh_placeholder,
    _get_fresh_suffix,
    _is_ground,
    check_and_rename_auxiliaries,
    check_and_rename_privates,
    collect_ground_terms,
)
from anthem_cx.utils.data import Auxiliaries, Predicate
from anthem_cx.utils.transformation import LOC, apply_transformer

from . import parse_program


class TestIsGround(TestCase):
    """Tests for _is_ground."""

    def test_is_ground(self) -> None:
        """Test cases for is ground function."""
        for exp, result in [
            (Function(LOC, "f", [], False), True),
            (Function(LOC, "f", [Function(LOC, "a", [], False)], False), True),
            (Variable(LOC, "X"), False),
            (Function(LOC, "f", [Variable(LOC, "X")], False), False),
        ]:
            self.assertEqual(_is_ground(exp), result)


class TestCollectGroundTerms(TestCase):
    """Tests for collect_ground_terms."""

    def test_collect_ground_terms(self) -> None:
        """Test cases for ground term collection."""
        for prg, result in [
            ("", set()),
            ("p(1).", {"1"}),
            ("p(a).", {"a"}),
            ("p(X) :- q(X).", set()),
            ("p(f(a)).", {"f(a)", "a"}),
            ("p(1+2). p(X+3) :- q(X).", {"(1+2)", "1", "2", "3"}),
            ("p(-8).", {"-8", "8"}),
            ("#const n = 5.", {"5"}),
            ("p(1;a,b).", {"1", "a", "b"}),
        ]:
            self.assertEqual(collect_ground_terms(parse_program(prg)), result)


class TestPlaceholderCollector(TestCase):
    """Tests for PlaceholderCollector."""

    def test_collect_placeholders(self) -> None:
        """Test cases for placeholder collection."""
        for prg, result in [
            ("#const n = 5.", {"n"}),
            ("p(a).", set()),
        ]:
            self.assertEqual(_collect_placeholders(parse_program(prg)), result)


class TestPrivatePredicateCollector(TestCase):
    """Tests for PrivatePredicateCollector."""

    def test_collect_privates(self) -> None:
        """Test cases for privates collection."""
        for prg, publics, result in [
            ("a :- b.", set(), {Predicate("a", 0), Predicate("b", 0)}),
            ("a :- b.", {Predicate("a", 0)}, {Predicate("b", 0)}),
            ("{p;q}.", set(), {Predicate("p", 0), Predicate("q", 0)}),
        ]:
            self.assertEqual(collect_privates(parse_program(prg), publics), result)


class TestPredicateReplacer(TestCase):
    """Tests for PredicateReplacer."""

    def test_predicate_replacer(self) -> None:
        """Test replacement of predicates."""
        for prg, replacements, result in [
            ("a :- b.", {Predicate("a", 0): Predicate("a__0", 0)}, "a__0 :- b."),
            ("a :- b.", {Predicate("b", 0): Predicate("b__0", 0)}, "a :- b__0."),
            ("c :- b.", {Predicate("a", 0): Predicate("a__0", 0)}, "c :- b."),
        ]:
            prg_replaced = apply_transformer(PredicateReplacer(replacements), parse_program(prg))
            self.assertEqual(prg_replaced, parse_program(result))


class TestHelperFunctions(TestCase):
    """Tests for private helper functions."""

    def test_conflicting_predicates(self) -> None:
        """Test cases for conflicting predicates."""
        for left, right, result in [
            ({Predicate("a", 0), Predicate("b", 1)}, {Predicate("b", 1), Predicate("c", 0)}, {Predicate("b", 1)}),
            ({Predicate("a", 1)}, {Predicate("b", 1)}, set()),
        ]:
            self.assertEqual(_conflicting_predicates(left, right), result)

    def test_contains_suffix(self) -> None:
        """Test cases for contains suffix."""
        for preds, suffix, result in [
            ({Predicate("p__", 0), Predicate("q", 0)}, "__", True),
            ({Predicate("p", 0)}, "__", False),
            ({Predicate("p__p", 2)}, "__", False),
        ]:
            self.assertEqual(_contains_suffix(preds, suffix), result)

    def test_get_fresh_placeholder(self) -> None:
        """Test cases for get fresh placeholder."""
        for base, placeholders, result in [
            ("n", {"m", "k"}, "n__0"),
            ("n", {"n__0", "n__1"}, "n__2"),
        ]:
            self.assertEqual(_get_fresh_placeholder(base, placeholders), result)

    def test_get_fresh_suffix(self) -> None:
        """Test cases for get fresh suffix."""
        for base, preds, result in [
            ("__", {Predicate("p", 0)}, "__0"),
            ("__", {Predicate("p__0", 0)}, "__1"),
        ]:
            self.assertEqual(_get_fresh_suffix(base, preds), result)

    def test_get_replacement_predicate(self) -> None:
        """Test cases for get replacement predicate."""
        for base, preds, result in [
            (Predicate("p", 0), {Predicate("q", 0)}, Predicate("p__0", 0)),
            (Predicate("p", 0), {Predicate("p__0", 0)}, Predicate("p__1", 0)),
            (Predicate("p", 0), {Predicate("p__0", 1)}, Predicate("p__0", 0)),
        ]:
            self.assertEqual(get_replacement_predicate(base, preds), result)


class TestCheckAndRenameAuxiliaries(TestCase):
    """Tests for check_and_rename_auxiliaries."""

    def test_check_rename_aux(self) -> None:
        """Test cases for check and rename auxiliaries."""
        for left, right, publics, aux, terms, result in [
            ("p :- q.", "", set(), Auxiliaries.default(), set(), Auxiliaries.default()),
            ("p :- __bot.", "", set(), Auxiliaries.default(), set(), Auxiliaries.default().replace(unsat="__bot__0")),
            (
                "#const __domain_size = 1.",
                "",
                set(),
                Auxiliaries.default(),
                set(),
                Auxiliaries.default().replace(size="__domain_size__0"),
            ),
            (
                "p :- q.",
                "",
                set(),
                Auxiliaries.default(),
                {"__domain_size", "__domain_size__0"},
                Auxiliaries.default().replace(size="__domain_size__1"),
            ),
            ("p__ :- q.", "", set(), Auxiliaries.default(), set(), Auxiliaries.default().replace(suffix="__0")),
            (
                "p__ :- q.",
                "",
                {Predicate("p__", 0)},
                Auxiliaries.default(),
                set(),
                Auxiliaries.default().replace(suffix="__0"),
            ),
        ]:
            self.assertEqual(
                check_and_rename_auxiliaries(parse_program(left), parse_program(right), publics, aux, terms), result
            )


class TestCheckAndRenamePrivates(TestCase):
    """Tests for check_and_rename_privates."""

    def test_check_and_rename_privates(self) -> None:
        """Test cases for checking and renaming of privates."""
        for left, right, publics, result_left, result_right in [
            ("a :- p.", "b :- p.", {Predicate("p", 0)}, "a :- p.", "b :- p."),
            ("a :- p. q :- a.", "b :- p. q :- b.", {Predicate("p", 0)}, "a :- p. q :- a.", "b :- p. q__0 :- b."),
        ]:
            new_left, new_right = check_and_rename_privates(parse_program(left), parse_program(right), publics)
            self.assertEqual(new_left, parse_program(result_left))
            self.assertEqual(new_right, parse_program(result_right))
