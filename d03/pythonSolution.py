import os, re


def solve(text) -> None:
    part_1 = 0
    part_2 = 0
    do = True

    for i in range(len(text)):
        if text[i:].startswith("do()"):
            do = True

        if text[i:].startswith("don't()"):
            do = False

        instr = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", text[i:])

        if instr is not None:
            x, y = int(instr.group(1)), int(instr.group(2))
            part_1 += x * y
            if do:
                part_2 += x * y

    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")


def main():
    inputFilePath = os.path.join(os.path.dirname(__file__), "input.txt")

    if os.path.exists(inputFilePath):
        with open(inputFilePath, "r") as f:
            text = f.read()
    else:
        print("Error: input.txt file does not exist")
        return

    solve(text)


if __name__ == "__main__":
    main()
