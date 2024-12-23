from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    DIRECTIONS = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]

    def parse(self, data: list[str]) -> list[list[str]]:
        return h.gridify(data)

    # Honestly I cannot be bothered to separate part1 and part2.
    # They'll be done together idm
    def solve_farm(self, grid: list[list[str]], part2: bool = False) -> int:
        part_1: int = 0
        part_2: int = 0

        seen_areas: set[tuple[int, int]] = set()

        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if (row, col) in seen_areas:
                    continue

                curr_crop_area: int = 0
                curr_crop_perimeter: int = 0
                crop_areas: list[tuple[int, int]] = [(row, col)]
                crop_perimiters: dict[tuple[int, int], set[tuple[int, int]]] = dict()

                while len(crop_areas) > 0:
                    row, col = crop_areas.pop()

                    if (row, col) in seen_areas:
                        continue

                    seen_areas.add((row, col))
                    crop_type = grid[row][col]
                    curr_crop_area += 1

                    for direction_row, direction_col in self.DIRECTIONS:
                        new_row = row + direction_row
                        new_col = col + direction_col

                        if (
                            not h.outside_grid(grid, new_row, new_col)
                            and grid[new_row][new_col] == crop_type
                        ):
                            crop_areas.append((new_row, new_col))
                        else:
                            curr_crop_perimeter += 1
                            if (direction_row, direction_col) not in crop_perimiters:
                                crop_perimiters[(direction_row, direction_col)] = set()
                            crop_perimiters[(direction_row, direction_col)].add(
                                (row, col)
                            )

                sides = 0
                for position in crop_perimiters.values():
                    seen_perimiters = set()

                    for row, col in position:
                        if (row, col) in seen_perimiters:
                            continue

                        sides += 1
                        are_perimiters: list[tuple[int, int]] = [(row, col)]
                        while len(are_perimiters) > 0:
                            row, col = are_perimiters.pop()

                            if (row, col) in seen_perimiters:
                                continue

                            seen_perimiters.add((row, col))

                            for direction_row, direction_col in self.DIRECTIONS:
                                new_row = row + direction_row
                                new_col = col + direction_col

                                if (new_row, new_col) in position:
                                    are_perimiters.append((new_row, new_col))

                part_1 += curr_crop_area * curr_crop_perimeter
                part_2 += curr_crop_area * sides

        return part_2 if part2 else part_1

    def part1(self, data: list[list[str]]) -> int:
        return self.solve_farm(data)

    def part2(self, data: list[list[str]]) -> int:
        return self.solve_farm(data, True)
