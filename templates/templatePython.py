import os

def parseInput(input: str):
    pass

def part1(lines) -> None:
    pass

def part2(lines) -> None:
    pass


def main():
    input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")

    if os.path.exists(input_file_path):
        with open(input_file_path, "r") as f:
            lines = f.readlines()
    else:
        print("Error: input.txt file does not exist")
        return

    parsedInput = parseInput(lines)

    part1(parsedInput)
    part2(parsedInput)

if __name__ == "__main__":
    main()
