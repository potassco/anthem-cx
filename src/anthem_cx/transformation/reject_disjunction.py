"""
Module to check if a program contains disjunctive rules.
"""

from clingo.ast import AST, ASTType, Transformer


class RejectDisjunctions(Transformer):
    """
    Reject any disjunctive rules.
    """

    def visit_Rule(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Raise an exception if the rule is disjunctive.
        """
        if node.head.ast_type == ASTType.Disjunction and len(node.head.elements) > 1:
            raise RuntimeError(f"Disjunctive rules not allowed {node}")
        return node
