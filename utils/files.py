from pathlib import Path
from rich.console import Console


class Files:
    console = Console()

    @staticmethod
    def create_day(year: int, day: int, ok_if_exists: bool = False) -> None:
        """
        Creates the necessary files and directories for a new day's puzzle.

        Args:
            year (int): The year of the puzzle.
            day (int): The day of the puzzle.
            ok_if_exists (bool, optional): If True, will overwrite the file if it already exists. Defaults to False.

        Raises:
            ValueError: If year is not a 4-digit number.
        """
        path: Path = Files.get_path()
        year_str: str = str(year)
        day_str: str = f"{day:02}"

        if len(year_str) != 4:
            raise ValueError("Year must be a 4-digit number, formatted as YYYY")

        if not Path("data").exists():
            Path("data").mkdir(parents=True, exist_ok=True)
        if not Path("solutions").exists():
            Path("solutions").mkdir(parents=True, exist_ok=True)

        data_folder: Path = Path(path, "data", year_str)
        solution_folder: Path = Path(path, "solutions", year_str)

        if not data_folder.exists():
            data_folder.mkdir(parents=True, exist_ok=True)
        if not solution_folder.exists():
            solution_folder.mkdir(parents=True, exist_ok=True)

        # Create the Data
        file_names: list[str] = [
            f"{day_str}_input.txt",
            f"{day_str}_test_input.txt",
            f"{day_str}_test_result_1.txt",
            f"{day_str}_test_result_2.txt",
        ]

        data_folder_day: Path = Path(data_folder, day_str)
        if not data_folder_day.exists():
            data_folder_day.mkdir(parents=True, exist_ok=True)

        for file in file_names:
            file_path: Path = Path(data_folder, day_str, file)
            if not file_path.exists():
                file_path.touch()

        # Create the Solution

        template_file: Path = Path("utils/templates/python_template.py")

        if template_file.exists():
            with open(template_file, "r") as f:
                template_content: str = f.read()
        else:
            template_content: str = ""

        file_path: Path = Path(solution_folder, f"{day_str}.py")
        if not file_path.exists() or ok_if_exists:
            with open(file_path, "w+") as f:
                f.write(template_content)
        else:
            Files.console.print(
                f"[black on yellow] WARNING [/black on yellow] File already exists: [cyan]{file_path}[/cyan]"
            )

    @staticmethod
    def get_path() -> Path:
        """
        Returns the parent directory of the current file.
        """
        # Assumes files.py is in a utils subdir
        return Path(__file__).parent.parent
