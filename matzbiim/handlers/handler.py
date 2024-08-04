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

# --- Class -------------------------------------------------------------------------- #


class Handler:
    """
    This class is a dectorator (factory) factory, representing a specific set of ways to
    transform data within a CSV file. Specifically, each handler maintains a list of
    functions that transform the data in a particular column.
    """

    _handlers: list[tuple[str, HANDLER_SIGNATURE]]
    """The list of column names and their associated functions."""

    def __init__(self) -> None:
        self._handlers = []

    @overload
    def __call__(self, func_or_column: HANDLER_SIGNATURE) -> HANDLER_SIGNATURE: ...

    @overload
    def __call__(
        self, func_or_column: str
    ) -> Callable[[HANDLER_SIGNATURE], HANDLER_SIGNATURE]: ...

    @overload
    def __call__(self) -> Callable[[HANDLER_SIGNATURE], HANDLER_SIGNATURE]: ...

    def __call__(
        self, func_or_column: HANDLER_SIGNATURE | str | None = None
    ) -> HANDLER_SIGNATURE | Callable[[HANDLER_SIGNATURE], HANDLER_SIGNATURE]:
        if callable(func_or_column):
            func = func_or_column
            self._handlers.append((func.__name__, func))
            return func

        else:

            def decorator(func: HANDLER_SIGNATURE) -> HANDLER_SIGNATURE:
                self._handlers.append((func_or_column or func.__name__, func))
                return func

            return decorator
