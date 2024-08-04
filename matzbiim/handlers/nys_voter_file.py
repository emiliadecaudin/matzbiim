"""
This module contains the Handler decorator factory.
"""

# --- Imports ------------------------------------------------------------------------ #

from datetime import datetime

from matzbiim.exceptions import SkipElement
from matzbiim.handlers.handler import Handler

# --- Constants ---------------------------------------------------------------------- #

nysboe_handler = Handler()

# --- Handler Functions -------------------------------------------------------------- #


@nysboe_handler("first_name")
@nysboe_handler("last_name")
def default(value: str) -> str:
    return value


@nysboe_handler("date_of_birth")
@nysboe_handler("last_voted_date")
@nysboe_handler("registration_date")
@nysboe_handler("inactive_date")
@nysboe_handler("purge_date")
def date(value: str) -> str:
    if value:
        return datetime.strptime(value, "%Y%m%d").strftime("%Y-%m-%d")
    else:
        return value


@nysboe_handler
def registration_status(value: str) -> str:
    if value == "P":
        raise SkipElement
    return value
