"""
The main entry point for the application.
"""

import sys
from copy import deepcopy

from . import assemble_and_execute
from .analysis.conflict import check_and_rename_auxiliaries, check_and_rename_privates
from .analysis.dependency import has_enough_visible_atoms, has_recursive_aggregates
from .eqt import get_difference_program, get_generate_program, get_public_reduct, normalize_program
from .utils import Auxiliaries, Direction, EVAData, Options, Programs
from .utils.logging import configure_logging, get_logger
from .utils.parse_program import parse_program, parse_program_as_str
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

    inputs, outputs = parse_user_guide(args.user_guide)
    left = parse_program(args.left)
    right = parse_program(args.right)

    left, right = check_and_rename_privates(left, right, inputs | outputs)

    auxiliaries = Auxiliaries.default()
    auxiliaries = check_and_rename_auxiliaries(left, right, inputs | outputs, auxiliaries)

    left_normalized = normalize_program(deepcopy(left))
    right_normalized = normalize_program(deepcopy(right))

    if has_recursive_aggregates(left_normalized) or has_recursive_aggregates(right_normalized):
        raise RuntimeError("Recursive aggregates are not supported.")

    # collect all options
    opts = Options(
        direction=Direction.from_string(args.direction),
        out_dir=args.save_to_files,
        solve=not args.no_solve,
        start=args.start,
        max_size=args.max,
        eva=EVAData.from_string(args.uniqueness_check),
        inputs=inputs,
        outputs=outputs,
        clingo_args=clingo_args,
        auxiliaries=auxiliaries,
    )

    if opts.eva.use_gc is None and opts.eva.use_syntax:
        if not has_enough_visible_atoms(left_normalized, inputs | outputs):
            log.info("Stratification check for left program failed (skip checking right)")
            opts.eva.syntax_failure()
        elif not has_enough_visible_atoms(right_normalized, inputs | outputs):
            log.info("Stratification check for right program failed")
            opts.eva.syntax_failure()
        else:
            log.info("Stratification check for both program succeeded")
            opts.eva.success()

    assumptions = parse_program_as_str(args.assumptions) if args.assumptions else None

    # collect all program parts
    progs = Programs(
        left=left,
        right=right,
        generate=get_generate_program(opts.inputs, assumptions, opts.auxiliaries, ground_terms),
        difference=get_difference_program(opts.outputs, bool(opts.eva.use_gc), opts.auxiliaries),
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

    assemble_and_execute(progs, opts)


if __name__ == "__main__":
    main()
