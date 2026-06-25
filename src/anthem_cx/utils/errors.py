"""
Project-specific exception types.
"""


class AnthemCXError(Exception):
    """
    An expected, user-facing error such as unsupported input or an invalid program.

    These are reported to the user as a clean error message (without a traceback);
    they are caught at the top level in ``__main__``. Internal invariant violations
    (i.e. conditions that can only arise from a bug) should keep raising a plain
    exception such as ``RuntimeError`` so that they surface with a full traceback.
    """
