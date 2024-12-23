from utils.solution_base import SolutionBase
import utils.helper_functions as h
from itertools import permutations


class Solution(SolutionBase):
    raw_input: bool = False

    POSITIONS: dict[str, tuple[int, int]] = {
        "7": (0, 0),
        "8": (0, 1),
        "9": (0, 2),
        "4": (1, 0),
        "5": (1, 1),
        "6": (1, 2),
        "1": (2, 0),
        "2": (2, 1),
        "3": (2, 2),
        "0": (3, 1),
        "A": (3, 2),
        "^": (0, 1),
        "a": (0, 2),
        "<": (1, 0),
        "v": (1, 1),
        ">": (1, 2),
    }

    DIRECTIONS: dict[str, tuple[int, int]] = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }

    memo = {}

    def parse(self, data: list[str]) -> list[str]:
        return data

    def part1(self, data: list[str]) -> int:
        total_directional_keypads = 2

        total = 0
        for sequence in data:
            sequence_length = self.solve_keypad(sequence, total_directional_keypads)
            total += sequence_length * int(h.extract_numbers_to_string(sequence))
        return total

    def part2(self, data: list[str]) -> int:
        total_directional_keypads = 25

        total = 0
        for sequence in data:
            sequence_length = self.solve_keypad(sequence, total_directional_keypads)
            total += sequence_length * int(h.extract_numbers_to_string(sequence))
        return total

    def moves_to_next_position(
        self,
        start_position: tuple[int, int],
        end_position: tuple[int, int],
        avoid: tuple[int, int] = (0, 0),
    ) -> list[str]:
        output = ""
        dx, dy = (
            end_position[0] - start_position[0],
            end_position[1] - start_position[1],
        )

        if dx < 0:
            output += "^" * abs(dx)
        else:
            output += "v" * dx
        if dy < 0:
            output += "<" * abs(dy)
        else:
            output += ">" * dy

        valid_moves = [
            "".join(p) + "a"
            for p in set(permutations(output))
            if not any(
                tuple(
                    sum(self.DIRECTIONS[move][dim] for move in p[:i])
                    + start_position[dim]
                    for dim in range(2)
                )
                == avoid
                for i in range(len(p))
            )
        ]

        return valid_moves if valid_moves else ["a"]

    def solve_keypad(
        self, sequence: str, total_layers: int = 2, current_depth: int = 0
    ) -> int:
        key = (sequence, current_depth, total_layers)

        if key in self.memo:
            return self.memo[key]

        empty_square = (3, 0) if current_depth == 0 else (0, 0)

        current_position = (
            self.POSITIONS["A"] if current_depth == 0 else self.POSITIONS["a"]
        )

        sequence_len = 0

        for char in sequence:
            next_position = self.POSITIONS[char]
            moves = self.moves_to_next_position(
                current_position, next_position, empty_square
            )
            if current_depth == total_layers:
                sequence_len += len(moves[0])
            else:
                sequence_len += min(
                    self.solve_keypad(move, total_layers, current_depth + 1)
                    for move in moves
                )
            current_position = next_position

        self.memo[key] = sequence_len
        return sequence_len
