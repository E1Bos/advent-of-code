import os

def parseInput(lines: str) -> list:
    return lines.splitlines()

def part1(lines: list) -> None:
    pass

def part2(lines: list) -> None:
    pass


def main():
    inputFilePath = os.path.join(os.path.dirname(__file__), "input.txt")

    if not os.path.exists(inputFilePath):
        print("Error: input file does not exist")
        return

    with open(inputFilePath, "r") as f:
        lines = parseInput(f.read())

    part1(lines)
    part2(lines)

if __name__ == "__main__":
    main()
