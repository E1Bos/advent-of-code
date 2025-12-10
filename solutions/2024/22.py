from utils.solution_base import SolutionBase
from collections import defaultdict


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[str]:
        return data

    def part1(self, data: list[str]) -> int:
        total: int = 0

        for num_str in data:
            number: int = int(num_str)

            for _ in range(2_000):
                number = (number ^ (number * 64)) % 16_777_216
                number = (number ^ (number // 32)) % 16_777_216
                number = (number ^ (number * 2048)) % 16_777_216
            total += number

        return total

    def part2(self, data: list[str]) -> int:
        data = data if not self.is_test else ["1", "2", "3", "2024"]

        profits: defaultdict[tuple[int, ...], int] = defaultdict(int)
        for num_str in data:
            number: int = int(num_str)

            changes_in_price: list[int] = []
            previous_price: int = number % 10
            seen_sequences: set[tuple[int, ...]] = set()

            for _ in range(2_000):
                number = (number ^ (number * 64)) % 16_777_216
                number = (number ^ (number // 32)) % 16_777_216
                number = (number ^ (number * 2_048)) % 16_777_216

                price: int = number % 10
                price_change: int = price - previous_price
                previous_price = price

                changes_in_price.append(price_change)

                if len(changes_in_price) < 4:
                    continue

                sequence: tuple[int, ...] = tuple(changes_in_price[-4:])

                if sequence in seen_sequences:
                    continue

                profits[sequence] += price

                seen_sequences.add(sequence)

        return max(profits.values())

    def evolve_number(self, number: int) -> int:
        """
        This was the method I was using to evolve the number in part1 and part2.
        However, making over ~800k function calls takes way too much time
        So the method is hard coded in each part
        """

        number = (number ^ (number * 64)) % 16_777_216
        number = (number ^ (number // 32)) % 16_777_216
        number = (number ^ (number * 2048)) % 16_777_216

        return number
