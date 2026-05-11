"""
Shared utilities for transformer unit tests.
"""

from unittest import TestCase

from clingo.ast import AST, Transformer, parse_string

from anthem_cx.utils.transformation import apply_transformer


def parse_program(program: str) -> list[AST]:
    """Parse an ASP program string into a list of AST nodes."""
    nodes: list[AST] = []
    parse_string(program, nodes.append)
    return nodes


def _normalize(rule_str: str) -> str:
    """Normalize constraints to use empty head (instead of false constant)."""
    # AST represents constraints as `#false :- body.`,
    # but transformations use an empty disjunction, i.e., `:- body.`
    return rule_str.replace("#false :- ", " :- ")


def assert_transform(
    test: TestCase,
    transformer: Transformer,
    input_str: str,
    expected_str: str,
) -> None:
    """
    Assert that applying transformer to the parsed input yields the parsed expected.

    Both sides are round-tripped through Clingo's parser so that syntactic
    normalization is applied consistently before comparison.
    """
    result = apply_transformer(transformer, parse_program(input_str))
    expected = parse_program(expected_str)
    test.assertEqual([_normalize(str(n)) for n in result], [_normalize(str(n)) for n in expected])
