from utils.puzzle_reader import PuzzleReader
from typing import Any, Callable
from rich.console import Console
from pyinstrument import Profiler
# from rich.panel import Panel


class SolutionBase:
    raw_input: bool = False
    console = Console()

    def __init__(
        self,
        year: int,
        day: int,
        only_test: bool = False,
        skip_test: bool = False,
        time_it: bool = False,
        profile_it: bool = False,
    ):
        self.year: int = year
        self.day: int = day

        self.skip_test: bool = skip_test
        self.only_test: bool = only_test if not self.skip_test else False
        self.is_test: bool = False
        self.is_part_1: bool = True

        self.time_it: bool = time_it
        self.profile_it: bool = profile_it

    def parse(self, data: Any) -> Any:
        return data

    def part1(self, data: Any) -> Any:
        raise NotImplementedError("Part 1 not implemented")

    def part2(self, data: Any) -> Any:
        raise NotImplementedError("Part 2 not implemented")

    def solve(self, part: int) -> Any:
        if self.only_test:
            return

        puzzle_input: Any = PuzzleReader.get_input(self.year, self.day, self.raw_input)

        if puzzle_input == None:
            return None

        data: Any = self.parse(puzzle_input)
        self.is_part_1 = True if part == 1 else False
        func = getattr(self, f"part{part}")

        if self.profile_it:
            result = self.profile(func, data)
        else:
            result = func(data)

        return result

    def get_test_input(self) -> Any:
        return PuzzleReader.get_input(self.year, self.day, self.raw_input, True)

    def get_test_results(self, part: int) -> Any:
        return PuzzleReader.get_test_results(self.year, self.day, part)

    def run_test(self, part: int) -> bool:
        """
        Runs the test for the specified part of the puzzle.

        Args:
            part (int): The part of the puzzle to test.

        Returns:
            bool: True if the test passed, False otherwise.
        """

        self.is_test: bool = True

        test_input: Any = self.get_test_input()
        expected_result: Any = self.get_test_results(part)

        func: Callable = getattr(self, f"part{part}")

        if expected_result is None or (
            not isinstance(expected_result, int) and len(expected_result) == 0
        ):
            self.is_test = False

            # Return true here so it still runs the solution even if the test result is missing
            return True

        parsed_test_input = self.parse(test_input)
        self.is_part_1 = True if part == 1 else False

        with self.console.status(f"[bold yellow]Testing P{part}...\n", spinner="dots"):
            if self.profile_it and self.only_test:
                result = self.profile(func, parsed_test_input)
            else:
                result = func(parsed_test_input)

        if result == expected_result:
            self.console.print(f"[black on green] OK [/black on green] Test for part {part} passed")
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

            self.console.print(
                f"[black on red] ERROR [/black on red] Test for part {part} failed" \
                f"\n[bold red]Output:[/bold red]   {result}" \
                f"\n[bold green]Expected:[/bold green] {expected_result}" \
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

    def profile(self, func: Callable, *args, **kwargs) -> Any:
        profiler: Profiler = Profiler()

        profiler.start()
        try:
            result: Any = func(*args, **kwargs)
        finally:
            profiler.stop()

            profiler.open_in_browser()

        return result
