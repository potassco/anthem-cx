"""
Module to transform a program into its public reduct.
"""

from clingo.ast import AST, ASTType, Function, Literal, Rule, Sign, SymbolicAtom, Transformer

from ..utils.data import Auxiliaries, Predicate
from ..utils.logging import get_logger
from ..utils.transformation import (
    LOC,
    atom_to_predicate,
    is_mapped_predicate,
    map_atom,
    unmap_atom,
)

log = get_logger(__name__)


class ReplacePositiveOutputPredicates(Transformer):
    """
    Replace all positive output predicates by their auxiliary version.
    """

    def __init__(self, outputs: set[Predicate], auxiliaries: Auxiliaries):
        super().__init__()
        self.outputs = outputs
        self.suffix = auxiliaries.suffix

    def visit_Literal(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Transform positive output literals.
        """
        atom = node.atom

        match atom.ast_type:
            case ASTType.BooleanConstant:
                # boolean constants are not changed
                return node

            case ASTType.Comparison:
                # comparisons are not changed
                return node

            case ASTType.Aggregate | ASTType.BodyAggregate:
                # transform the elements of aggregates
                new_elements = self.visit_sequence(atom.elements)
                atom.elements = new_elements

                return node

            case ASTType.SymbolicAtom:
                # change positive literals
                if node.sign == Sign.NoSign:
                    # get the predicate of the atom
                    predicate = atom_to_predicate(atom)

                    if predicate in self.outputs:
                        # change the predicate if it is an output predicate
                        new_atom = map_atom(atom, self.suffix)
                        new_literal = Literal(
                            location=LOC,
                            sign=Sign.NoSign,
                            atom=new_atom,
                        )
                        return new_literal

                return node

            case _:  # nocoverage
                log.warning("Unexpected atom type %s for literal %s", atom.ast_type, node)  # nocoverage
                return node  # nocoverage


class TransformRuleHeads(Transformer):
    """
    Transform rule heads.

    1. empty heads:
          :- body. is turned into
    unsat :- body.

    2. literal heads:
    unchanged

    3. choice heads:
    { l' } :- body.    with l output, is changed to
      l'   :- body, l.
    """

    def __init__(self, outputs: set[Predicate], auxiliaries: Auxiliaries):
        super().__init__()
        self.outputs = outputs
        self.unsat = auxiliaries.unsat
        self.suffix = auxiliaries.suffix

    def visit_Rule(self, node: AST) -> AST:  # pylint: disable=invalid-name
        """
        Transform choices and constraints into basic rules.
        """
        head = node.head

        # 1: empty head, i.e. empty disjunction or the literal #false
        if head.ast_type == ASTType.Disjunction or (
            head.ast_type == ASTType.Literal
            and head.atom.ast_type == ASTType.BooleanConstant
            and head.atom.value == False  # pylint: disable=singleton-comparison
        ):
            # the only type of disjunction should be the empty disjunction
            if head.ast_type == ASTType.Disjunction and len(head.elements) != 0:
                log.error("Unexpected disjunctive rule %s", node)
                raise RuntimeError(f"Unexpected disjunctive rule {node}")

            # new head is the unsat predicate
            unsat_head = Literal(
                location=LOC,
                sign=Sign.NoSign,
                atom=SymbolicAtom(
                    Function(
                        location=LOC,
                        name=self.unsat,
                        arguments=[],
                        external=False,
                    )
                ),
            )

            return Rule(location=LOC, head=unsat_head, body=node.body)

        # 2: head is a literal
        if head.ast_type == ASTType.Literal:
            return node

        # 3: choice rule
        if head.ast_type == ASTType.Aggregate and len(head.elements) == 1:
            # the choice rue should contain exactly one element and no guards
            if len(head.elements) != 1:  # nocoverage
                log.error("Unexpected choice rule with multiple elements %s", node)
                raise RuntimeError(f"Unexpected choice rule with multiple elements {node}")
            if head.left_guard is not None or head.right_guard is not None:  # nocoverage
                log.error("Unexpected choice rule with guards %s", node)
                raise RuntimeError(f"Unexpected choice rule with guards {node}")

            element = head.elements[0]
            if element.ast_type == ASTType.ConditionalLiteral:
                literal = element.literal
            else:
                literal = element  # nocoverage

            if literal.sign != Sign.NoSign:
                log.warning("Unexpected negation in choice head %s", node)
                return node

            atom = literal.atom
            # check if the choice atom is a mapped predicate (i.e. was originally an output predicate)
            if is_mapped_predicate(atom, self.suffix):
                # add the original predicate as a positive literal to the body
                new_body = node.body
                original_atom = unmap_atom(atom, self.suffix)
                original_literal = Literal(
                    location=LOC,
                    sign=Sign.DoubleNegation,
                    atom=original_atom,
                )
                new_body.append(original_literal)

                # the head of the new rule is the choice atom
                new_rule = Rule(
                    location=LOC,
                    head=Literal(location=LOC, sign=Sign.NoSign, atom=atom),
                    body=new_body,
                )

                return new_rule

            return node

        log.warning("Unexpected rule head %s", node)
        return node
