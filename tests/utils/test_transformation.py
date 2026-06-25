"""
Tests for utils.transformation module.

Covers the error branches and pool-symbol variants of atom_to_predicate,
map_atom, unmap_atom, is_mapped_predicate, aggregate_constraint, and
replace_predicate. The Function-symbol happy path of each function is already
exercised indirectly by the transformation tests.
"""

from unittest import TestCase

from clingo.ast import AST, Aggregate, ASTType, Function, Literal, Sign, parse_string

from anthem_cx.utils.data import Predicate
from anthem_cx.utils.transformation import (
    LOC,
    aggregate_constraint,
    atom_to_predicate,
    head_atom,
    is_mapped_predicate,
    map_atom,
    replace_predicate,
    unmap_atom,
)

from . import make_function_atom, make_pool_atom, make_unexpected_symbol_atom, make_variable_pool_atom

SUFFIX = "__"


def _parse_rule(src: str) -> AST:
    """Parse a single rule, returning its AST (skipping the #program directive)."""
    nodes: list[AST] = []
    parse_string(src, nodes.append)
    return nodes[1]


class TestHeadAtom(TestCase):
    """Tests for head_atom."""

    def test_cases(self) -> None:
        """head_atom returns the head predicate for literal/choice heads, None otherwise."""
        for src, expected in [
            # literal head -> its symbolic atom
            ("p :- q.", Predicate("p", 0)),
            # single-element choice head -> its symbolic atom
            ("{ p(X) } :- q(X).", Predicate("p", 1)),
            # constraint (non-symbolic literal head) -> None
            (":- q.", None),
            # head that is neither a literal nor a choice -> None
            ("a ; b :- c.", None),
        ]:
            with self.subTest(input=src):
                atom = head_atom(_parse_rule(src))
                predicate = atom_to_predicate(atom) if atom is not None else None
                self.assertEqual(predicate, expected)

    def test_raises(self) -> None:
        """Malformed choice heads raise ValueError."""
        for src in [
            # choice head with more than one element
            "{ p ; q } :- r.",
        ]:
            with self.subTest(input=src):
                with self.assertRaises(ValueError):
                    head_atom(_parse_rule(src))


class TestAtomToPredicate(TestCase):
    """Tests for atom_to_predicate."""

    def test_pool(self) -> None:
        """Pool SymbolicAtom returns a Predicate based on the first pool argument."""
        atom = make_pool_atom(["p", "q"])
        self.assertEqual(atom_to_predicate(atom), Predicate("p", 0))

    def test_non_symbolic_atom_raises(self) -> None:
        """Non-SymbolicAtom raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            atom_to_predicate(Function(LOC, "p", [], False))

    def test_unexpected_symbol_type_raises(self) -> None:
        """SymbolicAtom whose symbol is neither Function nor Pool raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            atom_to_predicate(make_unexpected_symbol_atom())


class TestMapAtom(TestCase):
    """Tests for map_atom."""

    def test_pool(self) -> None:
        """Pool SymbolicAtom maps the suffix onto every function in the pool."""
        atom = make_pool_atom(["p", "q"])
        result = map_atom(atom, SUFFIX)
        self.assertEqual(result.ast_type, ASTType.SymbolicAtom)
        self.assertEqual(result.symbol.ast_type, ASTType.Pool)
        self.assertEqual([arg.name for arg in result.symbol.arguments], ["p__", "q__"])

    def test_non_symbolic_atom_raises(self) -> None:
        """Non-SymbolicAtom raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            map_atom(Function(LOC, "p", [], False), SUFFIX)

    def test_unexpected_symbol_type_raises(self) -> None:
        """SymbolicAtom whose symbol is neither Function nor Pool raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            map_atom(make_unexpected_symbol_atom(), SUFFIX)

    def test_pool_with_variable_raises(self) -> None:
        """Pool that contains a Variable (not a Function) raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            map_atom(make_variable_pool_atom(), SUFFIX)


class TestUnmapAtom(TestCase):
    """Tests for unmap_atom."""

    def test_pool(self) -> None:
        """Pool SymbolicAtom strips the suffix from every function in the pool."""
        atom = make_pool_atom(["p__", "q__"])
        result = unmap_atom(atom, SUFFIX)
        self.assertEqual(result.ast_type, ASTType.SymbolicAtom)
        self.assertEqual(result.symbol.ast_type, ASTType.Pool)
        self.assertEqual([arg.name for arg in result.symbol.arguments], ["p", "q"])

    def test_non_symbolic_atom_raises(self) -> None:
        """Non-SymbolicAtom raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            unmap_atom(Function(LOC, "p", [], False), SUFFIX)

    def test_unexpected_symbol_type_raises(self) -> None:
        """SymbolicAtom whose symbol is neither Function nor Pool raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            unmap_atom(make_unexpected_symbol_atom(), SUFFIX)

    def test_pool_with_variable_raises(self) -> None:
        """Pool that contains a Variable (not a Function) raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            unmap_atom(make_variable_pool_atom(), SUFFIX)


class TestIsMappedPredicate(TestCase):
    """Tests for is_mapped_predicate."""

    def test_pool_mapped(self) -> None:
        """Returns True when the first function in the pool carries the suffix."""
        self.assertTrue(is_mapped_predicate(make_pool_atom(["p__", "q"]), SUFFIX))

    def test_pool_unmapped(self) -> None:
        """Returns False when the first function in the pool does not carry the suffix."""
        self.assertFalse(is_mapped_predicate(make_pool_atom(["p", "q__"]), SUFFIX))

    def test_non_symbolic_atom_raises(self) -> None:
        """Non-SymbolicAtom raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            is_mapped_predicate(Function(LOC, "p", [], False), SUFFIX)

    def test_unexpected_symbol_type_raises(self) -> None:
        """SymbolicAtom whose symbol is neither Function nor Pool raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            is_mapped_predicate(make_unexpected_symbol_atom(), SUFFIX)


class TestAggregateConstraint(TestCase):
    """Tests for aggregate_constraint."""

    def test_non_aggregate_raises(self) -> None:
        """Passing a non-aggregate AST node raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            aggregate_constraint(Function(LOC, "p", [], False), [])

    def test_aggregate(self) -> None:
        """Result is :- not A. — empty-disjunction head and a single negated aggregate in body."""
        agg = Aggregate(location=LOC, left_guard=None, elements=[], right_guard=None)
        result = aggregate_constraint(agg, [])
        self.assertEqual(result.head.ast_type, ASTType.Disjunction)
        self.assertEqual(len(result.head.elements), 0)
        self.assertEqual(len(result.body), 1)
        negated = result.body[0]
        self.assertEqual(negated.sign, Sign.Negation)
        self.assertEqual(str(negated.atom), str(agg))

    def test_with_body(self) -> None:
        """Original body literals appear first; the negated aggregate is appended last."""
        agg = Aggregate(location=LOC, left_guard=None, elements=[], right_guard=None)
        body_lit = Literal(LOC, Sign.NoSign, make_function_atom("r"))
        result = aggregate_constraint(agg, [body_lit])
        self.assertEqual(len(result.body), 2)
        self.assertEqual(str(result.body[0]), str(body_lit))
        self.assertEqual(result.body[1].sign, Sign.Negation)
        self.assertEqual(str(result.body[1].atom), str(agg))


class TestReplacePredicate(TestCase):
    """Tests for replace_predicate."""

    def test_function(self) -> None:
        """Replaces the predicate name in a Function SymbolicAtom."""
        atom = make_function_atom("p")
        result = replace_predicate(atom, Predicate("r", 0))
        self.assertEqual(result.ast_type, ASTType.SymbolicAtom)
        self.assertEqual(result.symbol.name, "r")

    def test_pool_raises_not_implemented(self) -> None:
        """Pool SymbolicAtom raises NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            replace_predicate(make_pool_atom(["p", "q"]), Predicate("r", 0))

    def test_non_symbolic_atom_raises(self) -> None:
        """Non-SymbolicAtom raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            replace_predicate(Function(LOC, "p", [], False), Predicate("r", 0))

    def test_unexpected_symbol_type_raises(self) -> None:
        """SymbolicAtom whose symbol is neither Function nor Pool raises RuntimeError."""
        with self.assertRaises(RuntimeError):
            replace_predicate(make_unexpected_symbol_atom(), Predicate("r", 0))
