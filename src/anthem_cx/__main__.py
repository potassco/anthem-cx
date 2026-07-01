"""
The main entry point for the application.
"""

import sys
from argparse import Namespace
from copy import deepcopy

from . import assemble_and_execute, determine_uniqueness, reject_recursive_aggregates
from .analysis.assumptions import check_assumptions
from .analysis.conflict import check_and_rename_auxiliaries, check_and_rename_privates, collect_ground_terms
from .analysis.inputs import check_inputs_not_in_heads
from .analysis.local import is_locally_unique
from .cx_program import (
    get_difference_constraint,
    get_difference_program,
    get_generate_program,
    get_public_reduct,
    normalize_program,
)
from .utils.data import Auxiliaries, Direction, Options, Programs, UniquenessCheck, UniquenessVerdict
from .utils.errors import AnthemCXError
from .utils.logging import configure_logging, get_logger
from .utils.output import program_to_str
from .utils.parse_program import parse_program
from .utils.parse_user_guide import parse_user_guide
from .utils.parser import get_parser


def main() -> None:
    """
    Run the main function.
    """
    # argument parser
    parser = get_parser()
    args, clingo_args = parser.parse_known_args()

    # logging
    configure_logging(sys.stderr, args.log, sys.stderr.isatty())
    log = get_logger("main")

    try:
        _run(args, clingo_args)
    except AnthemCXError as e:
        # expected, user-facing errors are reported without a traceback
        log.error("%s", e)
        sys.exit(1)


def _run(args: Namespace, clingo_args: list[str]) -> None:
    """
    Run the counterexample search for the parsed command line arguments.
    """
    log = get_logger("main")

    inputs, outputs = parse_user_guide(args.user_guide)
    left = parse_program(args.left)
    right = parse_program(args.right)

    left, right = check_and_rename_privates(left, right, inputs | outputs)

    ground_terms = collect_ground_terms(left + right)

    # constants from the programs are added to the input domain unless disabled
    domain_constants = set() if args.no_program_constants else ground_terms
    if not args.no_program_constants:
        log.info(
            "Collected %s domain constant(s) from the programs: %s",
            len(ground_terms),
            ", ".join(sorted(ground_terms)) or "none",
        )

    auxiliaries = Auxiliaries.default()
    auxiliaries = check_and_rename_auxiliaries(left, right, inputs | outputs, auxiliaries, ground_terms)

    left_normalized = normalize_program(deepcopy(left))
    right_normalized = normalize_program(deepcopy(right))

    # input predicates must not occur in the rule heads of the normalized programs
    check_inputs_not_in_heads(left_normalized, right_normalized, inputs)

    # collect all options
    opts = Options(
        direction=Direction.from_string(args.direction),
        out_dir=args.save_to_files,
        solve=not args.no_solve,
        start=args.start,
        max_size=args.max,
        uniqueness=UniquenessCheck.from_string(args.uniqueness_check),
        inputs=inputs,
        outputs=outputs,
        clingo_args=clingo_args,
        auxiliaries=auxiliaries,
    )

    # recursive aggregates are unsupported
    reject_recursive_aggregates(left_normalized, right_normalized)

    # decide how to solve based on the selected uniqueness check
    verdict = determine_uniqueness(left_normalized, right_normalized, inputs | outputs, opts.uniqueness)

    assumptions = None
    if args.assumptions:
        assumption_program = check_assumptions(
            parse_program(args.assumptions), inputs, outputs, left, right, opts.auxiliaries
        )
        assumptions = program_to_str(assumption_program, newline=True)

    # collect all program parts
    progs = Programs(
        left=left,
        right=right,
        generate=get_generate_program(opts.inputs, assumptions, opts.auxiliaries, domain_constants),
        difference=get_difference_program(opts.outputs, opts.auxiliaries),
        constraint=get_difference_constraint(verdict.uses_gc(), opts.auxiliaries),
        public_reduct_left=(
            get_public_reduct(left_normalized, opts.outputs, opts.auxiliaries)
            if opts.direction.includes_backward()
            else None
        ),
        public_reduct_right=(
            get_public_reduct(right_normalized, opts.outputs, opts.auxiliaries)
            if opts.direction.includes_forward()
            else None
        ),
    )

    counterexample = assemble_and_execute(progs, opts, verdict)

    if counterexample and verdict is UniquenessVerdict.NEEDS_LOCAL_CHECK:
        log.info(
            "Found a potential counterexample of size %s in the %s direction",
            counterexample.size,
            counterexample.direction,
        )
        log.info(counterexample)

        # run local uniqueness checks on the public reduct
        # the reduct for the counterexample's direction is guaranteed to exist
        if counterexample.is_forward:
            assert progs.public_reduct_right is not None
            if not is_locally_unique(progs.public_reduct_right, counterexample):
                log.info("Local uniqueness check for right program failed")
                verdict = UniquenessVerdict.GUESS_CHECK
        else:
            assert progs.public_reduct_left is not None
            if not is_locally_unique(progs.public_reduct_left, counterexample):
                log.info("Local uniqueness check for left program failed")
                verdict = UniquenessVerdict.GUESS_CHECK

        # solve gc program if required
        if verdict.uses_gc():
            progs.constraint = get_difference_constraint(True, opts.auxiliaries)
            counterexample = assemble_and_execute(progs, opts, verdict)
        else:
            log.info("Local uniqueness check succeeded")

    # report the final result if solving
    if opts.solve:
        if counterexample:
            print(f"Found a counterexample of size {counterexample.size} in the {counterexample.direction} direction")
            print(counterexample)
        else:
            print(f"No counterexample was found for the domain size max of {opts.max_size}")


if __name__ == "__main__":
    main()
