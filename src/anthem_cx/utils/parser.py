"""
The command line parser for the project.
"""

from argparse import ArgumentParser
from importlib import metadata
from textwrap import dedent
from typing import Any, Optional, cast

from . import logging

__all__ = ["get_parser"]

VERSION = metadata.version("anthem-cx")


def get_parser() -> ArgumentParser:
    """
    Return the parser for command line options.
    """
    parser = ArgumentParser(
        prog="anthem-cx",
        description=dedent(
            """\
            Find counterexamples to external equivalence problems
            """
        ),
    )
    levels = [
        ("error", logging.ERROR),
        ("warning", logging.WARNING),
        ("info", logging.INFO),
        ("debug", logging.DEBUG),
    ]

    def get(levels: list[tuple[str, int]], name: str) -> Optional[int]:
        for key, val in levels:
            if key == name:
                return val
        return None  # nocoverage

    parser.add_argument(
        "--log",
        default="warning",
        choices=[val for _, val in levels],
        metavar=f"{{{','.join(key for key, _ in levels)}}}",
        help="set the log level [%(default)s]",
        type=cast(Any, lambda name: get(levels, name)),
    )

    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {VERSION}")

    parser.add_argument(
        "--direction",
        "-d",
        type=str,
        choices=["universal", "forward", "backward"],
        default="universal",
        help="direction to find counterexamples in [%(default)s]",
    )

    parser.add_argument("--save-to-files", type=str, help="directory for saving the counterexample programs")

    parser.add_argument("--no-solve", "-n", action="store_true", help="disable solving the counterexample programs")

    parser.add_argument("--start", "-s", type=int, default=0, help="start value for the domain size [%(default)s]")

    parser.add_argument("--max", "-m", type=int, help="optional limit for the domain size")

    parser.add_argument(
        "--uniqueness-check",
        "-u",
        type=str,
        choices=["skip", "fail", "auto", "stratification", "local"],
        default="auto",
        help="control which uniqueness check is used [%(default)s]",
    )

    parser.add_argument("--assumptions", "-a", type=str, help="a file containing an assumption program")

    parser.add_argument("left", type=str, help="the left program")

    parser.add_argument("right", type=str, help="the right program")

    parser.add_argument("user_guide", metavar="user-guide", type=str, help="the user guide")

    return parser
