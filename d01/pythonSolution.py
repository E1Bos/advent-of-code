import os


def calcDistance(point1: int, point2: int) -> int:
    return abs(point1 - point2)


def part1(lines) -> None:
    leftSide, rightSide = [], []
    for line in lines:
        split = [x.strip() for x in line.split(" ") if x != ""]
        leftNum, rightNum = int(split[0]), int(split[1])

        leftSide.append(leftNum)
        rightSide.append(rightNum)

    leftSide.sort()
    rightSide.sort()

    total = 0
    for i in range(len(leftSide)):
        total += calcDistance(leftSide[i], rightSide[i])

    print(f"Part 1: {total}")


def part2(lines) -> None:
    leftSide, similarityScore = [], {}
    for line in lines:
        split = [x.strip() for x in line.split(" ") if x != ""]

        leftNum, rightNum = int(split[0]), int(split[1])
        leftSide.append(leftNum)

        if rightNum in similarityScore:
            similarityScore[rightNum] += 1
        else:
            similarityScore[rightNum] = 1

    total = 0
    for i in range(len(leftSide)):
        number = leftSide[i]
        if number in similarityScore:
            total += similarityScore[number] * number

    print(f"Part 2: {total}")


def main():
    inputFilePath = os.path.join(os.path.dirname(__file__), "input.txt")

    if os.path.exists(inputFilePath):
        with open(inputFilePath, "r") as f:
            lines = f.readlines()
    else:
        print("Error: input.txt file does not exist")
        return

    part1(lines)
    part2(lines)


if __name__ == "__main__":
    main()
