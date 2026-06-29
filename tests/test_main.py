"""
Test cases for main application functionality.
"""

import os
import sys
import tempfile
from contextlib import redirect_stderr
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from anthem_cx.__main__ import main
from anthem_cx.utils import logging
from anthem_cx.utils.parser import get_parser


class TestMain(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_parser(self) -> None:
        """
        Test the parser.
        """
        parser = get_parser()
        ret = parser.parse_args(["--log", "info", "left", "right", "user_guide"])
        self.assertEqual(ret.log, logging.INFO)

    def test_reports_anthem_cx_error_cleanly(self) -> None:
        """
        A user-facing error exits with code 1 and a clean message (no traceback).
        """
        fd, guide = tempfile.mkstemp(suffix=".ug")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("input: a/0.\noutput: b/0.\n")

        argv = ["anthem-cx", "/nonexistent/left.lp", "/nonexistent/right.lp", guide]
        try:
            with (
                patch.object(sys, "argv", argv),
                redirect_stderr(StringIO()),
                self.assertRaises(SystemExit) as cm,
            ):
                main()
        finally:
            os.unlink(guide)

        # the AnthemCXError is caught and turned into a clean exit, not a traceback
        self.assertEqual(cm.exception.code, 1)
