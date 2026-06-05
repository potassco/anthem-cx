"""
The anthem_cx project.
"""

from .utils.data import Counterexample, Options, Programs
from .utils.logging import get_logger
from .utils.output import build_eqt, build_eqt_gc, save_eqt_gc_to_file, save_eqt_to_file
from .utils.solving import solve_for_counterexample, solve_gc_for_counterexample

log = get_logger(__name__)


def assemble_and_execute(programs: Programs, options: Options) -> Counterexample | None:
    """
    Assemble the counterexample program from its components and execute/output it.

    Returns the counterexample if solving is enabled and one is found, otherwise None.
    """
    if options.eva.use_gc:
        return _assemble_and_execute_gc(programs, options)

    return _assemble_and_execute(programs, options)


def _assemble_and_execute(programs: Programs, options: Options) -> Counterexample | None:
    forward = None
    backward = None
    if options.direction.includes_forward():
        forward = build_eqt(
            programs.generate,
            programs.left,
            programs.public_reduct_right,  # type: ignore
            programs.difference,
            programs.constraint,
        )
    if options.direction.includes_backward():
        backward = build_eqt(
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
        save_eqt_to_file(forward, options.out_dir)
        save_eqt_to_file(backward, options.out_dir, False)
    else:
        print(f"{forward}\n")
        print(f"{backward}\n")

    return None


def _assemble_and_execute_gc(programs: Programs, options: Options) -> Counterexample | None:
    forward_guess, forward_check = None, None
    backward_guess, backward_check = None, None
    if options.direction.includes_forward():
        forward_guess, forward_check = build_eqt_gc(
            programs.generate,
            programs.left,
            programs.public_reduct_right,  # type: ignore
            programs.difference,
            programs.constraint,
        )
    if options.direction.includes_backward():
        backward_guess, backward_check = build_eqt_gc(
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
        save_eqt_gc_to_file(forward_guess, forward_check, options.out_dir)
        save_eqt_gc_to_file(backward_guess, backward_check, options.out_dir, False)
    else:
        print(f"{forward_guess}\n")
        print(f"{forward_check}\n")
        print(f"{backward_guess}\n")
        print(f"{backward_check}\n")

    return None
