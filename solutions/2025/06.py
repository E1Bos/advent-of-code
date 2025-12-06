from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[str]:
        return data

    def part1(self, data: list[str]) -> int:
        problems: list[list[int]] = []
        operations: list[str] = [op for op in data[-1].split(" ") if op != ""]

        for line in data:
            extracted_numbers: list[int] = h.extract_numbers(line)

            if not extracted_numbers:
                continue

            problems.append(extracted_numbers)

        total: int = 0

        for index in range(len(operations)):
            operation: str = operations[index]

            operation_total: int = 0 if operation == "+" else 1

            for problem in problems:
                if operation == "+":
                    operation_total += problem[index]
                else:
                    operation_total *= problem[index]

            total += operation_total

        return total

    def part2(self, data: list[str]) -> int:
        problems: list[list[str]] = []

        operations: list[str] = [op for op in data[-1].split(" ") if op != ""][::-1]
        operations_with_whitespace: list[str] = [
            "" for _ in data[-1].split(" ") if _ != ""
        ]

        pointer = 0
        op_index = 0
        while pointer < len(data[-1]):
            operations_with_whitespace[op_index] += data[-1][pointer]
            pointer += 1

            if pointer < len(data[-1]) and data[-1][pointer] != " ":
                op_index += 1
                operations_with_whitespace[op_index - 1] = operations_with_whitespace[
                    op_index - 1
                ][:-1]

        for line in data:
            groups: list[str] = []
            problem_index = 0
            char_index = 0
            while char_index < len(line):
                number_length = len(operations_with_whitespace[problem_index])

                group = line[char_index : char_index + number_length]
                if len(group) == number_length:
                    groups.append(group)
                    problem_index += 1
                char_index += number_length + 1
            if not groups:
                continue

            if not any(group.strip().isdigit() for group in groups):
                continue

            problems.append(groups)

        reordered_problems: list[list[str]] = [[] for _ in range(len(operations))]
        for char_index in range(len(operations)):
            for problem in problems:
                reordered_problems[char_index].append(problem[char_index])

        reordered_problems = reordered_problems[::-1]

        fixed_problems: list[list[int]] = [[] for _ in range(len(operations))]
        for char_index, problem in enumerate(reordered_problems):
            max_length: int = max(len(num) for num in problem)

            for number_index in range(0, max_length):
                updated_number_str: str = ""

                reverse_index = max_length - number_index - 1
                for num in problem:
                    updated_number_str += num[reverse_index]

                fixed_problems[char_index].append(int(updated_number_str))

        total: int = 0
        for index in range(len(operations)):
            operation: str = operations[index]

            operation_total: int = 0 if operation == "+" else 1
            final_problem: list[int] = fixed_problems[index]

            for number in final_problem:
                if operation == "+":
                    operation_total += number
                else:
                    operation_total *= number

            total += operation_total

        return total
