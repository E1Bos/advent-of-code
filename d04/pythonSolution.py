import os


def parseInput(lines) -> list[str]:
    return lines.splitlines()


def part1(lines) -> None:
    height = len(lines)
    width = len(lines[0])

    def checkDirection(row, col, rowDirection, colDirection) -> bool:
        if not (
            0 <= row + 3 * rowDirection < height and 0 <= col + 3 * colDirection < width
        ):
            return False

        word = ""
        for index in range(4):
            word += lines[row + index * rowDirection][col + index * colDirection]
        return word == "XMAS"

    total = 0
    for row in range(height):
        for col in range(width):
            directions = [
                (0, -1),  # left
                (0, 1),  # right
                (-1, 0),  # up
                (1, 0),  # down
                (-1, -1),  # up-left diagonal
                (-1, 1),  # up-right diagonal
                (1, -1),  # down-left diagonal
                (1, 1),  # down-right diagonal
            ]

            for rowDirection, colDirection in directions:
                if checkDirection(row, col, rowDirection, colDirection):
                    total += 1

    print(f"Part 1: {total}")


def part2(lines) -> None:
    height = len(lines)
    width = len(lines[0])

    def isValidCross(row, col) -> bool:
        if lines[row][col] != "A":
            return False

        upperLeft = lines[row - 1][col - 1]
        upperRight = lines[row - 1][col + 1]
        downLeft = lines[row + 1][col - 1]
        downRight = lines[row + 1][col + 1]
        return (
            sorted([upperLeft, upperRight, downLeft, downRight]) == ["M", "M", "S", "S"]
            and upperLeft != downRight
        )

    total = sum(
        isValidCross(r, c) for r in range(1, height - 1) for c in range(1, width - 1)
    )

    print(f"Part 2: {total}")


def main() -> None:
    inputFilePath = os.path.join(os.path.dirname(__file__), "input.txt")

    if os.path.exists(inputFilePath):
        with open(inputFilePath, "r") as f:
            lines = f.read()
    else:
        print("Error: input.txt file does not exist")
        return

    parsedInput = parseInput(lines)

    part1(parsedInput)
    part2(parsedInput)


if __name__ == "__main__":
    main()
