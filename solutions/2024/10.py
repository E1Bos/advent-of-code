from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[list[int]]:
        return h.gridify_ints(data)

    def part1(self, data: list[list[int]]) -> int:
        total_distinct = list()

        for row in range(len(data)):
            for col in range(len(data[row])):
                if data[row][col] != 0:
                    continue

                nines_in_route = self.find_total_distance(data, row, col, set())
                for n in nines_in_route:
                    total_distinct.append(n)

        return len(total_distinct)

    def part2(self, data: list[list[int]]) -> int:
        total_routes = 0

        for row in range(len(data)):
            for col in range(len(data[row])):
                if data[row][col] != 0:
                    continue

                total_routes += self.find_total(data, row, col)

        return total_routes

    def find_total_distance(
        self, grid: list[list[int]], row: int, col: int, nines: set[tuple[int, int]]
    ) -> set[tuple[int, int]]:
        possible_routes = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

        current_num = grid[row][col]

        if current_num == 9:
            nines.add((row, col))
            return nines

        for row, col in possible_routes:
            if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
                continue

            if grid[row][col] - current_num == 1:
                nines = self.find_total_distance(grid, row, col, nines)

        return nines

    def find_total(self, grid: list[list[int]], row: int, col: int) -> int:
        possible_routes = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

        current_num = grid[row][col]

        if current_num == 9:
            return 1

        total = 0
        for row, col in possible_routes:
            if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
                continue

            if grid[row][col] - current_num == 1:
                total += self.find_total(grid, row, col)

        return total
