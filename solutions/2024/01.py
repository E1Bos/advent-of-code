from utils.solution_base import SolutionBase
import utils.helper_functions as h
from collections import defaultdict


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[str]:
        return data

    def calculate_distance(self, point1: int, point2: int) -> int:
        return abs(point1 - point2)

    def part1(self, data: list[str]) -> int:
        left_side: list[int] = []
        right_side: list[int] = []

        for line in data:
            left_num, right_num = h.extract_numbers(line)
            left_side.append(left_num)
            right_side.append(right_num)

        left_side.sort()
        right_side.sort()

        total: int = 0
        for i in range(len(left_side)):
            total += self.calculate_distance(left_side[i], right_side[i])
        return total

    def part2(self, data: list[str]) -> int:
        left_side: list[int] = []
        similarity_score: defaultdict[int, int] = defaultdict(int)

        for line in data:
            left_num, right_num = h.extract_numbers(line)

            left_side.append(left_num)
            similarity_score[right_num] += 1

        total: int = 0
        for i in range(len(left_side)):
            number = left_side[i]
            total += similarity_score.get(number, 0) * number

        self.debug(similarity_score)

        return total
