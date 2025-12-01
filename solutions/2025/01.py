from utils.solution_base import SolutionBase

class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[int]:
        parsed: list[int] = []

        for line in data:
            if line.startswith("R"):
                parsed.append(int(line[1::]))
                continue
            
            parsed.append(-int(line[1::]))

        return parsed

    def part1(self, data: list[int]) -> int:
        current_dial: int = 50    
        solution: int = 0

        for line in data:
            if (line > 100) or (line < -100):
                line = line % 100

            current_dial += line

            if current_dial > 99:
                current_dial = current_dial - 100
            elif current_dial < 0:
                current_dial = 100 + current_dial

            if current_dial == 0:
                solution += 1
        
        return solution

    def part2(self, data: list[int]) -> int:
        current_dial: int = 50    
        solution: int = 0

        for line in data:
            next_dial = current_dial + line
            passed_zero = 0
            
            if line > 0:
                passed_zero = (next_dial // 100) - (current_dial // 100)
            elif line < 0:
                passed_zero = ((current_dial - 1) // 100) - ((next_dial - 1) // 100)
            
            solution += passed_zero
            current_dial = next_dial % 100
        
        return solution
