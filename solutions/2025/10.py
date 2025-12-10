from utils.solution_base import SolutionBase
from collections import deque
import z3  # {z3-solver} #type: ignore

# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright:  reportAttributeAccessIssue=false


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(
        self, data: list[str]
    ) -> list[tuple[list[bool], list[list[int]], list[int]]]:
        parsed_data: list[tuple[list[bool], list[list[int]], list[int]]] = []

        for line in data:
            final_state_str, rest = line.split(" ", 1)
            buttons_str, joltage_str = rest.rsplit(" ", 1)

            final_state: list[bool] = [x == "#" for x in final_state_str[1:-1]]

            buttons: list[list[int]] = []
            for button_str in buttons_str[1:-1].split(") ("):
                button: list[int] = [int(x) for x in button_str.split(",")]
                buttons.append(button)

            joltage: list[int] = [int(x) for x in joltage_str[1:-1].split(",")]

            parsed_data.append((final_state, buttons, joltage))

        return parsed_data

    def part1(self, data: list[tuple[list[bool], list[list[int]], list[int]]]) -> int:
        total: int = 0

        for target_state, buttons, _ in data:
            total += self.find_shortest_solution_p1(target_state, buttons)

        return total

    def part2(self, data: list[tuple[list[bool], list[list[int]], list[int]]]) -> int:
        total: int = 0

        for _, buttons, target_state in data:
            total += self.find_shortest_solution_p2(target_state, buttons)

        return total

    def find_shortest_solution_p1(
        self,
        final_state: list[bool],
        buttons: list[list[int]],
    ) -> int:
        memo: dict[tuple[bool, ...], int] = dict()

        queue: deque[tuple[list[bool], int]] = deque()
        queue.append(([False for _ in range(len(final_state))], 0))

        while queue:
            state, presses = queue.popleft()
            state_key = tuple(state)

            if state_key in memo:
                continue

            if state == final_state:
                return presses

            memo[state_key] = presses
            for button in buttons:
                new_state = self.flip_button(state, button)
                queue.append((new_state, presses + 1))

        return -1

    def find_shortest_solution_p2(
        self,
        final_joltage: list[int],
        buttons: list[list[int]],
    ) -> int:
        optimizer: z3.Optimize = z3.Optimize()

        button_count_vars: list[z3.ArithRef] = [
            z3.Int(f"b_{i}") for i in range(len(buttons))
        ]

        for count in button_count_vars:
            optimizer.add(count >= 0)

        num_indices: int = len(final_joltage)
        for index in range(num_indices):
            expr = z3.Sum(
                [
                    button_count_vars[index2]
                    for index2, btn_indices in enumerate(buttons)
                    if index in btn_indices
                ]
            )
            optimizer.add(expr == final_joltage[index])

        total_presses = z3.Sum(button_count_vars)
        optimizer.minimize(total_presses)

        if optimizer.check() == z3.sat:
            model = optimizer.model()
            return model.eval(total_presses).as_long()
        else:
            return -1

    def flip_button(self, state: list[bool], button: list[int]) -> list[bool]:
        new_state: list[bool] = state.copy()
        for index in button:
            new_state[index] = not new_state[index]

        return new_state
