#!/usr/bin/env python3

# Built-in modules
from types import ModuleType
from typing import Any
from datetime import date
from argparse import ArgumentParser
from importlib import import_module
from pathlib import Path
from timeit import default_timer
from logging import DEBUG, INFO, WARNING, ERROR
from sys import argv as sys_argv
import subprocess
import re

# Third-party modules
try:
    from pyperclip import copy
    from rich.panel import Panel
except ImportError:
    print("Please install the project requirements - `uv sync`")
    exit(1)

# Local modules
from utils.files import Files
from utils.solution_base import SolutionBase
from utils.output_handler import OutputHandler, Logger
from utils.cli_args import Args


def parse_arguments() -> Args:
    """Parse command-line arguments and return an Args dataclass instance."""
    parser: ArgumentParser = ArgumentParser(description="Advent of Code CLI")
    parser.add_argument(
        "-y",
        "--year",
        dest="year",
        default=date.today().year,
        metavar="year_num",
        type=int,
        help="Optional, year of the AoC problem, defaults to the current year",
    )
    parser.add_argument(
        "-d",
        "--day",
        dest="day",
        default=date.today().day,
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
        dest="run_all",
        action="store_true",
        help="Optional, run all parts",
    )
    parser.add_argument(
        "-t",
        "--test",
        dest="only_test",
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
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help="Optional, allow logging debug messages to stdout from the solution",
    )

    parsed_args, unknown = parser.parse_known_args()

    if unknown:
        print(f"Warning: Unknown arguments detected: {' '.join(unknown)}")

    return Args(
        year=parsed_args.year,
        day=parsed_args.day,
        part=parsed_args.part,
        copy_result=parsed_args.copy_result,
        run_all=parsed_args.run_all,
        only_test=parsed_args.only_test if not parsed_args.skip_test else False,
        skip_test=parsed_args.skip_test,
        create=parsed_args.create,
        timeit=parsed_args.timeit,
        profile=parsed_args.profile,
        debug=parsed_args.debug,
    )


def validate_arguments(context: OutputHandler, args: Args) -> None:
    """Validate the command-line arguments and print/log errors if invalid."""
    valid: bool = True

    if not 0 < args.day < 26:
        context.print_error("Day must be between 1 and 25")
        context.log(ERROR, f"Day out of range: {args.day}")
        valid = False

    if not 2014 <= args.year and not 14 <= args.year < 100:
        context.print_error("Year must be between 14-99 or 2014-2099")
        context.log(ERROR, f"Invalid year: {args.year}")
        valid = False

    if args.part not in [1, 2]:
        context.print_error("Part must be either 1 or 2")
        context.log(ERROR, f"Invalid part: {args.part}")
        valid = False

    if 14 <= args.year < 100:
        args.year = 2000 + args.year

    if date.today().month != 12 and args.year >= date.today().year and not args.create:
        context.log(WARNING, f"Advent of Code for {args.year} hasn't started yet")
        context.print_warning(
            f"Advent of Code for {args.year} hasn't started yet, please specify a different year using -y or --year",
            end="\n",
        )
        context.print_info(
            "To create the necessary files for the specified year and day, use the --create flag"
        )
        valid = False

    day_specified = any(arg.startswith(("-d", "--day")) for arg in sys_argv[1:])
    if date.today().month != 12 and not day_specified:
        context.log(WARNING, "Not December and day not specified")
        context.print_warning(
            "It is not currently December, please specify a day using -d or --day"
        )
        valid = False

    if not valid:
        exit(1)


def check_and_create_solution_files(
    context: OutputHandler, args: Args, create_if_not_exists: bool = False
) -> None:
    """Check if solution files exist and create them if necessary."""
    solution_path: Path = Path(f"solutions/{args.year}/{args.day_str}.py")

    if args.create or (create_if_not_exists and not solution_path.exists()):
        context.log(INFO, f"Creating files for {args.year}/{args.day}")
        Files.create_day(context, args, create_if_not_exists)
        exit(0)

    if not solution_path.exists():
        context.log(ERROR, f"Solution file not found: {solution_path}")
        context.print_error(
            f"Solution for [cyan]{args.year}/{args.day_str}[/cyan] does not exist"
        )
        exit(1)


def get_install_name(solution_path: Path, module_name: str) -> str:
    """
    Parse the solution file to find install hints for a module.

    Looks for patterns like:
        import z3  # {z3-solver}
        import z3 as z  # {z3-solver}
        from z3 import ...  # {z3-solver}

    Returns the install name from the comment, or the module name if no hint found.
    """
    # Pattern for: import module_name  # {install-name}
    pattern_import = rf"^import\s+{re.escape(module_name)}\s*#\s*\{{(.+?)\}}"

    # Pattern for: import module_name as alias  # {install-name}
    pattern_import_as = (
        rf"^import\s+{re.escape(module_name)}\s+as\s+\w+\s*#\s*\{{(.+?)\}}"
    )

    # Pattern for: from module_name import ...  # {install-name}
    pattern_from = rf"^from\s+{re.escape(module_name)}\s+import\s+.+?\s*#\s*\{{(.+?)\}}"

    patterns = [pattern_import_as, pattern_import, pattern_from]

    try:
        with open(solution_path, "r", encoding="utf-8") as f:
            for line in f:
                stripped_line = line.strip()
                for pattern in patterns:
                    match = re.match(pattern, stripped_line)
                    if match:
                        return match.group(1).strip()
    except Exception:
        pass

    return module_name


def install_missing_module(
    context: OutputHandler, module_name: str, install_name: str, install_all: bool
) -> tuple[bool, bool]:
    """Prompt to install a missing module and install it if confirmed."""
    response: str = "n"
    display_name: str = f"[cyan bold]{install_name}[/cyan bold]"

    if install_name != module_name:
        display_name += f" (for [cyan]{module_name}[/cyan])"

    if not install_all:
        context.print_warning(
            f"Module {display_name} is missing. Would you like to run [green bold]`uv pip install {install_name}`[/green bold]?\n"
            "[cyan](y/Y/n):[/cyan] ",
            end="",
        )
        response = context.console.input()

    if not response.lower() == "y" and not install_all:
        return False, False

    context.print_info(f"Installing missing module: {display_name}")
    subprocess.check_call(["uv", "pip", "install", install_name])
    return True, response.isupper() or install_all


def import_solution_module(context: OutputHandler, args: Args) -> ModuleType:
    """Import the solution module for the specified year and day, installing missing dependencies if necessary."""
    install_all: bool = False
    solution_path: Path = Path(f"solutions/{args.year}/{args.day_str}.py")

    while True:
        try:
            return import_module(f"solutions.{args.year}.{args.day_str}")
        except ImportError as e:
            required_module = str(e).split(" ")[-1].replace("'", "")
            context.log(WARNING, f"Missing module: {required_module}")

            install_name = get_install_name(solution_path, required_module)
            if install_name != required_module:
                context.log(
                    INFO, f"Found install hint: {required_module} -> {install_name}"
                )

            try:
                success, install_all = install_missing_module(
                    context, required_module, install_name, install_all
                )
            except subprocess.CalledProcessError as e:
                context.log(ERROR, f"Subprocess error: {e}")
                context.print_error(f"Subprocess error: {e}")
                exit(1)

            if not success:
                context.log(ERROR, f"Failed to install module: {install_name}")
                context.print_error(f"Failed to install module: {install_name}")
                exit(1)


def run_solution(
    context: OutputHandler, solution: SolutionBase, parts: list[int], args: Args
) -> None:
    """Run the solution for the specified parts, including tests and timing."""
    for part in parts:
        context.log(INFO, f"Running Part {part}")
        passed_test: bool = True
        if not args.skip_test:
            context.log(DEBUG, "Running tests")
            passed_test = solution.run_test(part)

        if not passed_test:
            context.log(ERROR, "Tests failed")
            return

        context.log(DEBUG, "Tests passed. Running solution")
        with context.console.status(
            f"[bold green]Running P{part}...\n", spinner="dots"
        ):
            start_time: float = default_timer()
            answer: Any = solution.solve(part)
            elapsed = default_timer() - start_time

        if answer is not None:
            answer_text = f"[black on green] RESULT [/black on green] {answer}"

            if args.timeit:
                if elapsed < 0.1:
                    elapsed = f"{elapsed * 1000:.2f}ms"
                else:
                    elapsed = f"{elapsed:.4f}s"

                answer_text += f"\n[black on blue]  TIME  [/black on blue] [blue not bold]{elapsed}[/blue not bold]"

            answer_panel = Panel(
                answer_text,
                style="bold green",
                border_style="green",
                title=f"[black on green] FINISHED [/black on green] [bold]Part {part} [/bold]",
            )

            context.print(answer_panel)
            context.log(
                INFO,
                f"Year {args.year} | Day {args.day} | Part {part} | Answer: {answer} | Time: {elapsed}",
            )

        if args.copy_result and answer is not None and len(parts) == 1:
            copy(str(answer))
            context.print(" Answer Copied ", style="black on blue")


def main() -> None:
    """Main entry point for the Advent of Code runner."""
    CREATE_IF_NOT_EXISTS: bool = True

    args: Args = parse_arguments()

    context = OutputHandler(
        logger=Logger(
            name="main-runner",
            log_path=Path("logs/log.log"),
            file_level=INFO,
        )
    )

    context.print()

    validate_arguments(context, args)
    check_and_create_solution_files(context, args, CREATE_IF_NOT_EXISTS)

    solution_module: ModuleType = import_solution_module(context, args)

    solution: SolutionBase = solution_module.Solution(
        context=context,
        args=args,
    )

    parts: list[int] = [args.part]
    if args.run_all:
        parts = [1, 2]

    context.log(INFO, f"Running Day {args.year}/{args.day} | Part {parts}")

    width: int = round((context.console.width - 20) * 0.7)
    horizontal_spacers: str = "─" * (width // 2)
    context.print(
        f"{horizontal_spacers} [yellow]*[/yellow] Advent of Code [yellow]*[/yellow] {horizontal_spacers}",
        justify="center",
        style="green bold",
    )
    context.print(
        f"Running Day [cyan]{args.year}/{args.day_str}[/cyan] | Part {' and '.join(map(str, parts))}",
        justify="center",
        style="green",
    )
    context.print()

    run_solution(context, solution, parts, args)

    context.logger.info("All parts processed, exiting.")


if __name__ == "__main__":
    main()
