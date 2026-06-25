"""
Module to check if a program contains disjunctive rules.
"""

from clingo.ast import AST, ASTType, Transformer

from ..utils.errors import AnthemCXError


class RejectDisjunctions(Transformer):
    """
    Reject any disjunctive rules.
    """

    def visit_Rule(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Raise an exception if the rule is disjunctive.
        """
        if node.head.ast_type == ASTType.Disjunction and len(node.head.elements) > 1:
            raise AnthemCXError(f"disjunctive rules are not supported: {node}")
        return node
