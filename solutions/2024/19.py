from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(self, data: str) -> tuple[list[str], list[str]]:
        base_towels, patterns = h.split_groups(data)
        base_towels: list[str] = h.comma_separated(base_towels[0])
        return base_towels, patterns

    def part1(self, data: tuple[list[str], list[str]]) -> int:
        base_towels, patterns = data

        return sum(
            self.is_possible(pattern, base_towels, dict()) for pattern in patterns
        )

    def part2(self, data: tuple[list[str], list[str]]) -> int:
        base_towels, patterns = data

        return sum(self.num_ways(pattern, base_towels, dict()) for pattern in patterns)

    def is_possible(
        self, pattern: str, base_towels: list[str], memo: dict[str, bool]
    ) -> bool:
        if pattern in memo:
            return memo[pattern]

        if len(pattern) == 0:
            return True

        for elem in base_towels:
            if pattern.startswith(elem) and self.is_possible(
                pattern[len(elem) :], base_towels, memo
            ):
                memo[pattern] = True
                return True

        memo[pattern] = False
        return False

    def num_ways(
        self, pattern: str, base_towels: list[str], memo: dict[str, int]
    ) -> int:
        if pattern in memo:
            return memo[pattern]

        if len(pattern) == 0:
            return 1

        permutations = 0
        for towel in base_towels:
            if pattern.startswith(towel):
                permutations += self.num_ways(pattern[len(towel) :], base_towels, memo)

        memo[pattern] = permutations

        return permutations
