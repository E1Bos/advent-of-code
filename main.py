#!/usr/bin/env python3
"""Advent of Code Runner - A CLI tool for running AoC solutions."""

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
from dataclasses import dataclass
import subprocess
import traceback
import re
import sys
import signal

# Third-party modules
try:
    from pyperclip import copy
    from rich.panel import Panel
    import yaml
except ImportError:
    print("Please install the project requirements - `uv sync`")
    exit(1)

# Local modules
from utils.files import Files
from utils.solution_base import SolutionBase
from utils.output_handler import OutputHandler, Logger
from utils.cli_args import Args


@dataclass
class YamlConfig:
    """Configuration loaded from config.yaml with CLI overrides."""

    year: int | None = None
    day: int | None = None
    part: int = 1
    create_missing_files: bool = True
    run_tests: bool = True
    run_quality_checks: bool = False
    auto_fix_quality: bool = False
    show_timing: bool = False
    copy_to_clipboard: bool = False
    debug: bool = False
    log_level: str = "INFO"
    log_path: str = "logs/log.log"

    @classmethod
    def from_yaml(cls, path: Path) -> "YamlConfig":
        """Load configuration from a YAML file."""
        if not path.exists():
            return cls()

        try:
            with open(path, "r", encoding="utf-8") as f:
                data: dict[str, Any] = yaml.safe_load(f) or {}
            return cls(
                year=data.get("year"),
                day=data.get("day"),
                part=data.get("part", 1),
                create_missing_files=data.get("create_missing_files", True),
                run_tests=data.get("run_tests", True),
                run_quality_checks=data.get("run_quality_checks", False),
                auto_fix_quality=data.get("auto_fix_quality", False),
                show_timing=data.get("show_timing", False),
                copy_to_clipboard=data.get("copy_to_clipboard", False),
                debug=data.get("debug", False),
                log_level=data.get("log_level", "INFO"),
                log_path=data.get("log_path", "logs/log.log"),
            )
        except Exception:
            return cls()


class AdventRunner:
    """
    Main runner class for Advent of Code solutions.

    Handles argument parsing, solution importing, test running, and execution.
    """

    def __init__(self) -> None:
        """Initialize the runner with configuration and context."""
        self._start_time: float = default_timer()
        self._current_operation: str = "Initializing"

        config_path = Path(__file__).parent / "config.yaml"
        self._config: YamlConfig = YamlConfig.from_yaml(config_path)

        self._args: Args = self._parse_arguments()

        log_level = getattr(__import__("logging"), self._config.log_level, INFO)
        self._context: OutputHandler = OutputHandler(
            logger=Logger(
                name="advent-runner",
                log_path=Path(self._config.log_path),
                file_level=log_level,
            )
        )

        self._solution: SolutionBase | None = None

    def _parse_arguments(self) -> Args:
        """Parse command-line arguments, using config as defaults."""
        parser = ArgumentParser(description="Advent of Code CLI Runner")

        default_year = self._config.year or date.today().year
        default_day = self._config.day or date.today().day

        parser.add_argument(
            "-y",
            "--year",
            dest="year",
            default=default_year,
            metavar="YEAR",
            type=int,
            help=f"Year of the AoC problem (default: {default_year})",
        )
        parser.add_argument(
            "-d",
            "--day",
            dest="day",
            default=default_day,
            metavar="DAY",
            type=int,
            help=f"Day of the AoC problem (default: {default_day})",
        )
        parser.add_argument(
            "-p",
            "--part",
            dest="part",
            default=self._config.part,
            metavar="PART",
            type=int,
            help=f"Part number (1 or 2, default: {self._config.part})",
        )
        parser.add_argument(
            "-c",
            "--copy",
            dest="copy_result",
            action="store_true",
            default=self._config.copy_to_clipboard,
            help="Copy the result to clipboard",
        )
        parser.add_argument(
            "-a",
            "--all",
            dest="run_all",
            action="store_true",
            help="Run all parts (1 and 2)",
        )
        parser.add_argument(
            "-t",
            "--test",
            dest="only_test",
            action="store_true",
            help="Only run tests, don't execute solution",
        )
        parser.add_argument(
            "--skip",
            "--skip-tests",
            dest="skip_test",
            action="store_true",
            default=not self._config.run_tests,
            help="Skip running tests",
        )
        parser.add_argument(
            "--create",
            action="store_true",
            dest="create",
            help="Create necessary files for specified year and day",
        )
        parser.add_argument(
            "-ti",
            "--timeit",
            dest="timeit",
            action="store_true",
            default=self._config.show_timing,
            help="Show timing information",
        )
        parser.add_argument(
            "-pr",
            "--profile",
            dest="profile",
            action="store_true",
            help="Profile the solution and open results in browser",
        )
        parser.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            default=self._config.debug,
            help="Enable debug output from solutions",
        )
        parser.add_argument(
            "-q",
            "--quality",
            dest="quality",
            action="store_true",
            default=self._config.run_quality_checks,
            help="Run code quality checks before executing",
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
            quality=parsed_args.quality,
            debug=parsed_args.debug,
        )

    def _validate_arguments(self) -> bool:
        """Validate the command-line arguments. Returns True if valid."""
        self._current_operation = "Validating arguments"
        valid = True

        if not 0 < self._args.day < 26:
            self._context.print_error("Day must be between 1 and 25")
            self._context.log(ERROR, f"Day out of range: {self._args.day}")
            valid = False

        if not 2014 <= self._args.year and not 14 <= self._args.year < 100:
            self._context.print_error("Year must be between 14-99 or 2014-2099")
            self._context.log(ERROR, f"Invalid year: {self._args.year}")
            valid = False

        if self._args.part not in [1, 2]:
            self._context.print_error("Part must be either 1 or 2")
            self._context.log(ERROR, f"Invalid part: {self._args.part}")
            valid = False

        if 14 <= self._args.year < 100:
            self._args.year = 2000 + self._args.year

        # Check if AoC has started for the given year
        if (
            date.today().month != 12
            and self._args.year >= date.today().year
            and not self._args.create
        ):
            self._context.log(
                WARNING, f"Advent of Code for {self._args.year} hasn't started yet"
            )
            self._context.print_warning(
                f"Advent of Code for {self._args.year} hasn't started yet, "
                "please specify a different year using -y or --year",
                end="\n",
            )
            self._context.print_info(
                "To create files for a future year, use the --create flag"
            )
            valid = False

        day_specified = any(arg.startswith(("-d", "--day")) for arg in sys_argv[1:])
        if date.today().month != 12 and not day_specified:
            self._context.log(WARNING, "Not December and day not specified")
            self._context.print_warning(
                "It is not currently December, please specify a day using -d or --day"
            )
            valid = False

        return valid

    def _check_and_create_files(self) -> bool:
        """Check if solution files exist and create them if necessary. Returns True to continue."""
        self._current_operation = "Checking solution files"
        solution_path = Path(f"solutions/{self._args.year}/{self._args.day_str}.py")

        if self._args.create:
            self._context.log(
                INFO, f"Creating files for {self._args.year}/{self._args.day}"
            )
            Files.create_day(self._context, self._args, force_create=True)
            return False

        if not solution_path.exists():
            if self._config.create_missing_files:
                self._context.log(
                    INFO, f"Creating files for {self._args.year}/{self._args.day}"
                )
                Files.create_day(
                    self._context, self._args, self._config.create_missing_files
                )
                return False
            else:
                self._context.log(ERROR, f"Solution file not found: {solution_path}")
                self._context.print_error(
                    f"Solution for [cyan]{self._args.year}/{self._args.day_str}[/cyan] does not exist"
                )
                return False

        if self._config.create_missing_files:
            Files.create_day(self._context, self._args, only_data=True)

        return True

    def _get_install_name(self, solution_path: Path, module_name: str) -> str:
        """
        Parse the solution file to find install hints for a module.

        Looks for patterns like:
            import z3  # {z3-solver}
            import z3 as z  # {z3-solver}
            from z3 import ...  # {z3-solver}

        Returns the install name from the comment, or the module name if not found.
        """
        # Pattern for: import module_name  # {install-name}
        pattern_import = rf"^import\s+{re.escape(module_name)}\s*#\s*\{{(.+?)\}}"

        # Pattern for: import module_name as alias  # {install-name}
        pattern_import_as = (
            rf"^import\s+{re.escape(module_name)}\s+as\s+\w+\s*#\s*\{{(.+?)\}}"
        )

        # Pattern for: from module_name import ...  # {install-name}
        pattern_from = (
            rf"^from\s+{re.escape(module_name)}\s+import\s+.+?\s*#\s*\{{(.+?)\}}"
        )

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

    def _install_missing_module(
        self, module_name: str, install_name: str, install_all: bool
    ) -> tuple[bool, bool]:
        """Prompt to install a missing module. Returns (success, install_all)."""
        response = "n"
        display_name = f"[cyan bold]{install_name}[/cyan bold]"

        if install_name != module_name:
            display_name += f" (for [cyan]{module_name}[/cyan])"

        if not install_all:
            self._context.print_warning(
                f"Module {display_name} is missing. Would you like to run "
                f"[green bold]`uv pip install {install_name}`[/green bold]?\n"
                "[cyan](y/Y/n):[/cyan] ",
                end="",
            )
            response = self._context.console.input()

        if response.lower() != "y" and not install_all:
            return False, False

        self._context.print_info(f"Installing missing module: {display_name}")
        subprocess.check_call(["uv", "pip", "install", install_name])
        return True, response.isupper() or install_all

    def _import_solution_module(self) -> ModuleType | None:
        """Import the solution module, installing missing dependencies if necessary."""
        self._current_operation = "Importing solution module"
        install_all = False
        solution_path = Path(f"solutions/{self._args.year}/{self._args.day_str}.py")

        while True:
            try:
                return import_module(
                    f"solutions.{self._args.year}.{self._args.day_str}"
                )
            except ImportError as e:
                required_module = str(e).split(" ")[-1].replace("'", "")
                self._context.log(WARNING, f"Missing module: {required_module}")

                install_name = self._get_install_name(solution_path, required_module)
                if install_name != required_module:
                    self._context.log(
                        INFO, f"Found install hint: {required_module} -> {install_name}"
                    )

                try:
                    success, install_all = self._install_missing_module(
                        required_module, install_name, install_all
                    )
                except subprocess.CalledProcessError as e:
                    self._context.log(ERROR, f"Subprocess error: {e}")
                    self._context.print_error(f"Subprocess error: {e}")
                    return None

                if not success:
                    self._context.log(
                        ERROR, f"Failed to install module: {install_name}"
                    )
                    self._context.print_error(
                        f"Failed to install module: {install_name}"
                    )
                    return None

    def _run_quality_checks(self) -> bool:
        """Run code quality checks using the test runner. Returns True if passed."""
        self._current_operation = "Running quality checks"

        try:
            cmd = [sys.executable, "utils/test_runner.py"]
            if self._config.auto_fix_quality:
                cmd.append("--fix")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent,
            )

            if result.returncode != 0:
                self._context.print_error("Quality checks failed:")
                if result.stdout:
                    self._context.print(result.stdout)
                if result.stderr:
                    self._context.print(result.stderr)
                return False

            self._context.print_ok("Quality checks passed")
            return True

        except FileNotFoundError:
            self._context.print_warning(
                "Test runner not found, skipping quality checks"
            )
            return True
        except Exception as e:
            self._context.print_error(f"Error running quality checks: {e}")
            return False

    def _run_solution(self, parts: list[int]) -> None:
        """Run the solution for the specified parts."""
        if self._solution is None:
            return

        for part in parts:
            self._current_operation = f"Running part {part}"
            self._context.log(INFO, f"Running Part {part}")

            # Run tests if not skipped
            passed_test = True
            if not self._args.skip_test:
                self._current_operation = f"Testing part {part}"
                self._context.log(DEBUG, "Running tests")
                passed_test = self._solution.run_test(part)

            if not passed_test:
                self._context.log(ERROR, "Tests failed")
                return

            # Run the actual solution
            self._current_operation = f"Solving part {part}"
            self._context.log(DEBUG, "Tests passed. Running solution")

            with self._context.console.status(
                f"[bold green]Running P{part}...\n", spinner="dots"
            ):
                start_time = default_timer()
                answer: Any = self._solution.solve(part)
                elapsed = default_timer() - start_time

            if answer is not None:
                self._display_result(part, answer, elapsed)

    def _display_result(self, part: int, answer: Any, elapsed: float) -> None:
        """Display the solution result with optional timing."""
        answer_text = f"[black on green] RESULT [/black on green] {answer}"

        if self._args.timeit:
            elapsed_str = (
                f"{elapsed * 1000:.2f}ms" if elapsed < 0.1 else f"{elapsed:.4f}s"
            )
            answer_text += f"\n[black on blue]  TIME  [/black on blue] [blue not bold]{elapsed_str}[/blue not bold]"

        answer_panel = Panel(
            answer_text,
            style="bold green",
            border_style="green",
            title=f"[black on green] FINISHED [/black on green] [bold]Part {part} [/bold]",
        )

        self._context.print(answer_panel)
        self._context.log(
            INFO,
            f"Year {self._args.year} | Day {self._args.day} | Part {part} | "
            f"Answer: {answer} | Time: {elapsed:.4f}s",
        )

        # Copy to clipboard if requested and only one part
        if self._args.copy_result and answer is not None:
            copy(str(answer))
            self._context.print(" Answer Copied ", style="black on blue")

    def _print_header(self, parts: list[int]) -> None:
        """Print the decorative header."""
        width = round((self._context.console.width - 20) * 0.7)
        horizontal_spacers = "─" * (width // 2)

        self._context.print(
            f"{horizontal_spacers} [yellow]*[/yellow] Advent of Code [yellow]*[/yellow] {horizontal_spacers}",
            justify="center",
            style="green bold",
        )
        self._context.print(
            f"Running Day [cyan]{self._args.year}/{self._args.day_str}[/cyan] | "
            f"Part {' and '.join(map(str, parts))}",
            justify="center",
            style="green",
        )
        self._context.print()

    def _handle_interrupt(self, signum: int | None = None, frame: Any = None) -> None:
        """Handle keyboard interrupt gracefully."""
        elapsed = default_timer() - self._start_time

        location = "Unknown location"
        if frame is not None:
            location = (
                f"{frame.f_code.co_filename}:{frame.f_lineno} in {frame.f_code.co_name}"
            )
        else:
            tb = traceback.extract_stack()
            if tb:
                last = tb[-2]
                location = f"{last.filename}:{last.lineno} in {last.name}"

        elapsed_str = f"{elapsed * 1000:.2f}ms" if elapsed < 0.1 else f"{elapsed:.4f}s"

        self._context.print()

        tb_lines = traceback.format_stack()[-5:-1]
        tb_context = "".join(tb_lines).strip()

        interrupt_panel = Panel(
            f"[bold]Operation:[/bold] {self._current_operation}\n"
            f"[bold]Location:[/bold] {location}\n"
            f"[bold]Elapsed:[/bold] {elapsed_str}\n"
            f"[bold]Traceback:[/bold]\n{tb_context}",
            title="[white on red] INTERRUPTED [/white on red]",
            style="red",
            border_style="red",
        )
        self._context.print(interrupt_panel)
        self._context.log(
            WARNING,
            f"Interrupted during {self._current_operation} at {location} after {elapsed_str}",
        )

        sys.exit(130)

    def start(self) -> None:
        """Main entry point - orchestrates the entire execution flow."""

        signal.signal(signal.SIGINT, self._handle_interrupt)

        try:
            self._context.print()

            if not self._validate_arguments():
                sys.exit(1)

            if not self._check_and_create_files():
                sys.exit(0)

            solution_module: ModuleType | None = self._import_solution_module()
            if solution_module is None or not hasattr(solution_module, "Solution"):
                self._context.print_error(
                    "The solution module does not have a 'Solution' class."
                )
                self._context.log(
                    ERROR, "Missing 'Solution' class in the solution module."
                )
                sys.exit(1)

            self._current_operation = "Instantiating solution"
            self._solution = getattr(solution_module, "Solution")(
                context=self._context,
                args=self._args,
            )

            parts: list[int] = [1, 2] if self._args.run_all else [self._args.part]

            self._context.log(
                INFO, f"Running Day {self._args.year}/{self._args.day} | Part {parts}"
            )

            self._print_header(parts)

            if self._config.run_quality_checks or self._args.quality:
                if not self._run_quality_checks():
                    sys.exit(1)

            self._run_solution(parts)

            self._context.log(INFO, "All parts processed, exiting.")

        except KeyboardInterrupt:
            self._handle_interrupt()
        except Exception as e:
            self._context.print_error(f"Unexpected error: {e}")
            self._context.log(ERROR, f"Unexpected error: {traceback.format_exc()}")
            sys.exit(1)


def main() -> None:
    """Main entry point for the Advent of Code runner."""
    runner = AdventRunner()
    runner.start()


if __name__ == "__main__":
    main()
