"""Contains the PuzzleReader class for reading puzzle input and expected test results."""

# Built-in modules
from os import path as os_path
from pathlib import Path
from typing import Any

# Local modules
from utils.cli_args import Args
from utils.files import Files
from utils.output_handler import OutputHandler


class PuzzleReader:
    """Utility class for reading input data and expected test results for puzzle solutions."""

    @staticmethod
    def get_input(
        context: OutputHandler,
        args: Args,
        raw_input: bool,
        is_test: bool = False,
    ) -> list[str] | str | None:
        """
        Retrieve the input data for a specific year and day of the puzzle.

        Args:
            context (OutputHandler): The output handler for the current run of the program.
            args (Args): The parsed command-line arguments.
            raw_input (bool): If True, the raw input data will be returned as a single string. If False, the input data will be returned as a list of strings.
            is_test (bool, optional): If True, the test input data will be retrieved. Defaults to False.

        Returns:
            list[str] | str | None: The input data for the specified year and day of the puzzle.

        Raises:
            FileNotFoundError: If the file corresponding to the specified year and day does not exist.
        """
        file_name: str = (
            f"{args.day_str}_input.txt"
            if not is_test
            else f"{args.day_str}_test_input.txt"
        )

        file_path: Path = Path(
            Files.get_path(), "data", args.year_str, args.day_str, file_name
        )

        try:
            PuzzleReader.__is_valid_file(file_path)
        except (FileNotFoundError, ValueError) as e:
            context.print_error(str(e))
            return None

        with open(file_path, "r") as f:
            if raw_input:
                return f.read()
            else:
                return [line.strip("\n") for line in f.readlines()]

    @staticmethod
    def get_test_results(context: OutputHandler, args: Args, part: int) -> Any:
        """
        Retrieve the expected test results for a specific year, day, and part of the puzzle.

        Args:
            context (OutputHandler): The output handler for the current run of the program.
            args (Args): The parsed command-line arguments.
            part (int): The part of the puzzle for which the test results are being retrieved.

        Returns:
            Any: The expected test results for the specified year, day, and part of the puzzle.

        Raises:
            FileNotFoundError: If the file corresponding to the specified year, day, and part does not exist.
        """
        file_name: str = f"{args.day_str}_test_result_{part}.txt"

        folder_path: Path = Path(
            Files.get_path(),
            "data",
            args.year_str,
            args.day_str,
        )

        file_path: Path = Path(folder_path, file_name)
        try:
            PuzzleReader.__is_valid_file(file_path)
        except FileNotFoundError as e:
            context.print_error(f"{e}")
            exit(1)
        except ValueError as e:
            raise ValueError(e)

        result: Any = [line.strip("\n") for line in open(file_path, "r").readlines()]

        result = (
            [int(x) for x in result] if all(x.isdigit() for x in result) else result
        )

        # If the test result is a single value, return the single value
        if len(result) == 1:
            result = result[0]

        return result

    @staticmethod
    def __is_valid_file(file_path: Path) -> None:
        """
        Ensure that the specified file exists and is not empty.

        This method checks whether the file at the given path exists. If the file
        does not exist, a FileNotFoundError is raised. If the file exists but is
        empty, a ValueError is raised.

        Args:
            file_path (Path): The path to the file to be validated.

        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
            ValueError: If the file is empty.
        """
        relative_path: str = os_path.relpath(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: [cyan]{relative_path}[/cyan]")

        if file_path.stat().st_size == 0:
            raise ValueError(f"File is empty: [cyan]{relative_path}[/cyan]")
