"""
This module contains the Handler decorator factory.
"""

# --- Imports ------------------------------------------------------------------------ #

from matzbiim.handlers.handler import Handler

# --- Constants ---------------------------------------------------------------------- #

nysboe_handler = Handler()

# --- Handler Functions -------------------------------------------------------------- #


@nysboe_handler("first_name")
@nysboe_handler("last_name")
def default(value: str) -> str:
    return value
