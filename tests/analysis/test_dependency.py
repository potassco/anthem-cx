"""
Tests for analysis/dependency.py.
"""

from unittest import TestCase

from clingo.ast import ASTType

from anthem_cx.analysis.dependency import (
    AggregateDependencyGraphBuilder,
    SignedDependencyGraphBuilder,
    _cycles_to_str,
    _edges_to_str,
    _nodes_to_str,
    has_enough_visible_atoms,
    has_recursive_aggregates,
)
from anthem_cx.utils import Predicate

from . import parse_program


class TestStringHelpers(TestCase):
    """Tests for _nodes_to_str, _edges_to_str, _cycles_to_str."""

    def test_nodes_to_str(self) -> None:
        """Test conversion of nodes to str."""
        for nodes, expected in [
            ([], "[]"),
            (["a"], "[a]"),
            (["a", "b", "c"], "[a, b, c]"),
        ]:
            self.assertEqual(_nodes_to_str(nodes), expected)

    def test_edges_to_str(self) -> None:
        """Test conversion of edges to str."""
        for edges, data, expected in [
            ([], False, "[]"),
            ([("a", "b"), ("c", "d")], False, "[(a,b), (c,d)]"),
            ([("a", "b", {"weight": -1}), ("c", "d", {"weight": 0})], True, "[((a,b), -1), ((c,d), 0)]"),
        ]:
            self.assertEqual(_edges_to_str(edges, data), expected)

    def test_cycles_to_str(self) -> None:
        for cycles, expected in [
            ([], "{}"),
            ([["a", "b"]], "{[a, b]}"),
            ([["a"], ["b", "c"]], "{[a], [b, c]}"),
        ]:
            self.assertEqual(_cycles_to_str(cycles), expected)


class TestHasEnoughVisibleAtoms(TestCase):
    """Tests for has_enough_visible_atoms (signed dependency graph analysis)."""

    def test_success(self) -> None:
        """Test cases that have enough visible atoms."""
        for prog, publics in [
            ("", set()),
            ("a :- not b.", {Predicate("a", 0), Predicate("b", 0)}),
            ("a :- b. b :- a.", set()),
            ("{a}.", {Predicate("a", 0)}),
            ("a :- 1 < 2.", {Predicate("a", 0)}),
            (":- a.", set()),
            ("a :- 1 <= #count{ 1 : b }.", {Predicate("a", 0), Predicate("b", 0)}),
        ]:
            self.assertTrue(has_enough_visible_atoms(parse_program(prog), publics))

    def test_failure(self) -> None:
        """Test cases that do not have enough visible atoms."""
        for prog, publics in [
            ("{a}.", set()),
            ("a :- not b. b :- not a.", set()),
        ]:
            self.assertFalse(has_enough_visible_atoms(parse_program(prog), publics))

    def test_signed_builder_visit_literal_null_head(self) -> None:
        """visit_Literal returns the node unchanged when current_head is None."""
        prog = parse_program("a :- b.")
        rules = [n for n in prog if n.ast_type == ASTType.Rule]
        body_literal = rules[0].body[0]
        builder = SignedDependencyGraphBuilder(set())
        result = builder.visit_Literal(body_literal)
        self.assertEqual(result, body_literal)

    def test_raises_on_multi_element_choice(self) -> None:
        """A choice rule with more than one element raises ValueError."""
        prog = parse_program("{a;b}.")
        builder = SignedDependencyGraphBuilder(set())
        with self.assertRaises(ValueError):
            for n in prog:
                builder(n)


class TestHasRecursiveAggregates(TestCase):
    """Tests for has_recursive_aggregates and AggregateDependencyGraphBuilder internals."""

    def test_success(self) -> None:
        """Test cases with recursive aggregates."""
        for prog in [
            "a :- 1 <= #count{ 1 : a }.",
            "a :- 1 <= { a }.",
            "a :- 1 <= { b : a }.",
        ]:
            self.assertTrue(has_recursive_aggregates(parse_program(prog)))

    def test_failure(self) -> None:
        """Test cases without recursive aggregates."""
        for prog in [
            "",
            "a :- b.",
            "a :- 1 <= #count{ X : b(X) }.",
            "a :- 1 <= #count{ a : b }.",
            "{a} :- a.",
        ]:
            self.assertFalse(has_recursive_aggregates(parse_program(prog)))

    def test_aggregate_builder_visit_literal_null_head(self) -> None:
        """visit_Literal returns the node unchanged when current_head is None."""
        prog = parse_program("a :- b.")
        rules = [n for n in prog if n.ast_type == ASTType.Rule]
        body_literal = rules[0].body[0]
        builder = AggregateDependencyGraphBuilder()
        result = builder.visit_Literal(body_literal)
        self.assertEqual(result, body_literal)

    def test_aggregate_builder_visit_literal_non_aggregate_body(self) -> None:
        """visit_Literal with a non-aggregate body literal returns the node unchanged."""
        prog = parse_program("a :- b.")
        rules = [n for n in prog if n.ast_type == ASTType.Rule]
        body_literal = rules[0].body[0]
        builder = AggregateDependencyGraphBuilder()
        for n in parse_program("a."):
            builder(n)
        result = builder.visit_Literal(body_literal)
        self.assertEqual(result, body_literal)

    def test_aggregate_builder_raises_on_multi_element_choice(self) -> None:
        """A choice rule head with more than one element raises ValueError."""
        prog = parse_program("{a;b}.")
        builder = AggregateDependencyGraphBuilder()
        with self.assertRaises(ValueError):
            for n in prog:
                builder(n)
