from utils.solution_base import SolutionBase
import utils.helper_functions as h
import re


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(self, data: str) -> str:
        return data

    def part1(self, data: str) -> int:
        total: int = 0
        for i in range(len(data)):
            instr = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", data[i:])

            if instr is not None:
                x, y = int(instr.group(1)), int(instr.group(2))
                total += x * y
        return total

    def part2(self, data: str) -> int:
        total: int = 0
        do: bool = True

        for i in range(len(data)):
            if data[i:].startswith("do()"):
                do = True

            if data[i:].startswith("don't()"):
                do = False

            instr = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", data[i:])

            if instr is not None and do is True:
                x, y = int(instr.group(1)), int(instr.group(2))
                total += x * y

        return total
