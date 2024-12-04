import os

def parse_input(lines: str) -> list:
    return lines.splitlines()

def part1(lines: list) -> None:
    pass

def part2(lines: list) -> None:
    pass


def main():
    input_file_path = os.path.join(os.path.dirname(__file__), "input.txt")

    if not os.path.exists(input_file_path):
        print("Error: input file does not exist")
        return

    with open(input_file_path, "r") as f:
        lines = parse_input(f.read())

    part1(lines)
    part2(lines)

if __name__ == "__main__":
    main()
