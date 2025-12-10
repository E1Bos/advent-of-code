from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(self, data: str) -> tuple[list[list[int]], ...]:
        locks: list[list[int]] = []
        keys: list[list[int]] = []

        split_data = h.split_groups(data)
        for item in split_data:
            is_lock = False
            heights = [0 for _ in range(len(item[0]))]

            if all([char == "#" for char in item[0]]):
                is_lock = True

            for row in item[1:]:
                for col, char in enumerate(row):
                    if char == "#":
                        heights[col] += 1

            if is_lock:
                locks.append(heights)
            else:
                keys.append(heights)

        return locks, keys

    def part1(self, data: tuple[list[list[int]], ...]) -> int:
        locks, keys = data

        total_valid: int = 0

        for lock in locks:
            for key in keys:
                sum_heights: list[int] = [lock[i] + key[i] for i in range(len(lock))]

                if all([height <= 6 for height in sum_heights]):
                    total_valid += 1

        return total_valid
