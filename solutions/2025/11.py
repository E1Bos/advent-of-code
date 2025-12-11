from utils.solution_base import SolutionBase
from collections import deque


class Solution(SolutionBase):
    raw_input: bool = False
    skip_empty_tests: bool = True

    def parse(self, data: list[str]) -> dict[str, list[str]]:
        parsed: dict[str, list[str]] = {}

        for line in data:
            conn_name, connections_str = line.split(": ", 1)
            connections: list[str] = connections_str.split(" ")
            parsed[conn_name] = connections

        return parsed

    def part1(self, data: dict[str, list[str]]) -> int:
        total: int = 0

        queue: deque[str] = deque()
        queue.append("you")

        while queue:
            current: str = queue.popleft()

            if current == "out":
                total += 1
                continue

            queue.extend(data[current])

        return total

    def part2(self, data: dict[str, list[str]]) -> int:
        memo: dict[tuple[str, bool, bool], int] = {}

        def recursive_search(current: str, visited_dac: bool, visited_fft: bool) -> int:
            key = (current, visited_dac, visited_fft)
            if key in memo:
                return memo[key]

            if current == "out":
                if visited_dac and visited_fft:
                    return 1
                else:
                    return 0

            if current == "dac":
                visited_dac = True
            if current == "fft":
                visited_fft = True

            count = 0
            for neighbor in data[current]:
                count += recursive_search(neighbor, visited_dac, visited_fft)

            memo[key] = count
            return count

        return recursive_search("svr", False, False)
