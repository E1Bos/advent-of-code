from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(self, data: str) -> list[int]:
        return h.extract_numbers(data)

    def part1(self, data: list[int]) -> int:
        total = 0

        for stone in data:
            total += self.calculate_final(stone, 25)

        return total

    def part2(self, data: list[int]) -> int:
        total = 0

        for stone in data:
            total += self.calculate_final(stone, 75)

        return total

    split_dict: dict[int, tuple[int, int]] = dict()
    seen_dict: dict[tuple[int, int], int] = dict()

    def split_number(self, num: int) -> tuple[int, int]:
        if num in self.seen_dict:
            return self.split_dict[num]

        strNum = str(num)
        left = strNum[: len(strNum) // 2]
        right = strNum[len(strNum) // 2 :]

        result = (int(left), int(right))

        self.split_dict[num] = result
        return result

    def calculate_final(self, number: int, blinks: int) -> int:
        if (number, blinks) in self.seen_dict:
            return self.seen_dict[(number, blinks)]

        if blinks == 0:
            result = 1
        elif number == 0:
            result = self.calculate_final(1, blinks - 1)
        elif len(str(number)) % 2 == 0:
            first_half, second_half = self.split_number(number)
            result = self.calculate_final(
                first_half, blinks - 1
            ) + self.calculate_final(second_half, blinks - 1)
        else:
            result = self.calculate_final(number * 2024, blinks - 1)

        self.seen_dict[(number, blinks)] = result
        return result
