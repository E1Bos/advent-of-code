from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[str]:
        return data

    def part1(self, data: list[str]) -> int:
        total_tokens = 0
        for index in range(0, len(data), 4):
            button_A = h.extract_numbers(data[index])
            button_B = h.extract_numbers(data[index + 1])
            goal = h.extract_numbers(data[index + 2])

            result = h.system_of_equation(button_A, button_B, goal)

            if result is not None:
                total_tokens += 3 * result[0] + result[1]

        return total_tokens

    def part2(self, data: list[str]) -> int:
        total_tokens = 0
        offset = 10_000_000_000_000
        for index in range(0, len(data), 4):
            button_A = h.extract_numbers(data[index])
            button_B = h.extract_numbers(data[index + 1])
            goal = h.extract_numbers(data[index + 2])

            goal = [goal[0] + offset, goal[1] + offset]

            result = h.system_of_equation(button_A, button_B, goal)

            if result is not None:
                total_tokens += 3 * result[0] + result[1]

        return total_tokens
