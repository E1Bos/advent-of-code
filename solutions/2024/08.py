from utils.solution_base import SolutionBase
import utils.helper_functions as h
from collections import defaultdict


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[list[str]]:
        return h.gridify(data)

    def part1(self, data: list[list[str]]) -> int:
        return self.solve_antennas(data)

    def part2(self, data: list[list[str]]) -> int:
        return self.solve_antennas(data, True)

    def find_antennas(self, grid: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
        antennas: defaultdict[str, list[tuple[int, int]]] = defaultdict(list)
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] != ".":
                    antennas[grid[row][col]].append((row, col))
        return antennas

    def solve_antennas(self, grid: list[list[str]], part2: bool = False) -> int:
        part_1_antinodes: set[tuple[int, int]] = set()
        part_2_antinodes: set[tuple[int, int]] = set()

        antennas = self.find_antennas(grid)

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                for _, positions in antennas.items():
                    for antenna_1_row, antenna_1_col in positions:
                        for antenna_2_row, antenna_2_col in positions:
                            # Skip if the same antenna
                            if (antenna_1_row, antenna_1_col) == (
                                antenna_2_row,
                                antenna_2_col,
                            ):
                                continue

                            # Manhattan distances iirc
                            distance_1 = abs(row - antenna_1_row) + abs(
                                col - antenna_1_col
                            )
                            distance_2 = abs(row - antenna_2_row) + abs(
                                col - antenna_2_col
                            )

                            # Distances between the two antennae, row/col
                            distance_row_1 = row - antenna_1_row
                            distance_col_1 = col - antenna_1_col
                            distance_row_2 = row - antenna_2_row
                            distancecol_2 = col - antenna_2_col

                            # Add antinodes that are the same distance
                            if (
                                distance_row_1 * distancecol_2
                                == distance_col_1 * distance_row_2
                            ):
                                part_2_antinodes.add((row, col))

                                # Add antinodes that are 2x or 1/2x apart
                                if (
                                    distance_1 == 2 * distance_2
                                    or distance_1 * 2 == distance_2
                                ):
                                    part_1_antinodes.add((row, col))

        return len(part_2_antinodes) if part2 else len(part_1_antinodes)
