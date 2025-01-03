"""File containing the OutputHandler and Logger classes."""

# Built-in modules
from pathlib import Path
from logging import FileHandler, Formatter, DEBUG, INFO
from logging import Logger as _Logger

# Third-party modules
from rich.console import Console
from rich.logging import RichHandler


class Logger(_Logger):
    """Custom logger class that inherits from the built-in Python logger."""

    def __init__(
        self,
        name: str = __name__,
        console: Console | None = None,
        log_path: Path | None = None,
        stream_level: int = INFO,
        file_level: int = DEBUG,
    ) -> None:
        """
        Initialize a new logger instance.

        Args:
            console (Console, optional): An instance of the rich.console.Console class. Defaults to None.
            log_path (Path, optional): The path to the log file. Defaults to None.
            stream_level (int, optional): The logging level for the stream handler. Defaults to INFO.
            file_level (int, optional): The logging level for the file handler. Defaults to DEBUG.
        """
        super().__init__(name)

        if log_path and not log_path.parent.exists():
            log_path.parent.mkdir(parents=True)

        self.setLevel(DEBUG)

        # time_format = r"%I:%M:%S %p"
        time_format = "%H:%M:%S"
        stream_format = Formatter("%(name)s %(message)s", datefmt=time_format)
        file_format = Formatter(
            "%(asctime)s.%(msecs)03d - [%(name)s] - [%(levelname)s]:\t%(message)s",
            datefmt=time_format,
        )

        if console:
            stream_handler = RichHandler(console=console, level=stream_level)
            stream_handler.setFormatter(stream_format)
            self.addHandler(stream_handler)

        if log_path:
            file_handler = FileHandler(log_path)
            file_handler.setLevel(file_level)
            file_handler.setFormatter(file_format)
            self.addHandler(file_handler)


class OutputHandler:
    """
    Class to manage the output of the program.

    Attributes:
        console (Console): The rich console object to print messages to the terminal.
        logger (Logger): The logger object to log messages.
    """

    def __init__(
        self, console: Console | None = None, logger: Logger | None = None
    ) -> None:
        """
        Initialize a new OutputHandler instance.

        Args:
            console (Console, optional): An instance of the rich.console.Console class. Defaults to None.
            logger (Logger, optional): An instance of the Logger class. Defaults to None.
        """
        self.console = console if console else Console()
        self.logger = (
            logger
            if logger
            else Logger(
                name="main-runner",
                log_path=Path("logs/log.log"),
                file_level=INFO,
            )
        )

    def print_ok(self, *args, end: str = "\n\n", **kwargs) -> None:
        """
        Print an ok message to the console.
        """
        self.console.print(
            "[black on green] OK [/black on green]",
            *args,
            **kwargs,
            end=end,
            style="green",
        )

    def print_warning(self, *args, end: str = "\n\n", **kwargs) -> None:
        """Print a warning message to the console."""
        self.console.print(
            "[black on yellow] WARNING [/black on yellow]",
            *args,
            **kwargs,
            end=end,
            style="yellow",
        )

    def print_error(self, *args, end: str = "\n\n", **kwargs) -> None:
        """Print an error message to the console."""
        self.console.print(
            "[black on red] ERROR [/black on red]",
            *args,
            **kwargs,
            end=end,
            style="red",
        )

    def print_info(self, *args, end: str = "\n\n", **kwargs) -> None:
        """Print an info message to the console."""
        self.console.print(
            "[black on blue] INFO [/black on blue]",
            *args,
            **kwargs,
            end=end,
            style="blue",
        )

    def print(self, *args, **kwargs) -> None:
        """Print a message to the console using the rich library."""
        self.console.print(*args, **kwargs)

    def log(self, *args, **kwargs) -> None:
        """Log a message using the logger."""
        self.logger.log(*args, **kwargs)
