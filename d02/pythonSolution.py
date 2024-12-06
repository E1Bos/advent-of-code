import os


def isSafe(input: list[int]) -> bool:
    sortedInput = sorted(input)
    sameDirection = (input == sortedInput) or (input[::-1] == sortedInput)

    isGood = True
    for i in range(len(input) - 1):
        difference = abs(input[i] - input[i + 1])
        if not 1 <= difference <= 3:
            isGood = False
            break

    return isGood and sameDirection


def fastSolve(lines) -> None:
    levels = [list(map(int, line.split())) for line in lines]

    part1 = sum(1 for level in levels if isSafe(level))
    part2 = sum(
        1
        for level in levels
        if any(isSafe(level[:i] + level[i + 1 :]) for i in range(len(level)))
    )

    # Output
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


def oldSolve(lines) -> None:
    levels = [list(map(int, line.split())) for line in lines]

    part1 = 0
    part2 = 0
    for level in levels:
        # Part 1
        if isSafe(level):
            part1 += 1

        # Part 2
        safe = False
        for badNumber in range(len(levels)):
            newLevel = level[:badNumber] + level[badNumber + 1 :]
            if isSafe(newLevel):
                safe = True
                break

        if safe:
            part2 += 1


def main():
    inputFilePath = os.path.join(os.path.dirname(__file__), "input.txt")

    if os.path.exists(inputFilePath):
        with open(inputFilePath, "r") as f:
            lines = f.readlines()
    else:
        print("Error: input.txt file does not exist")
        return

    fastSolve(lines)


if __name__ == "__main__":
    main()
