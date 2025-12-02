from utils.solution_base import SolutionBase
import utils.helper_functions as h
from typing import Any


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(self, data: list[str]) -> Any:
        parsed: list[str] = h.comma_separated(data)

        output: list[tuple[int, int]] = []

        for line in parsed:
            left, right = line.split("-")
            output.append((int(left), int(right)))

        return output

    def part1(self, data: list[int]) -> int:
        solution: int = 0

        for left, right in data:
            for number in range(left, right + 1):
                converted_num: str = str(number)

                if len(converted_num) % 2 != 0:
                    continue

                if h.is_repeated_substring(converted_num, num_substrings=2):
                    solution += number

        return solution

    def part2(self, data: list[int]) -> int:
        solution: int = 0

        for left, right in data:
            for number in range(left, right + 1):
                result = h.is_repeated_substring(str(number))

                if result:
                    solution += number

        return solution
