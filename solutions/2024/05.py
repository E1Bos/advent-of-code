from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(self, data: str) -> tuple[dict[str, list[str]], list[list[str]]]:
        split = h.split_groups(data)
        rules = split[0]
        updates: list[list[str]] = [line.split(",") for line in split[1]]

        rules_dict: dict[str, list[str]] = {}
        for rule in rules:
            before, after = rule.split("|")

            before_list = rules_dict.get(before, [])
            before_list.append(after)
            rules_dict[before] = before_list

        return (rules_dict, updates)

    def part1(self, data: tuple[dict[str, list[str]], list[list[str]]]) -> int:
        total: int = 0

        rules, updates = data[0], data[1]

        for update in updates:
            if self.is_valid_rule(update, rules):
                middle_char = update[len(update) // 2]
                total += int(middle_char)

        return total

    def part2(self, data: tuple[dict[str, list[str]], list[list[str]]]) -> int:
        total: int = 0

        rules, updates = data[0], data[1]

        for update in updates:
            if self.is_valid_rule(update, rules):
                continue
            else:
                self.swap_invalid(update, rules)
                middle_char = update[len(update) // 2]
                total += int(middle_char)

        return total

    def find_invalid_position(
        self, update: list[str], rules: dict[str, list[str]]
    ) -> tuple[int, str] | None:
        for i in range(len(update)):
            current_num = update[i]
            if current_num in rules:
                before = update[:i]
                must_be_before = rules[current_num]

                for must_be in must_be_before:
                    if must_be in before:
                        return (i, must_be)
        return None

    def is_valid_rule(self, update: list[str], rules: dict[str, list[str]]) -> bool:
        return self.find_invalid_position(update, rules) is None

    def swap_invalid(self, update: list[str], rules: dict[str, list[str]]) -> None:
        while not self.is_valid_rule(update, rules):
            result = self.find_invalid_position(update, rules)

            if result is None:
                raise ValueError("Invalid data")

            pos, must_be = result

            before = update[:pos]
            update[pos], update[before.index(must_be)] = must_be, update[pos]
