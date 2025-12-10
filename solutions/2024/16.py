from utils.solution_base import SolutionBase
import utils.helper_functions as h
from collections import deque
import sys


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[list[str]]:
        return h.gridify(data)

    def part1(self, data: list[list[str]]) -> int:
        start_row, start_col = h.find_in_grid_or_error(data, "S")
        facing = (0, 1)

        next_move: deque[tuple[int, int, tuple[int, int], int]] = deque(
            [(start_row, start_col, facing, 0)]
        )

        seen_positions: dict[tuple[int, int, tuple[int, int]], int] = dict()
        minval = sys.maxsize

        while next_move:
            row, col, facing, steps = next_move.popleft()

            if row < 0 or row >= len(data) or col < 0 or col >= len(data[0]):
                continue

            seen_steps = seen_positions.get((row, col, facing), None)

            if seen_steps is not None and seen_steps <= steps:
                continue

            char = data[row][col]

            if char == "E":
                minval = min(minval, steps)

            if char == "#":
                continue

            seen_positions[(row, col, facing)] = steps

            next_move.append((row + facing[0], col + facing[1], facing, steps + 1))

            left_direction = (facing[1], -facing[0])
            right_direction = (-facing[1], facing[0])

            next_move.append((row, col, left_direction, steps + 1000))
            next_move.append((row, col, right_direction, steps + 1000))

            seen_positions[(row, col, facing)] = steps

        return minval

    def part2(self, data: list[list[str]]) -> int:
        start_row, start_col = h.find_in_grid_or_error(data, "S")
        facing = (0, 1)

        next_move: deque[
            tuple[int, int, tuple[int, int], int, list[tuple[int, int]]]
        ] = deque([(start_row, start_col, facing, 0, [(start_row, start_col)])])

        minval = sys.maxsize
        best_path: set[tuple[int, int]] = set()

        seen_positions: dict[tuple[int, int, tuple[int, int]], int] = dict()
        while next_move:
            row, col, facing, steps, path = next_move.popleft()

            if row < 0 or row >= len(data) or col < 0 or col >= len(data[0]):
                continue

            seen_steps = seen_positions.get((row, col, facing), None)

            if seen_steps is not None and seen_steps < steps:
                continue

            char = data[row][col]

            if char == "E":
                if steps < minval:
                    best_path.clear()

                    minval = steps

                if steps == minval:
                    for row, col in path:
                        best_path.add((row, col))

            if char == "#":
                continue

            seen_positions[(row, col, facing)] = steps

            next_move.append(
                (
                    row + facing[0],
                    col + facing[1],
                    facing,
                    steps + 1,
                    path + [(row + facing[0], col + facing[1])],
                )
            )

            left_direction = (facing[1], -facing[0])
            right_direction = (-facing[1], facing[0])

            next_move.append(
                (row, col, left_direction, steps + 1000, path + [(row, col)])
            )
            next_move.append(
                (row, col, right_direction, steps + 1000, path + [(row, col)])
            )

        return len(best_path)
