import os


def parseInput(lines: str) -> tuple[dict[str, list[str]], list[list[str]]]:
    rules, updates = lines.split("\n\n")
    rules = rules.splitlines()
    updates = [line.split(",") for line in updates.splitlines()]

    rules_dict = {}
    for rule in rules:
        before, after = rule.split("|")

        before_list = rules_dict.get(before, [])
        before_list.append(after)
        rules_dict[before] = before_list

    return rules_dict, updates


def findInvalidPosition(
    update: list[str], rules: dict[str, list[str]]
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


def isValidRule(update: list[str], rules: dict[str, list[str]]) -> bool:
    return findInvalidPosition(update, rules) is None


def swapInvalid(update: list[str], rules: dict[str, list[str]]) -> None:
    while not isValidRule(update, rules):
        pos, must_be = findInvalidPosition(update, rules)
        before = update[:pos]
        update[pos], update[before.index(must_be)] = must_be, update[pos]


def solve(rules: dict[str, list[str]], updates: list[list[str]]) -> None:
    part_1 = 0
    part_2 = 0

    for update in updates:
        if isValidRule(update, rules):
            middle_char = update[len(update) // 2]
            part_1 += int(middle_char)
        else:
            swapInvalid(update, rules)
            middle_char = update[len(update) // 2]
            part_2 += int(middle_char)

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")


def main() -> None:
    inputFilePath = os.path.join(os.path.dirname(__file__), "input.txt")

    if os.path.exists(inputFilePath):
        with open(inputFilePath, "r") as f:
            lines = f.read()
    else:
        print("Error: input.txt file does not exist")
        return

    rules, updates = parseInput(lines)

    solve(rules, updates)


if __name__ == "__main__":
    main()
