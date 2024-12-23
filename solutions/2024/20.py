from utils.solution_base import SolutionBase
import utils.helper_functions as h
from collections import deque


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[list[str]]:
        return h.gridify(data)

    def part1(self, data: list[list[str]]) -> int:
        return self.solve_with_cheat(data, 2)

    def part2(self, data: list[list[str]]) -> int:
        return self.solve_with_cheat(data, 20)

    def get_distance_at_each_tile(
        self, grid: list[list[str]]
    ) -> dict[tuple[int, int], int]:
        start_pos = h.find_in_grid_or_error(grid, "S")
        end_pos = h.find_in_grid_or_error(grid, "E")

        queue = deque([(start_pos, {start_pos: 0})])
        seen_positions = set([start_pos])

        while queue:
            pos, path = queue.popleft()

            if pos == end_pos:
                path[pos] = len(path)
                return path

            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_pos = (pos[0] + dy, pos[1] + dx)

                if h.outside_grid(grid, new_pos[0], new_pos[1]):
                    continue

                if grid[new_pos[0]][new_pos[1]] == "#":
                    continue

                if new_pos in seen_positions:
                    continue

                path[new_pos] = len(path)
                queue.append((new_pos, path))
                seen_positions.add(new_pos)

        raise Exception("No path found")

    def get_possible_jumps_at(
        self, grid: list[list[str]], current_pos: tuple[int, int], cheat_distance: int
    ) -> set[tuple[int, tuple[int, int]]]:

        jumps = set()

        while cheat_distance > 1:
            for cheat_range in range(cheat_distance + 1):
                for dy, dx in [
                    (cheat_range, cheat_range - cheat_distance),
                    (cheat_range, -(cheat_range - cheat_distance)),
                    (-cheat_range, cheat_range - cheat_distance),
                    (-cheat_range, -(cheat_range - cheat_distance)),
                ]:
                    row = current_pos[0] + dy
                    col = current_pos[1] + dx

                    if h.outside_grid(grid, row, col):
                        continue

                    if grid[row][col] == "#":
                        continue

                    jumps.add((cheat_distance, (row, col)))

            cheat_distance -= 1

        return jumps

    def solve_with_cheat(self, grid: list[list[str]], cheat_distance: int) -> int:
        path = self.get_distance_at_each_tile(grid)

        time_savings = 100 if not self.is_test else 2 if self.is_part_1 else 50

        paths = set()

        for position, distance in path.items():
            for moves, cheat_position in self.get_possible_jumps_at(
                grid, position, cheat_distance
            ):
                if h.outside_grid(grid, *cheat_position):
                    continue

                if grid[cheat_position[0]][cheat_position[1]] == "#":
                    continue

                if path[cheat_position] - distance < time_savings + moves:
                    continue

                paths.add((position, cheat_position))

        return len(paths)
