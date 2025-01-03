"""
This module contains the Handler decorator factory.
"""

# --- Imports ------------------------------------------------------------------------ #

from collections.abc import Callable
from typing import overload

# --- Constants ---------------------------------------------------------------------- #

HANDLER_ARGUMENT_TYPE = str
HANDLER_RETURN_TYPE = str
HANDLER_SIGNATURE = Callable[[HANDLER_ARGUMENT_TYPE], HANDLER_RETURN_TYPE]
META_HANDLER_SIGNATURE = Callable[[HANDLER_SIGNATURE], HANDLER_SIGNATURE]

# --- Class -------------------------------------------------------------------------- #


class Handler:
    """
    This class is a dectorator (factory) factory, representing a specific set of ways to
    transform data within a CSV file. Specifically, each handler maintains a list of
    functions that transform the data in a particular column.
    """

    _handlers: dict[str, HANDLER_SIGNATURE]
    """The list of column names and their associated functions."""

    def __init__(self) -> None:
        self._handlers = {}

    @overload
    def __call__(self, func: HANDLER_SIGNATURE) -> HANDLER_SIGNATURE: ...

    @overload
    def __call__(self, column: str) -> META_HANDLER_SIGNATURE: ...

    def __call__(
        self, *args, **kwargs
    ) -> HANDLER_SIGNATURE | META_HANDLER_SIGNATURE:
        if callable(func_or_column):
            func = func_or_column
            self._handlers[func.__name__] = func
            return func

        else:

            def decorator(func: HANDLER_SIGNATURE) -> HANDLER_SIGNATURE:
                column = func_or_column
                self._handlers[column] = func
                return func

            return decorator

    def handle(self, column: str, value: HANDLER_ARGUMENT_TYPE) -> HANDLER_RETURN_TYPE:
        if column not in self._handlers:
            raise NotImplementedError(f"No handler present for column `{column}`.")
        else:
            return self._handlers[column](value)
