"""
Module to normalize rule heads.
"""

from clingo.ast import AST, ASTType, Disjunction, Literal, Rule, Sign, Transformer

from ..utils.logging import get_logger
from ..utils.transformation import LOC

log = get_logger(__name__)


def _remove_negation(sign: Sign) -> Sign:
    """
    Remove one negation from sign.
    """
    match sign:
        case Sign.NoSign:
            log.warning("Unexpected no sign")  # nocoverage
            return sign  # nocoverage
        case Sign.Negation:
            return Sign.NoSign
        case Sign.DoubleNegation:
            return Sign.Negation


class RemoveHeadCondition(Transformer):
    """
    Remove conditional literals in rule heads

    h : c :- body. is turned into
    h :- body, c.
    """

    def visit_Rule(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Transform rules whose head is a conditional literal.
        """
        head = node.head

        # conditionals are elements of a disjunction
        if head.ast_type != ASTType.Disjunction:
            return node

        # empty head
        if len(head.elements) == 0:
            return node

        # ensure that the head only has one (disjunctive) element
        if len(head.elements) > 1:
            log.error("Unexpected disjunctive rule %s", node)
            raise RuntimeError(f"Unexpected disjunctive rule {node}")

        conditional = head.elements[0]

        # add the condition to the body
        new_body = list(node.body)
        for cond in conditional.condition:
            new_body.append(cond)

        new_rule = Rule(
            location=LOC,
            # new head is just the literal of the conditional
            head=conditional.literal,
            body=new_body,
        )

        return new_rule


class NormalizeHead(Transformer):
    """
    Normalize (non-choice) rule heads,
    i.e. remove negated heads and comparisons.

    1. single negation:
    not l :- body. is turned into
    :- body, l.

    2. double negation:
    not not l :- body. is turned into
    :- body, not l.

    3. comparisons:
    X < Y :- body. is turned into
    :- body, not X < Y.
    (note that negated comparisons are already handled in 1/2)
    """

    def visit_Rule(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Transform rules heads.
        """
        head = node.head

        # skip all rules whose head is not a literal
        if head.ast_type != ASTType.Literal:
            return node

        # only rules whose head literal is negated are transformed
        if head.sign in [Sign.Negation, Sign.DoubleNegation]:
            # empty head for the constraint
            empty_head = Disjunction(
                location=LOC,
                elements=[],
            )

            # remove a negation
            new_sign = _remove_negation(head.sign)

            # new body is obtained by adding the head atom with its new sign
            new_body = list(node.body)
            new_body.append(
                Literal(
                    location=LOC,
                    sign=new_sign,
                    atom=head.atom,
                )
            )

            new_rule = Rule(
                location=LOC,
                head=empty_head,
                body=new_body,
            )

            return new_rule

        if head.atom.ast_type == ASTType.Comparison:
            empty_head = Disjunction(location=LOC, elements=[])
            new_body = list(node.body)
            new_body.append(
                Literal(
                    location=LOC,
                    sign=Sign.Negation,
                    atom=head.atom,
                )
            )
            new_rule = Rule(
                location=LOC,
                head=empty_head,
                body=new_body,
            )
            return new_rule

        return node
