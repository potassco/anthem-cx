"""
The main entry point for the application.
"""

import sys
from copy import deepcopy

from . import assemble_and_execute, run_syntactic_checks
from .analysis.conflict import check_and_rename_auxiliaries, check_and_rename_privates, collect_ground_terms
from .eqt import (
    get_difference_constraint,
    get_difference_program,
    get_generate_program,
    get_public_reduct,
    normalize_program,
)
from .utils.data import Auxiliaries, Direction, Options, Programs, UniquenessData
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
    get_logger("main")

    inputs, outputs = parse_user_guide(args.user_guide)
    left = parse_program(args.left)
    right = parse_program(args.right)

    left, right = check_and_rename_privates(left, right, inputs | outputs)

    ground_terms = collect_ground_terms(left + right)

    auxiliaries = Auxiliaries.default()
    auxiliaries = check_and_rename_auxiliaries(left, right, inputs | outputs, auxiliaries, ground_terms)

    left_normalized = normalize_program(deepcopy(left))
    right_normalized = normalize_program(deepcopy(right))

    # collect all options
    opts = Options(
        direction=Direction.from_string(args.direction),
        out_dir=args.save_to_files,
        solve=not args.no_solve,
        start=args.start,
        max_size=args.max,
        gc=UniquenessData.from_string(args.uniqueness_check),
        inputs=inputs,
        outputs=outputs,
        clingo_args=clingo_args,
        auxiliaries=auxiliaries,
    )

    # run all syntactic checks
    # if we use any checks for uniqueness this will change opts.gc in place
    run_syntactic_checks(left_normalized, right_normalized, opts, inputs | outputs)

    assumptions = parse_program_as_str(args.assumptions) if args.assumptions else None

    # collect all program parts
    progs = Programs(
        left=left,
        right=right,
        generate=get_generate_program(opts.inputs, assumptions, opts.auxiliaries, ground_terms),
        difference=get_difference_program(opts.outputs, opts.auxiliaries),
        constraint=get_difference_constraint(bool(opts.gc.use_gc), opts.auxiliaries),
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

    counterexample = assemble_and_execute(progs, opts)

    # report the final result if solving
    if opts.solve:
        if counterexample:
            print(counterexample)
        else:
            print(f"No counterexample was found for the domain size max of {opts.max_size}")


if __name__ == "__main__":
    main()
