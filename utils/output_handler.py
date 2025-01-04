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

    def __init__(self, logger: Logger, console: Console | None = None) -> None:
        """
        Initialize a new OutputHandler instance.

        Args:
            logger (Logger): An instance of the Logger class.
            console (Console, optional): An instance of the rich.console.Console class. Defaults to None.
        """
        self.logger = logger
        self.console = console if console else Console()

    def print_ok(self, *args, end: str = "\n\n", **kwargs) -> None:
        """
        Print an ok message to the console.
        """
        self.__print_with_block("OK", "green", *args, **kwargs)

    def print_warning(self, *args, **kwargs) -> None:
        """Print a warning message to the console."""
        self.__print_with_block("WARNING", "yellow", *args, **kwargs)

    def print_error(self, *args, **kwargs) -> None:
        """Print an error message to the console."""
        self.__print_with_block("ERROR", "red", *args, **kwargs)

    def print_info(self, *args, **kwargs) -> None:
        """Print an info message to the console."""
        self.__print_with_block("INFO", "blue", *args, **kwargs)

    def __print_with_block(
        self, block_text: str, block_color: str, *args, **kwargs
    ) -> None:
        """Print a message with a colored block to the console."""
        self.console.print(
            f"[black on {block_color}] {block_text} [/black on {block_color}]",
            *args,
            **kwargs,
            style=block_color,
        )

    def print(self, *args, **kwargs) -> None:
        """Print a message to the console using the rich library."""
        self.console.print(*args, **kwargs)

    def log(self, *args, **kwargs) -> None:
        """Log a message using the logger."""
        self.logger.log(*args, **kwargs)
