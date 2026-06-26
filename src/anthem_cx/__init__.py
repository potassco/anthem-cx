"""
The anthem_cx project.
"""

from clingo.ast import AST

from .analysis.dependency import has_negative_cycle, has_odd_negative_cycle, has_recursive_aggregates
from .utils.data import Counterexample, Options, Predicate, Programs, UniquenessCheck, UniquenessVerdict
from .utils.errors import AnthemCXError
from .utils.logging import get_logger
from .utils.output import build_cx_program, build_cx_program_gc, save_cx_program_gc_to_file, save_cx_program_to_file
from .utils.solving import solve_for_counterexample, solve_gc_for_counterexample

log = get_logger(__name__)


def reject_recursive_aggregates(left: list[AST], right: list[AST]) -> None:
    """
    Reject programs containing recursive aggregates, which are not supported.
    """
    if has_recursive_aggregates(left) or has_recursive_aggregates(right):
        raise AnthemCXError("recursive aggregates are not supported")


def determine_uniqueness(
    left: list[AST], right: list[AST], public_predicates: set[Predicate], check: UniquenessCheck
) -> UniquenessVerdict:
    """
    Decide how to solve the counterexample program based on the selected uniqueness check.

    Returns:
        UniquenessVerdict: solve directly, use guess-and-check, or defer to local check
    """
    match check:
        case UniquenessCheck.SKIP:
            return UniquenessVerdict.DIRECT
        case UniquenessCheck.FAIL:
            return UniquenessVerdict.GUESS_CHECK
        case UniquenessCheck.STRATIFICATION:
            return _stratification_verdict(left, right, public_predicates)
        case UniquenessCheck.LOCAL:
            return _local_precondition_verdict(left, right, public_predicates)
        case UniquenessCheck.AUTO:
            if _is_stratified(left, right, public_predicates):
                return UniquenessVerdict.DIRECT
            return _local_precondition_verdict(left, right, public_predicates)


def _is_stratified(left: list[AST], right: list[AST], public_predicates: set[Predicate]) -> bool:
    """Check whether both programs are stratified (no negative cycle), with logging."""
    if has_negative_cycle(left, public_predicates):
        log.info("Stratification check for left program failed (skip checking right)")
        return False
    if has_negative_cycle(right, public_predicates):
        log.info("Stratification check for right program failed")
        return False
    log.info("Stratification check for both programs succeeded")
    return True


def _stratification_verdict(left: list[AST], right: list[AST], public_predicates: set[Predicate]) -> UniquenessVerdict:
    """Stratification decides directly: solve directly if stratified, otherwise guess-and-check."""
    if _is_stratified(left, right, public_predicates):
        return UniquenessVerdict.DIRECT
    return UniquenessVerdict.GUESS_CHECK


def _local_precondition_verdict(
    left: list[AST], right: list[AST], public_predicates: set[Predicate]
) -> UniquenessVerdict:
    """
    Check the local uniqueness precondition (no odd negative cycle).

    A failed precondition forces guess and check; otherwise the decision is deferred until a
    potential counterexample is found and the local check can be run on it.
    """
    if has_odd_negative_cycle(left, public_predicates):
        log.info("Local uniqueness precondition for left program failed (skip checking right)")
        return UniquenessVerdict.GUESS_CHECK
    if has_odd_negative_cycle(right, public_predicates):
        log.info("Local uniqueness precondition for right program failed")
        return UniquenessVerdict.GUESS_CHECK
    log.info("Local uniqueness precondition for both programs succeeded")
    return UniquenessVerdict.NEEDS_LOCAL_CHECK


def assemble_and_execute(programs: Programs, options: Options, verdict: UniquenessVerdict) -> Counterexample | None:
    """
    Assemble the counterexample program from its components and execute/output it.

    Returns the counterexample if solving is enabled and one is found, otherwise None.
    """
    if verdict.uses_gc():
        log.info("Using the guess and check approach")
        return _assemble_and_execute_gc(programs, options)

    return _assemble_and_execute(programs, options)


def _assemble_and_execute(programs: Programs, options: Options) -> Counterexample | None:
    forward = None
    backward = None
    if options.direction.includes_forward():
        forward = build_cx_program(
            programs.generate,
            programs.left,
            programs.public_reduct_right,  # type: ignore
            programs.difference,
            programs.constraint,
        )
    if options.direction.includes_backward():
        backward = build_cx_program(
            programs.generate,
            programs.right,
            programs.public_reduct_left,  # type: ignore
            programs.difference,
            programs.constraint,
            False,
        )

    if options.solve:
        return solve_for_counterexample(
            forward,
            backward,
            options.inputs,
            options.outputs,
            options.start,
            options.max_size,
            options.clingo_args,
            options.auxiliaries.size,
        )

    if options.out_dir:
        save_cx_program_to_file(forward, options.out_dir)
        save_cx_program_to_file(backward, options.out_dir, False)
    else:
        if forward:
            print(f"{forward}\n")
        if backward:
            print(f"{backward}\n")

    return None


def _assemble_and_execute_gc(programs: Programs, options: Options) -> Counterexample | None:
    forward_guess, forward_check = None, None
    backward_guess, backward_check = None, None
    if options.direction.includes_forward():
        forward_guess, forward_check = build_cx_program_gc(
            programs.generate,
            programs.left,
            programs.public_reduct_right,  # type: ignore
            programs.difference,
            programs.constraint,
        )
    if options.direction.includes_backward():
        backward_guess, backward_check = build_cx_program_gc(
            programs.generate,
            programs.right,
            programs.public_reduct_left,  # type: ignore
            programs.difference,
            programs.constraint,
            False,
        )

    if options.solve:
        return solve_gc_for_counterexample(
            forward_guess,
            forward_check,
            backward_guess,
            backward_check,
            options.inputs,
            options.outputs,
            options.start,
            options.max_size,
            options.clingo_args,
            options.auxiliaries.size,
        )

    if options.out_dir:
        save_cx_program_gc_to_file(forward_guess, forward_check, options.out_dir)
        save_cx_program_gc_to_file(backward_guess, backward_check, options.out_dir, False)
    else:
        if forward_guess and forward_check:
            print(f"{forward_guess}\n")
            print(f"{forward_check}\n")
        if backward_guess and backward_check:
            print(f"{backward_guess}\n")
            print(f"{backward_check}\n")

    return None
