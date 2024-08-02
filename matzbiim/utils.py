"""
This module for is for "one-off" utils that don't fit in their own module.
"""

# --- Imports ------------------------------------------------------------------------ #

import contextlib
from glob import glob

import inquirer

# --- Functions ---------------------------------------------------------------------- #


def find_and_select_file(prefix: str) -> str | None:
    """
    This method searches ./data for any files beginning with the prefix
    `prefix`, prompts the user to select one of those files, and then returns
    the selected path.

    Returns
    -------
    string
        A relative path to the selected file.
    None
        If no such files were found.
    """

    matching_files = glob(pathname=f"{prefix}*", root_dir="./data")

    if len(matching_files) == 0:
        print(
            f"No files matching '{prefix}*' found in ./data. Are you sure you're in the root of the project directory?"
        )

    else:
        with contextlib.suppress(KeyboardInterrupt):
            file = inquirer.list_input(
                "Please select which file you would like to use", choices=matching_files
            )

            if isinstance(file, str):
                return "./data/" + file

    return None
