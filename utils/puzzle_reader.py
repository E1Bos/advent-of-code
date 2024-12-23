import os
import sys
from pathlib import Path
from typing import Any
from rich.console import Console

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
from utils.files import Files


class PuzzleReader:
    console = Console()

    @staticmethod
    def get_input(
        year: int, day: int, raw_input: bool, is_test: bool = False
    ) -> list[str] | str | None:
        """
        Retrieves the input data for a specific year and day of the puzzle.

        Args:
            year (int): The year of the puzzle, formatted as YYYY.
            day (int): The day of the puzzle.
            raw_input (bool): If True, the raw input data will be returned as a single string. If False, the input data will be returned as a list of strings.
            is_test (bool, optional): If True, the test input data will be retrieved. Defaults to False.

        Returns:
            list[str] | str | None: The input data for the specified year and day of the puzzle.

        Raises:
            FileNotFoundError: If the file corresponding to the specified year and day does not exist.
        """
        file_name: str = (
            f"{day:02d}_input.txt" if not is_test else f"{day:02d}_test_input.txt"
        )

        file_path: Path = Path(
            Files.get_path(), "data", f"{year:04d}", f"{day:02d}", file_name
        )

        try:
            PuzzleReader.__is_valid_file(file_path)
        except (FileNotFoundError, ValueError) as e:
            (
                PuzzleReader.console.print(f"[on red] ERROR [/on red] {e}")
                if not is_test
                else PuzzleReader.console.print(f"[on yellow] WARNING [/on yellow] {e}")
            )
            return None

        with open(file_path, "r") as f:
            if raw_input:
                return f.read()
            else:
                return [line.strip("\n") for line in f.readlines()]

        return None

    @staticmethod
    def get_test_results(year: int, day: int, part: int) -> Any:
        """
        Retrieves the expected test results for a specific year, day, and part of the puzzle.

        Args:
            year (int): The year of the puzzle, formatted as YYYY.
            day (int): The day of the puzzle.
            part (int): The part of the puzzle for which the test results are being retrieved.

        Returns:
            Any: The expected test results for the specified year, day, and part of the puzzle.

        Raises:
            FileNotFoundError: If the file corresponding to the specified year, day, and part does not exist.
        """
        file_name: str = f"{day:02d}_test_result_{part}.txt"

        folder_path: Path = Path(
            Files.get_path(),
            "data",
            f"{year:04d}",
            f"{day:02d}",
        )

        file_path: Path = Path(folder_path, file_name)
        try:
            PuzzleReader.__is_valid_file(file_path)
        except FileNotFoundError as e:
            PuzzleReader.console.print(f"[on red] ERROR [/on red] {e}")
            exit(1)
        except ValueError as e:
            PuzzleReader.console.print(f"[on yellow] WARNING [/on yellow] {e}")
            return None

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
        relative_path: str = os.path.relpath(file_path)
        
        if not file_path.exists:
            raise FileNotFoundError(f"File not found: [cyan]{relative_path}[/cyan]")

        if file_path.stat().st_size == 0:
            raise ValueError(f"File is empty: [cyan]{relative_path}[/cyan]. [yellow bold]Skipping...[/yellow bold]")
