"""
This module contains the Handler decorator factory.
"""

# --- Imports ------------------------------------------------------------------------ #

from matzbiim.handlers.handler import Handler

# --- Constants ---------------------------------------------------------------------- #

nysboe_handler = Handler()

# --- Handler Functions -------------------------------------------------------------- #


@nysboe_handler("last_name")
def last_name(value: str) -> str:
    return value


@nysboe_handler
def first_name(value: str) -> str:
    return value
