from typing import Tuple
from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[str]:
        return data

    def part1(self, data: list[str]) -> int:
        return sum(
            result
            for result, *nums in (h.extract_numbers(line) for line in data)
            if self.is_valid(result, 0, tuple(nums))
        )

    def part2(self, data: list[str]) -> int:
        return sum(
            result
            for result, *nums in (h.extract_numbers(line) for line in data)
            if self.is_valid(result, 0, tuple(nums), can_concat=True)
        )

    def is_valid(
        self,
        result: int,
        current: int,
        numbers: Tuple[int, ...],
        can_concat: bool = False,
    ) -> bool:
        if current == result and not numbers:
            return True

        if not numbers or current > result:
            return False

        num, *remaining = numbers
        remaining_tuple = tuple(remaining)

        # Basic operations
        add = self.is_valid(result, current + num, remaining_tuple, can_concat)
        mult = self.is_valid(result, current * num, remaining_tuple, can_concat)

        # Concatenation
        if can_concat:
            concat_num = int(str(current) + str(num)) if current != 0 else num
            concat = self.is_valid(result, concat_num, remaining_tuple, can_concat)
            return add or mult or concat

        return add or mult
