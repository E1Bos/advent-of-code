from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(self, data: str) -> tuple[list[list[str]], str]:
        grid, moves = h.split_groups(data)
        grid = h.gridify(grid)
        moves = "".join(moves)
        return grid, moves

    def part1(self, data: tuple[list[list[str]], str]) -> int:
        grid, moves = data
        position = h.find_in_grid(grid, "@")

        if position is None:
            raise Exception("Robot not found")

        row, col = position

        for move in moves:
            direction_row = {"^": -1, "v": 1}.get(move, 0)
            direction_col = {"<": -1, ">": 1}.get(move, 0)

            new_row, new_col = row + direction_row, col + direction_col

            if grid[new_row][new_col] == "O":
                block_row, block_col = new_row, new_col
                while grid[block_row][block_col] == "O":
                    block_row, block_col = (
                        block_row + direction_row,
                        block_col + direction_col,
                    )
                    if (
                        block_row < 0
                        or block_row >= len(grid)
                        or block_col < 0
                        or block_col >= len(grid[0])
                    ):
                        break

                if grid[block_row][block_col] == ".":
                    prev_block = grid[block_row - direction_row][
                        block_col - direction_col
                    ]
                    while prev_block != "@":
                        grid[block_row][block_col] = "O"
                        block_row, block_col = (
                            block_row - direction_row,
                            block_col - direction_col,
                        )
                        grid[block_row][block_col] = "."
                        prev_block = grid[block_row - direction_row][
                            block_col - direction_col
                        ]

            if grid[new_row][new_col] == ".":
                grid[row][col] = "."
                grid[new_row][new_col] = "@"
                row, col = new_row, new_col

        return self.get_gps_sum(grid, "O")

    def part2(self, data: tuple[list[list[str]], str]) -> int:
        grid, moves = data
        grid = self.convert_to_double_grid(grid)
        position = h.find_in_grid(grid, "@")

        if position is None:
            raise Exception("Robot not found")

        row, col = position

        for move in moves:
            direction_row = {"^": -1, "v": 1}.get(move, 0)
            direction_col = {"<": -1, ">": 1}.get(move, 0)

            targets = [(row, col)]
            can_move = True

            for target_row, target_col in targets:
                new_row, new_col = (
                    target_row + direction_row,
                    target_col + direction_col,
                )

                if (new_row, new_col) in targets:
                    continue

                char = grid[new_row][new_col]

                if char == "#":
                    can_move = False
                    break
                if char == "[":
                    targets.append((new_row, new_col))
                    targets.append((new_row, new_col + 1))
                if char == "]":
                    targets.append((new_row, new_col))
                    targets.append((new_row, new_col - 1))

            if not can_move:
                continue

            grid_copy = [list(row) for row in grid]

            grid[row][col] = "."
            grid[row + direction_row][col + direction_col] = "@"

            for block_row, block_col in targets[1:]:
                grid[block_row][block_col] = "."
            for block_row, block_col in targets[1:]:
                grid[block_row + direction_row][block_col + direction_col] = grid_copy[
                    block_row
                ][block_col]

            row, col = row + direction_row, col + direction_col

        return self.get_gps_sum(grid, "[")

    def get_gps_sum(self, grid: list[list[str]], target: str) -> int:
        total = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == target:
                    total += 100 * row + col
        return total

    def convert_to_double_grid(self, grid: list[list[str]]) -> list[list[str]]:
        block_map = {
            "#": "##",
            "O": "[]",
            ".": "..",
            "@": "@.",
        }
        return [list("".join(block_map[c] for c in line)) for line in grid]
