from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[list[int]]:
        return [[int(x) for x in line] for line in data]

    def part1(self, data: list[list[int]]) -> int:
        final_largest: list[int] = []

        for line in data:
            pick_largest: int = self.pick_largest(line, 2)
            final_largest.append(pick_largest)

        return sum(final_largest)

    def part2(self, data: list[list[int]]) -> int:
        final_largest: list[int] = []

        for line in data:
            pick_largest: int = self.pick_largest(line, 12)
            final_largest.append(pick_largest)

        return sum(final_largest)

    def pick_largest(self, data: list[int], digits_to_pick: int) -> int:
        num_digits: int = len(data)
        selected_digits: list[int] = []
        search_start: int = 0

        for pick_index in range(digits_to_pick):
            digits_left: int = digits_to_pick - pick_index - 1
            search_end: int = num_digits - digits_left

            max_digit: int = -1
            max_digit_index: int = search_start
            for i in range(search_start, search_end):
                if data[i] > max_digit:
                    max_digit = data[i]
                    max_digit_index = i

            selected_digits.append(max_digit)
            search_start = max_digit_index + 1

        result: list[int] = selected_digits
        combined: int = int("".join(str(d) for d in result))

        return combined
