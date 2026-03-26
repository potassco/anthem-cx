"""
The main entry point for the application.
"""

import sys

from . import assemble_and_execute
from .eqt import get_difference_program, get_generate_program, get_public_reduct, normalize_program
from .utils import Direction, Options, Programs
from .utils.dependency import has_enough_visible_atoms, has_recursive_aggregates
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
    args = parser.parse_args()

    # logging
    configure_logging(sys.stderr, args.log, sys.stderr.isatty())
    log = get_logger("main")

    left_normalized = normalize_program(parse_program(args.left))
    right_normalized = normalize_program(parse_program(args.right))

    if has_recursive_aggregates(left_normalized) or has_recursive_aggregates(right_normalized):
        raise RuntimeError("Recursive aggregates are not supported.")

    # collect all options
    inputs, outputs = parse_user_guide(args.user_guide)
    opts = Options(
        direction=Direction.from_string(args.direction),
        out_dir=args.save_to_files,
        solve=not args.no_solve,
        start=args.start,
        max_size=args.max,
        # use_gc could be directional, i.e. use_gc_forward and use_gc_backward
        use_gc=(
            not (
                has_enough_visible_atoms(left_normalized, inputs | outputs)
                and has_enough_visible_atoms(right_normalized, inputs | outputs)
            )
            if args.guess_and_check is None
            else args.guess_and_check
        ),
        inputs=inputs,
        outputs=outputs,
    )

    if args.guess_and_check is None:
        if opts.use_gc:
            log.warning("EVA condition could not be verified, using guess and check transformation.")
        else:
            log.info("EVA condition was verified.")

    assumptions = parse_program_as_str(args.assumptions) if args.assumptions else None

    # collect all program parts
    progs = Programs(
        left=parse_program(args.left),
        right=parse_program(args.right),
        generate=get_generate_program(opts.inputs, assumptions),
        difference=get_difference_program(opts.outputs, opts.use_gc),
        public_reduct_left=(
            get_public_reduct(left_normalized, opts.outputs) if opts.direction.includes_backward() else None
        ),
        public_reduct_right=(
            get_public_reduct(right_normalized, opts.outputs) if opts.direction.includes_forward() else None
        ),
    )

    assemble_and_execute(progs, opts)


if __name__ == "__main__":
    main()
