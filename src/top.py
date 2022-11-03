""" Program in order to create a 'top' command implemented in Python. """

# needed imports
import schedule
import psutil
from datetime import datetime
import pandas as pd
import os
import typer


def upper_diagnostics():
    """Function to calculate all 'upper' diagnostics."""
    pass


def process_stats():
    """Function to calculate order of processes in top command."""
    pass


def top(interactMode):
    """Function to compile all diagnostic information into a organized display."""

    pass


def main(
    nonInteract: bool = typer.Option(
        None,
        "--non-interactive",
        help="if you want the program to run only one time or iteratively.",
    )
):
    if nonInteract is not None:
        # if they want to run it more than once:
        top(nonInteract)
    else:
        # run normally through schedule
        top(nonInteract)


if __name__ == "__main__":
    main()
