from typing import Any
from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    DIRECTIONS: dict[str, tuple[int, int]] = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }
    ROTATIONS: dict[str, str] = {"^": ">", ">": "v", "v": "<", "<": "^"}

    def parse(self, data: list[str]) -> list[list[str]]:
        return h.gridify(data)

    def part1(self, data: list[list[str]]) -> int:
        return self.walk(data)

    def part2(self, data: list[list[str]]) -> int:
        guard_position = h.find_in_grid_or_error(data, "^")

        grid_copy = [row.copy() for row in data]

        total_loops = 0

        seen_moves, _ = self.walk(data, True)

        for block_row, block_col in seen_moves:
            if (block_row, block_col) == guard_position:
                continue

            changed_grid = [row[:] for row in grid_copy]
            changed_grid[block_row][block_col] = "#"

            _, is_loop = self.walk(changed_grid, True)

            if is_loop:
                total_loops += 1

        return total_loops

    def walk(self, data: list[list[str]], part2: bool = False) -> Any:
        seen_positions: set[tuple[int, int]] = set()

        guard_char = "^"
        guard_row, guard_col = h.find_in_grid_or_error(data, guard_char)
        original_guard_row, original_guard_col = guard_row, guard_col
        data[original_guard_row][original_guard_col] = "X"

        block_position: dict[str, bool] = {}
        is_loop = False

        while True:
            seen_positions.add((guard_row, guard_col))

            dx, dy = self.DIRECTIONS[guard_char]
            new_row, new_col = guard_row + dx, guard_col + dy

            if h.outside_grid(data, new_row, new_col):
                break

            if data[new_row][new_col] == "#":
                guard_char = self.ROTATIONS[guard_char]
                dict_key = f"{new_row},{new_col},{guard_char}"

                if part2 and block_position.get(dict_key, False):
                    is_loop = True
                    break
                else:
                    block_position[dict_key] = True
            else:
                guard_row, guard_col = new_row, new_col

            if is_loop and part2:
                break

        data[original_guard_row][original_guard_col] = "^"

        if not part2:
            return len(seen_positions)

        return seen_positions, is_loop
