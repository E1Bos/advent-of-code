# Built-in modules
from typing import Any, Callable
from logging import INFO, DEBUG
from pathlib import Path
from io import StringIO
import builtins
from argparse import Namespace

# Third-party modules
from pyinstrument import Profiler
from pyinstrument.session import Session

# from rich.panel import Panel

# Local modules
from utils.puzzle_reader import PuzzleReader
from utils.output_handler import OutputHandler, Logger

builtin_print = builtins.print


class SolutionBase:
    """
    Base class for all solutions.

    Attributes:
        raw_input (bool): Whether the input is raw text or a list of strings.
        skip_empty_tests (bool): Whether to skip tests with no expected results.
        override_print (bool): Whether to override the built-in print function.
    """

    raw_input: bool = False
    skip_empty_tests: bool = False
    override_print: bool = False
    __context: OutputHandler

    def __init__(
        self,
        context: OutputHandler,
        args: Namespace,
    ):
        self.__context = OutputHandler(
            context.console,
            Logger(
                name=f"{args.year}-{args.day}-solution",
                console=context.console if args.debug else None,
                log_path=Path("logs/log.log") if args.debug else None,
                stream_level=DEBUG,
                file_level=DEBUG,
            ),
        )

        self.__args = args

        self.__args.only_test = args.only_test if not args.skip_test else False
        self.is_test: bool = False
        self.is_part_1: bool = True

        # Override the built-in print function
        if self.override_print:
            builtins.print = self.print

    def parse(self, data: Any) -> Any:
        return data

    def part1(self, data: Any) -> Any:
        raise NotImplementedError("Part 1 not implemented")

    def part2(self, data: Any) -> Any:
        raise NotImplementedError("Part 2 not implemented")

    def print(self, *args, **kwargs) -> None:
        contents = SolutionBase.__get_contents(*args, **kwargs)
        self.__context.log(INFO, contents)

    def debug(self, *args, **kwargs) -> None:
        contents = SolutionBase.__get_contents(*args, **kwargs)
        self.__context.log(DEBUG, contents)

    @staticmethod
    def __get_contents(*args, **kwargs) -> str:
        output = StringIO()
        builtin_print(*args, file=output, **kwargs)
        contents = output.getvalue()
        output.close()

        return contents[:-1] if contents.endswith("\n") else contents

    def solve(self, part: int) -> Any:
        if self.__args.only_test:
            return

        puzzle_input: Any = PuzzleReader.get_input(
            self.__context, self.__args, self.raw_input
        )

        if puzzle_input is None:
            return None

        self.is_part_1 = True if part == 1 else False
        data: Any = self.parse(puzzle_input)

        func = getattr(self, f"part{part}")

        result = self.__run_solution(func, data)

        return result

    def __run_solution(self, func: Callable, data: Any) -> Any:
        try:
            if self.__args.profile:
                return self.__profile(func, data)
            return func(data)
        except NotImplementedError:
            self.__context.print_error("Part not implemented")
            return None

    def __get_test_input(self) -> Any:
        return PuzzleReader.get_input(self.__context, self.__args, self.raw_input, True)

    def __get_test_results(self, part: int) -> Any:
        return PuzzleReader.get_test_results(self.__context, self.__args, part)

    def run_test(self, part: int) -> bool:
        """
        Runs the test for the specified part of the puzzle.

        Args:
            part (int): The part of the puzzle to test.

        Returns:
            bool: True if the test passed, False otherwise.
        """

        self.is_test: bool = True

        test_input: Any = self.__get_test_input()

        try:
            expected_result: Any = self.__get_test_results(part)
        except ValueError as e:
            if self.skip_empty_tests:
                self.__context.print("[black on green] SKIPPING TEST [/black on green]")
                return True

            self.__context.print_error(
                f"{e}, cannot run test for part {part}", end="\n"
            )
            self.__context.print_info(
                "Set [green]skip_empty_tests[/green] to True to skip this check."
            )
            return False

        func: Callable = getattr(self, f"part{part}")

        if expected_result is None or (
            not isinstance(expected_result, int) and len(expected_result) == 0
        ):
            self.is_test = False

            # Return true here so it still runs the solution even if the test result is missing
            return True

        self.is_part_1 = True if part == 1 else False
        parsed_test_input = self.parse(test_input)

        with self.__context.console.status(
            f"[bold yellow]Testing P{part}...\n", spinner="dots"
        ):
            result = self.__run_solution(func, parsed_test_input)

        if result is None:
            return False

        if result == expected_result:
            self.__context.print(
                f"[black on green] OK [/black on green] Test for part {part} passed"
            )
        else:
            result_str: str = str(result)
            expected_str: str = str(expected_result)

            diff_str: str = ""
            for res_char, exp_char in zip(result_str, expected_str):
                if res_char != exp_char:
                    diff_str += f"[red bold]{exp_char}[/red bold]"
                else:
                    diff_str += exp_char

            if len(result_str) < len(expected_str):
                diff_str += f"[red bold]{expected_str[len(result_str):]}[/red bold]"

            if len(result_str) > len(expected_str):
                diff_str += f"[red bold]{result_str[len(expected_str):]}[/red bold]"

            self.__context.print(
                f"[black on red] ERROR [/black on red] Test for part {part} failed"
                f"\n[bold red]Output:[/bold red]   {result}"
                f"\n[bold green]Expected:[/bold green] {expected_result}"
                f"\n[bold blue]Diff:[/bold blue]     {diff_str}",
            )

            # Panel used for errors
            # error_panel = Panel(
            #     f"[bold red]Output:[/bold red]   {result}\n"
            #     f"[bold green]Expected:[/bold green] {expected_result}\n"
            #     f"[bold blue]Diff:[/bold blue]     {diff_str}",
            #     title=f"[black on red] ERROR [/black on red] Test for part {part} failed",
            #     border_style="red",
            # )
            # self.console.print(error_panel)
            return False

        self.is_test = False
        return True

    def __profile(self, func: Callable, *args, **kwargs) -> Any:
        profiler: Profiler = Profiler()

        profiler.start()
        result: Any = func(*args, **kwargs)
        session: Session = profiler.stop()

        if self.__args.only_test or not self.is_test:
            self.__context.print_info("Session too fast to profile", end="\n")

        if session.sample_count != 0:
            profiler.open_in_browser()

        return result
