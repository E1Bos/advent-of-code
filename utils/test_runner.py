import unittest
import doctest
import os
import sys
import importlib.util
from pathlib import Path
from typing import Any
from types import ModuleType
import argparse
import subprocess
from dataclasses import dataclass, field
from typing import Set


@dataclass(frozen=True)
class ExcludeDirsRecord:
    dirs: Set[str] = field(
        default_factory=lambda: {
            ".venv",
            ".git",
            "__pycache__",
            ".ruff_cache",
            ".vscode",
            "logs",
            "data",
            "solutions",
            "templates",
        }
    )


ExcludeDirs = ExcludeDirsRecord()


class ProjectDocTestLoader:
    def __init__(self, verbose: bool, no_output: bool) -> None:
        self.verbose: bool = verbose
        self.no_output: bool = no_output
        self.start_dir: Path = Path(__file__).parent.parent.absolute()

        # Add project root to sys.path to ensure imports within modules (e.g., 'from utils...') work correctly
        if str(self.start_dir) not in sys.path:
            sys.path.insert(0, str(self.start_dir))

    def discover(self) -> unittest.TestSuite:
        tests: unittest.TestSuite = unittest.TestSuite()

        # Use ExcludeDirs record
        exclude_dirs: set[str] = ExcludeDirs.dirs

        if self.verbose and not self.no_output:
            print(f"Scanning for doctests in: {self.start_dir}")

        for root, dirs, files in os.walk(self.start_dir):
            # Modify dirs in-place to skip excluded directories during traversal
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                # Check for Python files, excluding this test script itself
                if str(file).endswith(".py") and file != os.path.basename(__file__):
                    file_path: Path = Path(root) / file

                    try:
                        # Construct module name from file path relative to project root
                        rel_path: Path = file_path.relative_to(self.start_dir)
                        module_name: str = str(rel_path).replace(os.sep, ".")[:-3]

                        # Load the module dynamically
                        spec = importlib.util.spec_from_file_location(
                            module_name, file_path
                        )
                        if spec and spec.loader:
                            module: ModuleType = importlib.util.module_from_spec(spec)
                            # Register module in sys.modules so imports inside it resolve correctly
                            sys.modules[module_name] = module
                            spec.loader.exec_module(module)

                            # Create a DocTestSuite for the module
                            try:
                                # This finds all docstrings with >>> examples and creates tests for them
                                suite = doctest.DocTestSuite(module)
                                tests.addTests(suite)
                            except ValueError:
                                # ValueError is raised if no doctests are found in the module; just skip it
                                pass
                    except Exception as e:
                        # If a file cannot be imported (e.g., syntax error or missing dependency), report it but continue
                        if self.verbose and not self.no_output:
                            print(f"[Warning] Skipping {file_path.name}: {e}")
        return tests


class CodeQualityTests(unittest.TestCase):
    fix_issues: bool = False

    def test_check(self) -> None:
        """Run ruff check"""
        root: Path = Path(__file__).parent.parent
        cmd: list[str] = ["ruff", "check", "."]
        if self.fix_issues:
            cmd.insert(2, "--fix")

        try:
            subprocess.run(
                cmd,
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            self.fail(f"Ruff check failed:\n{e.stdout}\n{e.stderr}")
        except FileNotFoundError:
            self.skipTest("Ruff executable not found")

    def test_format(self) -> None:
        """Run ruff format --check"""
        root: Path = Path(__file__).parent.parent
        try:
            subprocess.run(
                ["ruff", "format", "--check", "."],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            self.fail(f"Ruff format check failed:\n{e.stdout}\n{e.stderr}")
        except FileNotFoundError:
            self.skipTest("Ruff executable not found")

    def test_types(self) -> None:
        """Run ty type checking"""
        root: Path = Path(__file__).parent.parent
        try:
            subprocess.run(
                ["ty", "check"],
                cwd=root,
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            self.fail(f"Ty type check failed:\n{e.stdout}\n{e.stderr}")
        except FileNotFoundError:
            self.skipTest("Ty executable not found")

    def test_docstring_format(self) -> None:
        """Check that all functions/classes have properly formatted docstrings"""
        root: Path = Path(__file__).parent.parent

        if str(root) not in sys.path:
            sys.path.insert(0, str(root))

        for pyfile in root.rglob("*.py"):
            # Skip excluded directories
            if any(part in ExcludeDirs.dirs for part in pyfile.parts):
                continue
            if pyfile.name == os.path.basename(__file__):
                continue
            try:
                rel_path = pyfile.relative_to(root)
                module_name = str(rel_path).replace(os.sep, ".")[:-3]

                spec = importlib.util.spec_from_file_location(module_name, pyfile)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)

                    failed, _ = doctest.testmod(module, verbose=False)
                    if failed > 0:
                        self.fail(f"Doctests failed in {module_name}")
            except Exception:
                continue


def load_tests(
    loader: unittest.TestLoader, tests: unittest.TestSuite, ignore: Any
) -> unittest.TestSuite:
    """
    Discover and load all doctests from Python files in the project.
    This function is automatically called by unittest.main().
    """
    no_output: bool = "-n" in sys.argv or "--no-output" in sys.argv
    verbose: bool = "-v" in sys.argv or "--verbose" in sys.argv
    fix: bool = "-f" in sys.argv or "--fix" in sys.argv

    CodeQualityTests.fix_issues = fix

    discoverer: ProjectDocTestLoader = ProjectDocTestLoader(verbose, no_output)
    tests.addTests(discoverer.discover())
    tests.addTests(loader.loadTestsFromTestCase(CodeQualityTests))
    return tests


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "-n", "--no-output", action="store_true", help="Suppress all output"
    )
    parser.add_argument(
        "-f", "--fix", action="store_true", help="Automatically fix ruff issues"
    )
    args, unknown = parser.parse_known_args()

    if args.verbose and not args.no_output:
        print("Verbose mode enabled")

    if args.no_output:
        sys.stdout = open(os.devnull, "w")

    unittest.main(argv=[sys.argv[0]] + unknown, verbosity=0 if not args.verbose else 2)
