"""
Module to reject classical negation.
"""

from clingo.ast import AST, ASTType, Transformer

from ..utils.errors import AnthemCXError


class RejectClassicalNegation(Transformer):
    """
    Reject classically negated atoms (e.g. -p), which are not supported.
    """

    def visit_SymbolicAtom(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Raise an error if the atom uses classical negation.

        Classical negation is represented as a symbolic atom whose symbol is a
        unary operation (e.g. -p); ordinary atoms have a function or pool symbol.
        The check is on the atom's symbol only, so arithmetic negation in an
        argument (e.g. p(-X)) is not affected.
        """
        if node.symbol.ast_type == ASTType.UnaryOperation:
            raise AnthemCXError(f"classical negation is not supported: {node}")
        return node
