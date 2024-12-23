from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(self, data: str) -> tuple[dict[str, int], list[int]]:
        register_data, program_data = h.split_groups(data)
        registers: dict[str, int] = {
            "A": h.extract_numbers(register_data[0])[0],
            "B": h.extract_numbers(register_data[1])[0],
            "C": h.extract_numbers(register_data[2])[0],
        }
        program = h.extract_numbers(program_data[0])

        return registers, program

    def get_output(self, registers: dict[str, int], program: list[int]) -> list[int]:
        program_pointer = 0
        A, B, C = registers["A"], registers["B"], registers["C"]

        output = []

        while program_pointer < len(program):

            def get_operand_meaning(operand):
                if operand >= 7:
                    raise ValueError("Invalid operand")

                if operand == 4:
                    return A
                elif operand == 5:
                    return B
                elif operand == 6:
                    return C

                return operand

            opcode = program[program_pointer]
            operand_literal = program[program_pointer + 1]
            operand = get_operand_meaning(operand_literal)

            match opcode:
                case 0:
                    A = A >> operand
                case 1:
                    B = B ^ operand_literal
                case 2:
                    B = operand % 8
                case 3:
                    if A != 0:
                        program_pointer = operand_literal - 2
                case 4:
                    B = B ^ C
                case 5:
                    output.extend([num for num in str(operand % 8)])
                case 6:
                    B = A >> operand
                case 7:
                    C = A >> operand

            program_pointer += 2

        return [int(num) for num in output]

    def part1(self, data: tuple[dict[str, int], list[int]]) -> str:
        registers, program = data
        output = self.get_output(registers, program)

        return ",".join([str(num) for num in output])

    def part2(self, data: tuple[dict[str, int], list[int]]) -> int | str:
        debug = False

        registers, program = data
        a_value = 0
        best = 0

        while True:
            a_value += 1
            # a_reg = a_value
            # a_reg = a_value * 8**correct_values + offset
            # This value will be different for every person
            a_reg = a_value * 8**14 + 0o00532756025052

            registers["A"] = a_reg

            output = self.get_output(registers, program)

            if output == program:
                return a_reg

            if debug:
                counter = 0
                for expected, curr in zip(program, output):
                    if expected != curr:
                        break

                    counter += 1

                if counter > best:
                    best = counter
                    print(f"{a_value=}, {a_reg=}, {oct(a_reg)=}, {best=}")
                    print(output)
                    print(program)
