from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[list[str]]:
        return h.gridify(data)

    def part1(self, data: list[list[str]]) -> int:
        total: int = 0

        for row in range(len(data)):
            for col in range(len(data[row])):
                cell: str = data[row][col]

                if cell == ".":
                    continue

                adjacent_str: list[str] = h.get_adjacent(
                    data, row, col, include_diagonal=True
                )

                adjacent_count: int = adjacent_str.count("@")

                if adjacent_count < 4:
                    total += 1

        return total

    def part2(self, data: list[list[str]]) -> int:
        total: int = 0

        grid_copy: list[list[str]] = [row.copy() for row in data]

        just_removed: bool = True
        while just_removed:
            just_removed = False

            for row in range(len(data)):
                for col in range(len(data[row])):
                    cell: str = data[row][col]

                    if cell == ".":
                        continue

                    adjacent_str: list[str] = h.get_adjacent(
                        data, row, col, include_diagonal=True
                    )

                    adjacent_count: int = adjacent_str.count("@")

                    if adjacent_count < 4:
                        total += 1
                        just_removed = True
                        grid_copy[row][col] = "."

            data = [row.copy() for row in grid_copy]

        return total
