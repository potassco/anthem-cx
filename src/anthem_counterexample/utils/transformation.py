"""
Module containing utilities for transformations.
"""

from typing import Sequence

from clingo.ast import (
    AST,
    Aggregate,
    ASTType,
    Disjunction,
    Function,
    Literal,
    Location,
    Pool,
    Position,
    Rule,
    Sign,
    SymbolicAtom,
    Transformer,
)

from . import Predicate
from .logging import get_logger

log = get_logger(__name__)

PREDICATE_SUFFIX = "__"
UNSAT_PREDICATE = "__unsat"
DIFF_PREDICATE = "__diff"
DOMAIN_PREDICATE = "__dom"

LOC = Location(Position("<string>", 1, 1), Position("<string>", 1, 1))


def apply_transformer(transformer: Transformer, prog: list[AST]) -> list[AST]:
    """
    Apply a transformer to a logic program.
    """
    ret = []
    for n in prog:
        x = transformer(n)
        if isinstance(x, list):
            ret.extend(x)
        else:
            ret.append(x)

    return ret


def atom_to_predicate(atom: AST) -> Predicate:
    """
    Get the predicate of an atom.
    """
    if atom.ast_type is not ASTType.SymbolicAtom:
        raise RuntimeError(f"Argument is not a symbolic atom {atom}")

    fun = atom.symbol

    if fun.ast_type is not ASTType.Function:
        if fun.ast_type == ASTType.Pool:
            fun = fun.arguments[0]
        else:
            raise RuntimeError(f"Unexpected symbolic atom whose symbol is not a function or pool {atom}")

    return Predicate(fun.name, len(fun.arguments))


def map_atom(atom: AST) -> AST:
    """
    Map an atom to its auxiliary version.
    """
    if atom.ast_type is not ASTType.SymbolicAtom:
        raise RuntimeError(f"Argument is not a symbolic atom {atom}")

    term = atom.symbol

    match term.ast_type:
        case ASTType.Function:
            new_atom = SymbolicAtom(symbol=_map_function(term))
            return new_atom
        case ASTType.Pool:
            new_arguments = []
            for arg in term.arguments:
                new_arguments.append(_map_function(arg))
            new_atom = SymbolicAtom(symbol=Pool(location=LOC, arguments=new_arguments))
            return new_atom
        case _:
            log.error("term %s with unexpected type %s", term, term.ast_type)

    return atom


def _map_function(function: AST) -> AST:
    if function.ast_type is not ASTType.Function:
        raise RuntimeError(f"Argument is not a function {function}")

    new_name = function.name + PREDICATE_SUFFIX
    new_function = Function(
        location=function.location,
        name=new_name,
        arguments=function.arguments,
        external=function.external,
    )

    return new_function


def _unmap_function(function: AST) -> AST:
    if function.ast_type is not ASTType.Function:
        raise RuntimeError(f"Argument is not a function {function}")

    return Function(
        location=function.location,
        name=function.name.removesuffix(PREDICATE_SUFFIX),
        arguments=function.arguments,
        external=function.external,
    )


def unmap_atom(atom: AST) -> AST:
    """
    Undo the mapping of a predicate to its auxiliary version.
    """
    if atom.ast_type is not ASTType.SymbolicAtom:
        raise RuntimeError(f"Argument is not a symbolic atom {atom}")

    term = atom.symbol

    match term.ast_type:
        case ASTType.Function:
            return SymbolicAtom(symbol=_unmap_function(term))
        case ASTType.Pool:
            new_arguments = []
            for arg in term.arguments:
                new_arguments.append(_unmap_function(arg))
            return SymbolicAtom(symbol=Pool(location=LOC, arguments=new_arguments))
        case _:
            raise RuntimeError(f"Term of atom is not a function or pool: {atom}")


def is_mapped_predicate(atom: AST) -> bool:
    """
    Check whether an atom contains an auxiliary predicate.
    """
    if atom.ast_type is not ASTType.SymbolicAtom:
        raise RuntimeError(f"Argument is not a symbolic atom {atom}")

    term = atom.symbol

    match term.ast_type:
        case ASTType.Function:
            name: str = term.name
            return name.endswith(PREDICATE_SUFFIX)
        case ASTType.Pool:
            function = term.arguments[0]
            name = function.name
            return name.endswith(PREDICATE_SUFFIX)
        case _:
            log.error("term %s with unexpected type %s", term, term.ast_type)

    return False


def choice_rule_for_elements(elements: Sequence[AST], body: Sequence[AST]) -> AST:
    """
    Get a choice rule for the conditions of elements.
    """
    choice_elements = []
    for elem in elements:
        choice_elements.append(elem.condition)

    choice_head = Aggregate(
        location=LOC,
        left_guard=None,
        right_guard=None,
        elements=choice_elements,
    )

    choice_rule = Rule(location=LOC, head=choice_head, body=body)

    return choice_rule


def aggregate_constraint(aggregate: AST, body: Sequence[AST]) -> AST:
    """
    Turn a body B and aggregate A into the constraint :- B, not A.
    """
    if aggregate.ast_type not in [ASTType.Aggregate, ASTType.BodyAggregate]:
        raise RuntimeError(f"Argument is not an aggregate {aggregate}")

    constraint_body = list(body)
    constraint_body.append(
        Literal(
            location=LOC,
            sign=Sign.Negation,
            atom=aggregate,
        )
    )

    constraint = Rule(
        location=LOC,
        head=Disjunction(location=LOC, elements=[]),
        body=constraint_body,
    )

    return constraint
