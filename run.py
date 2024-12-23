from types import ModuleType
from typing import Any
from datetime import date
from argparse import ArgumentParser, Namespace
from importlib import import_module
from pathlib import Path
from timeit import default_timer
from pyperclip import copy

from rich.console import Console
from rich.panel import Panel

from utils.files import Files
from utils.solution_base import SolutionBase


def main() -> None:
    CREATE_IF_NOT_EXISTS: bool = False

    _today: int = date.today().day
    _year: int = date.today().year

    console: Console = Console()

    def print_error(message: str) -> None:
        console.print(f"[black on red] ERROR [/black on red] {message}\n", style="red")

    def print_ok(message: str) -> None:
        console.print(f"[black on green] OK [/black on green] {message}\n", style="green")

    parser: ArgumentParser = ArgumentParser(description="Advent of Code CLI")
    parser.add_argument(
        "-y",
        "--year",
        dest="year",
        default=_year,
        metavar="year_num",
        type=int,
        help="Optional, year of the AoC problem, defaults to the current year",
    )
    parser.add_argument(
        "-d",
        "--day",
        dest="day",
        default=_today,
        metavar="day_num",
        type=int,
        help="Optional, day of the AoC problem, defaults to the current day",
    )
    parser.add_argument(
        "-p",
        "--part",
        dest="part",
        default=1,
        metavar="part_num",
        type=int,
        help="Optional, part number of the solution, defaults to part 1",
    )
    parser.add_argument(
        "-c",
        "--copy",
        dest="copy_result",
        action="store_true",
        help="Optional, copy the results to the clipboard",
    )
    parser.add_argument(
        "-a",
        "--all",
        dest="all",
        action="store_true",
        help="Optional, run all parts",
    )
    parser.add_argument(
        "-t",
        "--test",
        dest="only_tests",
        action="store_true",
        help="Optional, only run tests",
    )
    parser.add_argument(
        "--skip",
        "--skip-tests",
        dest="skip_test",
        action="store_true",
        help="Optional, skip running tests",
    )
    parser.add_argument(
        "--create",
        action="store_true",
        dest="create",
        help="Optional, create necessary files for specified year and day",
    )
    parser.add_argument(
        "-ti",
        "--timeit",
        dest="timeit",
        action="store_true",
        help="Optional, time the solution",
    )
    parser.add_argument(
        "-pr",
        "--profile",
        dest="profile",
        action="store_true",
        help="Optional, profile the solution and open the results in a browser",
    )

    args: Namespace = parser.parse_args()

    console.print()

    if not 0 < args.day < 26:
        print_error("Day must be between 1 and 25")
        exit(1)

    if not 2014 <= args.year and not 14 <= args.year < 100:
        print_error(
            "Year must be a 2-digit number starting at 14 or a 4-digit number starting at 2014"
        )
        exit(1)

    if 14 <= args.year < 100:
        args.year = 2000 + args.year

    solution_path: Path = Path(f"solutions/{args.year:04d}/{args.day:02d}.py")

    if args.create or (CREATE_IF_NOT_EXISTS and not solution_path.exists()):
        Files.create_day(args.year, args.day)
        print_ok(f"Created files for [cyan]{args.year}/{args.day}[/cyan]")
        exit(0)

    if not solution_path.exists():
        print_error(f"Solution for [cyan]{args.year}/{args.day}[/cyan] does not exist")
        exit(1)

    if args.part not in [1, 2]:
        print_error("Part must be 1 or 2")
        exit(1)

    solution_module: ModuleType = import_module(
        f"solutions.{args.year:04d}.{args.day:02d}"
    )
    solution: SolutionBase = solution_module.Solution(
        args.year, args.day, args.only_tests, args.skip_test, args.timeit, args.profile
    )

    parts: list[int] = [args.part]
    if args.all:
        parts = [1, 2]

    width = console.width
    horizontal_spacers: str = '─' * ((width - 20) // 2)
    console.print(
        f"{horizontal_spacers} [yellow]*[/yellow] Advent of Code [yellow]*[/yellow] {horizontal_spacers}",
        justify="center",
        style="green bold",
    )
    console.print(
        f"Running Day [cyan]{args.year}/{args.day}[/cyan] | Part {" and ".join(map(str, parts))}",
        justify="center",
        style="green"
    )
    console.print()

    for part in parts:
        passed_test: bool = True
        if not args.skip_test:
            passed_test = solution.run_test(part)

        if not passed_test:
            continue

        with console.status(f"[bold green]Running P{part}...\n", spinner="dots"):
            start_time: float = default_timer()
            answer: Any = solution.solve(part)

        if answer is not None:
            answer_text = f"[black on green] RESULT [/black on green] {answer}"

            if args.timeit:
                elapsed = default_timer() - start_time
                answer_text += f"\n[black on blue]  TIME  [/black on blue] [blue not bold]{elapsed:.4f}s[/blue not bold]"

            answer_panel = Panel(
                answer_text,
                style="green",
                border_style="green",
                title=f"[black on green] FINISHED [/black on green] [bold]Part {part} [/bold]",
            )
            console.print(answer_panel)

        if args.copy_result and answer is not None and len(parts) == 1:
            copy(str(answer))
            console.print(" Answer Copied ", style="black on blue")

    console.print()
    exit(0)


if __name__ == "__main__":
    main()
