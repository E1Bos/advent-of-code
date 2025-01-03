from dataclasses import dataclass


@dataclass
class Args:
    year: int
    day: int
    part: int = 1
    copy_result: bool = False
    run_all: bool = False
    only_test: bool = False
    skip_test: bool = False
    create: bool = False
    timeit: bool = False
    profile: bool = False
    debug: bool = False

    @property
    def year_str(self) -> str:
        return str(self.year)

    @property
    def day_str(self) -> str:
        return str(self.day).zfill(2)
