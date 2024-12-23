from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[str]:
        return data

    def part1(self, data: list[str]) -> int:
        height: int = len(data)
        width: int = len(data[0])

        def check_direction(row: int, col: int, row_dir: int, row_col: int) -> bool:
            if not (0 <= row + 3 * row_dir < height and 0 <= col + 3 * row_col < width):
                return False

            word: str = ""
            for index in range(4):
                word += data[row + index * row_dir][col + index * row_col]
            return word == "XMAS"

        total: int = 0
        for row in range(height):
            for col in range(width):
                directions = [
                    (0, -1),  # left
                    (0, 1),  # right
                    (-1, 0),  # up
                    (1, 0),  # down
                    (-1, -1),  # up-left diagonal
                    (-1, 1),  # up-right diagonal
                    (1, -1),  # down-left diagonal
                    (1, 1),  # down-right diagonal
                ]

                for row_dir, col_dir in directions:
                    if check_direction(row, col, row_dir, col_dir):
                        total += 1

        return total

    def part2(self, data: list[str]) -> int:
        def is_valid_cross(row: int, col: int) -> bool:
            if data[row][col] != "A":
                return False

            upper_left: str = data[row - 1][col - 1]
            upper_right: str = data[row - 1][col + 1]
            down_left: str = data[row + 1][col - 1]
            down_right: str = data[row + 1][col + 1]

            return (
                sorted([upper_left, upper_right, down_left, down_right])
                == ["M", "M", "S", "S"]
                and upper_left != down_right
            )

        return sum(
            is_valid_cross(r, c)
            for r in range(1, len(data) - 1)
            for c in range(1, len(data[0]) - 1)
        )
