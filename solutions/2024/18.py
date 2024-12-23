from utils.solution_base import SolutionBase
import utils.helper_functions as h
from collections import deque


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[str]:
        return data

    def part1(self, data: list[str]) -> int:
        grid_size = 70 if not self.is_test else 6
        fallen_bytes = 1024 if not self.is_test else 12

        bad_spaces = [
            (bad_x, bad_y)
            for row in data[:fallen_bytes]
            for bad_x, bad_y in [h.extract_numbers(row)]
        ]

        steps = self.solve_grid(grid_size, bad_spaces)

        if steps is None:
            raise RuntimeError("No path found")

        return steps

    def part2(self, data: list[str]) -> str:
        grid_size = 70 if not self.is_test else 6

        all_bad_spaces = [
            (bad_x, bad_y) for row in data for bad_x, bad_y in [h.extract_numbers(row)]
        ]

        last_impossible = None
        left, right = 0, len(data)
        while left <= right:
            mid = (left + right) // 2

            steps = self.solve_grid(grid_size, all_bad_spaces[:mid])
            if steps == None:
                last_impossible = mid
                right = mid - 1
            else:
                left = mid + 1

        if last_impossible != None:
            bad_x, bad_y = h.extract_numbers(data[last_impossible - 1])
            return f"{bad_x},{bad_y}"

        raise RuntimeError("No corrupted bytes block the path to the exit")

    def solve_grid(
        self, grid_size: int, bad_spaces: list[tuple[int, int]]
    ) -> int | None:
        min_steps = None
        seen_positions = set()
        queue = deque([(0, 0, 0)])

        while queue:
            x, y, steps = queue.popleft()

            if x == grid_size and y == grid_size:
                min_steps = min(min_steps, steps) if min_steps is not None else steps
                continue

            if (y, x) in bad_spaces or h.outside_grid(grid_size + 1, x, y):
                continue

            if (x, y) in seen_positions:
                continue

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                queue.append((x + dx, y + dy, steps + 1))

            seen_positions.add((x, y))

        return min_steps
