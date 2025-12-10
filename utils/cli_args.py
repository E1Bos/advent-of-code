"""Module for handling command line arguments."""

from dataclasses import dataclass


@dataclass
class Args:
    """
    Class for handling command line arguments.

    Attributes:
        year (int): The year of the puzzle.
        day (int): The day of the puzzle.
        part (int): The part of the puzzle to solve.
        copy_result (bool): Whether to copy the result to the clipboard.
        run_all (bool): Whether to run all parts of the puzzle.
        only_test (bool): Whether to only run the tests.
        skip_test (bool): Whether to skip the tests.
        create (bool): Whether to create the necessary files for the specified year and day.
        timeit (bool): Whether to time the execution of the solution.
        profile (bool): Whether to profile the execution of the solution.
        quality (bool): Whether to run code quality checks before the solution.
        debug (bool): Whether to run the solution in debug mode.

    Properties:
        year_str (str): The year as a string.
        day_str (str): The day as a string with 2 digits
    """

    year: int
    day: int
    part: int = 1
    copy_result: bool = False
    run_all: bool = False
    only_test: bool = False
    skip_test: bool = False
    create: bool = False
    timeit: bool = False
    profile: bool = False
    quality: bool = False
    debug: bool = False

    @property
    def year_str(self) -> str:
        """Return the year as a string."""
        return str(self.year)

    @property
    def day_str(self) -> str:
        """Return the day as a string with 2 digits."""
        return str(self.day).zfill(2)
