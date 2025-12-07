from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[list[str]]:
        return h.gridify(data)

    def part1(self, data: list[list[str]]) -> int:
        beam_start: tuple[int, int] = (data[0].index("S"), 0)

        beam_positions: set[tuple[int, int]] = set()
        beam_positions.add(beam_start)

        total_splits: int = 0

        while len(beam_positions) > 0:
            new_beam_positions: set[tuple[int, int]] = set()
            for pos in beam_positions:
                x, y = pos

                if y == len(data) - 1:
                    continue

                if data[y + 1][x] == ".":
                    new_beam_positions.add((x, y + 1))
                elif data[y + 1][x] == "^":
                    total_splits += 1
                    new_beam_positions.add((x - 1, y + 1))
                    new_beam_positions.add((x + 1, y + 1))
            beam_positions = new_beam_positions

        return total_splits

    def part2(self, data: list[list[str]]) -> int:
        beam_start: tuple[int, int] = (data[0].index("S"), 0)

        memo: dict[tuple[int, int], int] = {}
        total_splits: int = self.calculate_timeline_recursive(data, beam_start, memo)

        return total_splits

    def calculate_timeline_recursive(
        self,
        data: list[list[str]],
        current_beam_pos: tuple[int, int],
        memo: dict[tuple[int, int], int],
    ) -> int:
        if current_beam_pos in memo:
            return memo[current_beam_pos]

        x, y = current_beam_pos
        if y == len(data) - 1:
            memo[current_beam_pos] = 1
            return 1

        result: int = 0

        if data[y + 1][x] == ".":
            result = self.calculate_timeline_recursive(data, (x, y + 1), memo)
        elif data[y + 1][x] == "^":
            left_path = self.calculate_timeline_recursive(data, (x - 1, y + 1), memo)
            right_path = self.calculate_timeline_recursive(data, (x + 1, y + 1), memo)
            result = left_path + right_path

        memo[current_beam_pos] = result
        return result
