from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[str]:
        return data

    def part1(self, data: list[str]) -> int:
        return sum(1 for level in map(h.extract_numbers, data) if self.is_safe(level))

    def part2(self, data: list[str]) -> int:
        return sum(
            1
            for level in map(h.extract_numbers, data)
            if any(self.is_safe(level[:i] + level[i + 1 :]) for i in range(len(level)))
        )

    def is_safe(self, input: list[int]) -> bool:
        sorted_input = sorted(input)
        same_direction = (input == sorted_input) or (input[::-1] == sorted_input)

        is_good = True
        for i in range(len(input) - 1):
            difference = abs(input[i] - input[i + 1])
            if not 1 <= difference <= 3:
                is_good = False
                break

        return is_good and same_direction
