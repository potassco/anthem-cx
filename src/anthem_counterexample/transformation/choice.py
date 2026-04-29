"""
Module to transform choice rules into normal form.
"""

from clingo.ast import (
    AST,
    Aggregate,
    ASTType,
    Comparison,
    ComparisonOperator,
    Guard,
    Literal,
    Location,
    Rule,
    Sign,
    SymbolicAtom,
    Transformer,
    Variable,
)

from ..utils.logging import get_logger
from ..utils.transformation import LOC, aggregate_constraint, choice_rule_for_elements

log = get_logger(__name__)


def _is_choice(head: AST) -> bool:
    return head.ast_type == ASTType.Aggregate


class ChoicePoolNormalizer(Transformer):
    """
    Remove choices over pools.

    E.g. { p(1;2) } :- body. is turned into:
    { p(1) } :- body. and
    { p(2) } :- body.
    """

    def visit_Rule(self, node: AST) -> AST | list[AST]:  # pylint: disable=invalid-name
        """
        Transform choice rules over a pool.
        """
        head = node.head
        if not _is_choice(head):
            return node

        if len(head.elements) != 1:
            raise RuntimeError(f"Choice rule with unexpected number of elements {node}")

        element = head.elements[0]
        atom = element.literal.atom
        symbol = atom.symbol

        if symbol.ast_type == ASTType.Pool:
            new_rules = []

            for arg in symbol.arguments:
                new_rules.append(
                    Rule(
                        location=LOC,
                        head=Literal(
                            location=LOC,
                            sign=Sign.NoSign,
                            atom=SymbolicAtom(symbol=arg),
                        ),
                        body=node.body,
                    )
                )

            return new_rules

        return node


class ChoiceTermNormalizer(Transformer):
    """
    Normalize terms containing intervals or pools in choice rules.

    E.g. { p(1..3) : q(X) } :- body. is turned into:
    { p(Y) : q(X), Y = 1..3 } :- body.
    """

    def __init__(self) -> None:
        super().__init__()
        self._var_counter = 0
        self.used_vars: set[str] = set()

    def _collect_used_vars(self, node: AST) -> None:
        """
        Collect all variables occurring in the rule.
        """
        self.used_vars.clear()

        class VarCollector(Transformer):
            """Helper class to collect variables."""

            def visit_Variable(self, node: AST) -> AST:  # pylint: disable=invalid-name
                """Collect variable."""
                self_outer.used_vars.add(node.name)
                return node

        self_outer = self
        VarCollector().visit(node)

    def _fresh_var(self, location: Location) -> AST:
        """
        Generate a fresh variable not occurring in the rule.
        """
        while True:
            self._var_counter += 1
            name = f"_X{self._var_counter}"
            if name not in self.used_vars:
                self.used_vars.add(name)
                return Variable(location, name)

    def _rewrite_term(self, term: AST, new_conditions: list[AST]) -> AST:
        """
        Recursively rewrite a term.

        If the term or any sub-term is an interval or a pool it is replaced by a fresh variable
        and an equality between the new variable and the term is added to new_conditions.
        """
        # case 1: interval or pool term
        if term.ast_type in (ASTType.Interval, ASTType.Pool):
            var = self._fresh_var(term.location)

            eq = Literal(
                term.location,
                Sign.NoSign,
                Comparison(var, [Guard(ComparisonOperator.Equal, term)]),
            )

            new_conditions.append(eq)
            return var

        # case 2: function term
        if term.ast_type == ASTType.Function:
            new_args = [self._rewrite_term(arg, new_conditions) for arg in term.arguments]
            return term.update(arguments=new_args)

        # case 3: unary operation
        if term.ast_type == ASTType.UnaryOperation:
            new_arg = self._rewrite_term(term.argument, new_conditions)
            return term.update(argument=new_arg)

        # case 4: binary operation
        if term.ast_type == ASTType.BinaryOperation:
            new_left = self._rewrite_term(term.left, new_conditions)
            new_right = self._rewrite_term(term.right, new_conditions)
            return term.update(left=new_left, right=new_right)

        return term

    def visit_Rule(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Transform choice rules containing intervals or pools.
        """
        head = node.head

        # skip any rules whose head is not an aggregate
        if not _is_choice(head):
            return node

        self._collect_used_vars(node)

        new_elements = []

        for elem in head.elements:
            atom = elem.literal.atom
            symbol = atom.symbol

            if symbol.ast_type != ASTType.Function:
                raise RuntimeError(f"Unexpected element {elem} in rule {node}")

            new_condition = list(elem.condition)

            # rewrite each term by replacing with a fresh variable if term is pool/interval
            # the equality between the new variable and the original term is added to new_condition
            new_args = [self._rewrite_term(arg, new_condition) for arg in symbol.arguments]

            new_symbol = symbol.update(arguments=new_args)

            new_atom = atom.update(symbol=new_symbol)

            new_lit = elem.literal.update(atom=new_atom)

            new_elem = elem.update(literal=new_lit, condition=new_condition)

            new_elements.append(new_elem)

        new_head = head.update(elements=new_elements)

        return node.update(head=new_head)


class ChoiceGuardNormalizer(Transformer):
    """
    Normalize choice heads by removing guards.

    E.g. lower <= { l : L } <= upper :- body. is turned into:
    1. { l : L } :- body. and
    2. :- body, not lower <= { l : L } <= upper.
    """

    def visit_Rule(self, node: AST) -> AST | list[AST]:  # pylint: disable=invalid-name
        """
        Transform choice rules.
        """
        head = node.head

        if not _is_choice(head):
            return node

        # skip choice rules without guards
        if head.left_guard is None and head.right_guard is None:
            return node

        # new choice rule without guards
        choice_rule = choice_rule_for_elements(head.elements, node.body)

        # body aggregate corresponding to the original choice head
        body_aggregate = Aggregate(
            location=LOC,
            left_guard=head.left_guard,
            elements=head.elements,
            right_guard=head.right_guard,
        )

        # constraint to enforce the guards of the original choice
        constraint = aggregate_constraint(body_aggregate, node.body)

        return [choice_rule, constraint]


class ChoiceElementNormalizer(Transformer):
    """
    Normalize choice heads.

    E.g. { l1 : L1 ; l2 : L2 } :- body. is turned into:
    { l1 : L1 } :- body, L1. and
    { l2 : L2 } :- body, L2.
    """

    def visit_Rule(self, node: AST) -> AST | list[AST]:  # pylint: disable=invalid-name
        """
        Transform choice rules.
        """
        head = node.head

        if not _is_choice(head):
            return node

        new_rules = []

        # construct a new rule for each element of the choice
        for elem in head.elements:
            # the new choice head
            choice = Aggregate(
                location=LOC,
                left_guard=None,
                elements=[elem],
                right_guard=None,
            )

            new_rules.append(
                Rule(
                    location=LOC,
                    head=choice,
                    body=node.body,
                )
            )

        return new_rules


class ChoiceConditionNormalizer(Transformer):
    """
    Normalize conditions in choice heads.

    E.g. { l : L } :- body. is turned into:
    { l } :- body, L.
    """

    def visit_Rule(self, node: AST) -> AST | list[AST]:  # pylint: disable=invalid-name
        """
        Transform choice rules.
        """
        head = node.head

        if not _is_choice(head):
            return node

        if len(head.elements) != 1:
            raise RuntimeError(f"Choice rule with unexpected number of elements {node}")

        element = head.elements[0]

        new_head = Aggregate(
            location=LOC,
            left_guard=None,
            elements=[element.literal],
            right_guard=None,
        )

        new_body = node.body
        for cond in element.condition:
            new_body.append(cond)

        return Rule(location=LOC, head=new_head, body=new_body)
