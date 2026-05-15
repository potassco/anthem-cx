"""Shared utilities for analysis unit tests."""

from clingo.ast import AST, parse_string


def parse_program(program: str) -> list[AST]:
    """Parse an ASP program string into a list of AST nodes."""
    nodes: list[AST] = []
    parse_string(program, nodes.append)
    return nodes
