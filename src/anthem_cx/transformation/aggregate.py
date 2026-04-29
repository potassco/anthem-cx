"""
Module to remove head aggregates.
"""

from clingo.ast import AST, ASTType, BodyAggregate, BodyAggregateElement, Transformer

from ..utils.transformation import LOC, aggregate_constraint, choice_rule_for_elements


class HeadAggregateNormalizer(Transformer):
    """
    Normalize head aggregates into choices and constraint.

    E.g. lower <= #count{ t : l : L } <= upper :- body. is turned into:
    1. { l : L } :- body. and
    2. :- body, not lower <= #count{ t : l, L } <= upper.
    """

    def visit_Rule(self, node: AST) -> AST | list[AST]:  # pylint: disable=invalid-name
        """
        Transform rules with head aggregates.
        """
        head = node.head

        # only head aggregates need to be changed
        if head.ast_type != ASTType.HeadAggregate:
            return node

        # choice rule from the elements of the aggregate
        choice_rule = choice_rule_for_elements(head.elements, node.body)

        # body aggregate corresponding to the original head aggregate
        body_aggregate_elements = []
        for elem in head.elements:
            conditional = elem.condition
            condition = []
            condition.append(conditional.literal)
            for x in conditional.condition:
                condition.append(x)
            new_elem = BodyAggregateElement(
                terms=elem.terms,
                condition=condition,
            )
            body_aggregate_elements.append(new_elem)

        body_aggregate = BodyAggregate(
            location=LOC,
            left_guard=head.left_guard,
            function=head.function,
            elements=body_aggregate_elements,
            right_guard=head.right_guard,
        )

        # constraint to enforce the aggregate
        constraint = aggregate_constraint(body_aggregate, node.body)

        return [choice_rule, constraint]
