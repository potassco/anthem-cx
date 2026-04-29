"""
Module to check if a program contains disjunctive rules.
"""

from clingo.ast import AST, ASTType, Transformer

from ..utils.logging import get_logger

log = get_logger(__name__)


class RejectDisjunctions(Transformer):
    """
    Reject any disjunctive rules.
    """

    def visit_Rule(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Raise an exception if the rule is disjunctive.
        """
        if node.head.ast_type == ASTType.Disjunction and len(node.head.elements) > 1:
            log.error("Disjunctive rules not supported %s", node)
            raise RuntimeError(f"Disjunctive rules not allowed {node}")
        return node
