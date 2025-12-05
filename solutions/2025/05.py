from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(self, data: str) -> tuple[list[tuple[int, int]], list[int]]:
        split_groups: list[list[str]] = h.split_groups(data)
        fresh_ranges: list[tuple[int, int]] = [
            (int(x.split("-")[0]), int(x.split("-")[1])) for x in split_groups[0]
        ]
        ids: list[int] = [int(x) for x in split_groups[1]]

        return fresh_ranges, ids

    def part1(self, data: tuple[list[tuple[int, int]], list[int]]) -> int:
        total: int = 0

        fresh_ranges, ids = data

        for id in ids:
            for fresh_range in fresh_ranges:
                min_id, max_id = fresh_range

                if min_id <= id <= max_id:
                    total += 1
                    break

        return total

    def part2(self, data: tuple[list[tuple[int, int]], list[int]]) -> int:
        fresh_ranges, _ = data

        did_merge: bool = True
        ranges: list[tuple[int, int]] = self.merge_similar_ranges(fresh_ranges)

        while did_merge:
            did_merge = False
            new_ranges = self.merge_similar_ranges(ranges)

            if len(new_ranges) != len(ranges):
                did_merge = True
                ranges = new_ranges

        total: int = 0
        for _, length in ranges:
            total += length + 1

        return total

    def merge_similar_ranges(
        self, ranges: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        ranges.sort()
        merged = []
        for interval in ranges:
            if not merged or merged[-1][1] < interval[0]:
                merged.append(list(interval))
            else:
                merged[-1][1] = max(merged[-1][1], interval[1])

        return list(set((start, end - start) for start, end in merged))
