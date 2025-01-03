"""Utility class for file and directory operations."""

# Built-in module
from pathlib import Path

# Local modules
from utils.output_handler import OutputHandler
from utils.cli_args import Args


class Files:
    """Utility class for file and directory operations."""

    @staticmethod
    def create_day(
        context: OutputHandler, args: Args, ok_if_exists: bool = False
    ) -> None:
        """
        Create the necessary files and directories for a new day's puzzle.

        Args:
            context (OutputHandler): The output handler for the program.
            args (Args): The parsed command-line arguments.
            ok_if_exists (bool, optional): If True, will overwrite the file if it already exists. Defaults to False.

        Raises:
            ValueError: If year is not a 4-digit number.
        """
        path: Path = Files.get_path()

        if len(args.year_str) != 4:
            raise ValueError("Year must be a 4-digit number, formatted as YYYY")

        Files.__create_directories(path, args.year_str)
        Files.__create_data_files(path, args)
        Files.__create_solution_file(context, path, args, ok_if_exists)

    @staticmethod
    def __create_directories(path: Path, year_str: str) -> None:
        """
        Create the necessary directories for the specified year.

        Args:
            path (Path): The path to the grandparent directory of the current file.
            year_str (str): The year as a string.
        """
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

    @staticmethod
    def __create_data_files(path: Path, args: Args) -> None:
        """
        Create the necessary data files for the specified year and day.

        Args:
            path (Path): The path to the grandparent directory of the current file.
            args (Args): The parsed command-line arguments.
        """
        data_folder: Path = Path(path, "data", args.year_str)
        file_names: list[str] = [
            f"{args.day_str}_input.txt",
            f"{args.day_str}_test_input.txt",
            f"{args.day_str}_test_result_1.txt",
            f"{args.day_str}_test_result_2.txt",
        ]

        data_folder_day: Path = Path(data_folder, args.day_str)
        if not data_folder_day.exists():
            data_folder_day.mkdir(parents=True, exist_ok=True)

        for file in file_names:
            file_path: Path = Path(data_folder, args.day_str, file)
            if not file_path.exists():
                file_path.touch()

    @staticmethod
    def __create_solution_file(
        context: OutputHandler,
        path: Path,
        args: Args,
        ok_if_exists: bool,
    ) -> None:
        """
        Create a new solution file for the specified year and day.

        Args:
            context (OutputHandler): The output handler for the program.
            path (Path): The path to the grandparent directory of the current file.
            args (Args): The parsed command-line arguments.
            ok_if_exists (bool): If True, will overwrite the file if it already exists.
        """
        solution_folder: Path = Path(path, "solutions", args.year_str)
        template_file: Path = Path("utils/templates/python_template.py")

        template_content: str = ""
        if template_file.exists():
            with open(template_file, "r") as f:
                template_content = f.read()

        template_content = Files.__edit_template(template_content)

        file_path: Path = Path(solution_folder, f"{args.day_str}.py")
        if not file_path.exists() or ok_if_exists:
            with open(file_path, "w+") as f:
                f.write(template_content)
            context.print_ok(f"Created file: [cyan]{file_path}[/cyan] and data files")
        else:
            context.print_warning(f"File already exists: [cyan]{file_path}[/cyan]")

    @staticmethod
    def __edit_template(template: str) -> str:
        """
        Adjust the template content to fit the current solution.

        Args:
            template (int): The template content.

        Returns:
            str: The adjusted template content.
        """
        remove_strings: list[str] = [
            "# noqa",
        ]

        for string in remove_strings:
            template = template.replace(string, "")

        return template

    @staticmethod
    def get_path() -> Path:
        """
        Return the grandparent directory of the current file.

        Returns:
            Path: The grandparent directory of the current file. (Assumes files.py is in a utils subdir)
        """
        parent: Path = Path(__file__).parent

        if parent.name == "utils":
            return parent.parent

        raise ValueError(
            f"Expected parent directory of {__file__} to be 'utils', but found '{parent.name}'"
        )
