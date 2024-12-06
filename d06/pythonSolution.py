import os

# Constants
DIRECTIONS: dict[str, tuple[int, int]] = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}
ROTATIONS: dict[str, str] = {"^": ">", ">": "v", "v": "<", "<": "^"}


def parseInput(lines: str) -> list[list[str]]:
    return [list(line) for line in lines.splitlines()]


def getGuardPosition(guardChar: str, lines: list[list[str]]) -> tuple[int, int]:
    for rowIdx, row in enumerate(lines):
        try:
            return rowIdx, row.index(guardChar)
        except ValueError:
            continue
    raise ValueError("Guard not found")


def isOutside(row: int, col: int, gridSize: tuple[int, int]) -> bool:
    return row < 0 or row >= gridSize[0] or col < 0 or col >= gridSize[1]


"""
def part1_old(
    lines: list[list[str]], stopIfNDupes: int | None = None
) -> tuple[list[list[str]], set[tuple[int, int]], int]:
    seenPositions: set[tuple[int, int]] = set()
    gridSize = (len(lines), len(lines[0]))

    # Set up
    guardChar = "^"
    guardRow, guardCol = getGuardPosition(guardChar, lines)
    originalGuardRow, originalGuardCol = guardRow, guardCol
    lines[originalGuardRow][originalGuardCol] = "X"

    timesSeen = 0
    while stopIfNDupes is None or timesSeen < stopIfNDupes:
        if (guardRow, guardCol) in seenPositions:
            timesSeen += 1
        seenPositions.add((guardRow, guardCol))

        # New position based on dict defined up top
        deltaX, deltaY = DIRECTIONS[guardChar]
        newRow, newCol = guardRow + deltaX, guardCol + deltaY

        # Check if the guard's next move will leave the grid (win or whatev)
        if isOutside(newRow, newCol, gridSize):
            break

        # Bump off the walls
        if lines[newRow][newCol] == "#":
            guardChar = ROTATIONS[guardChar]
        else:
            guardRow, guardCol = newRow, newCol

    # Fix the lines since I messed them up
    lines[originalGuardRow][originalGuardCol] = "^"
    return lines, seenPositions, timesSeen

@testSpeed
def part2_old(lines: list[list[str]], seenMoves: set[tuple[int, int]]) -> int:
    totalLoops = 0
    arbitraryNum = 900
    guardStart = getGuardPosition("^", lines)

    # Create a grid template
    templateGrid = [row.copy() for row in lines]

    for blockRow, blockCol in seenMoves:
        # Skip guard's starting position
        if (blockRow, blockCol) == guardStart:
            continue

        # Create a new grid
        testLines = [row.copy() for row in templateGrid]
        testLines[blockRow][blockCol] = "#"

        # Test this configuration
        _, _, timesSeen = part1_old(testLines, arbitraryNum)

        # Check if this creates a loop
        if timesSeen == arbitraryNum:
            totalLoops += 1

    return totalLoops

def solve_old(lines: list[list[str]]) -> None:
    # Run part 1
    lines, seenMoves, _ = part1_old(lines)
    print(f"Part 1: {len(seenMoves)}")

    # Run part 2
    part2Result = part2_old(lines, seenMoves)
    print(f"Part 2: {part2Result}")
"""


def part1(
    lines: list[list[str]], stopIfSameDirection: bool = False
) -> tuple[list[list[str]], set[tuple[int, int]], int]:
    seenPositions: set[tuple[int, int]] = set()
    gridSize = (len(lines), len(lines[0]))

    # Set up
    guardChar = "^"
    guardRow, guardCol = getGuardPosition(guardChar, lines)
    originalGuardRow, originalGuardCol = guardRow, guardCol
    lines[originalGuardRow][originalGuardCol] = "X"

    blockPosition: dict[tuple[int, int, str]] = {}
    isLoop = False

    while True:
        seenPositions.add((guardRow, guardCol))

        # New position based on dict defined up top
        deltaX, deltaY = DIRECTIONS[guardChar]
        newRow, newCol = guardRow + deltaX, guardCol + deltaY

        # Check if the guard's next move will leave the grid (win or whatev)
        if isOutside(newRow, newCol, gridSize):
            break

        # Bump off the walls
        if lines[newRow][newCol] == "#":
            guardChar = ROTATIONS[guardChar]
            dictKey = f"{newRow},{newCol},{guardChar}"

            if stopIfSameDirection and blockPosition.get(dictKey, False):
                isLoop = True
                break
            else:
                blockPosition[dictKey] = True
        else:
            guardRow, guardCol = newRow, newCol

    # Fix the lines since I messed them up
    lines[originalGuardRow][originalGuardCol] = "^"
    return lines, seenPositions, isLoop


def part2(lines: list[list[str]], seenMoves: set[tuple[int, int]]) -> int:
    guardStart = getGuardPosition("^", lines)

    # Create a grid template
    templateGrid = [row.copy() for row in lines]

    totalLoops = 0

    # Process moves in batches for better cache utilization
    for blockRow, blockCol in seenMoves:
        if (blockRow, blockCol) == guardStart:
            continue

        # Minimize copying by reusing the same grid
        testLines = [row[:] for row in templateGrid]
        testLines[blockRow][blockCol] = "#"

        # Only need the loop status
        if part1(testLines, True)[2]:
            totalLoops += 1

    return totalLoops


def solve(lines: list[list[str]]) -> None:
    # Run part 1
    lines, seenMoves, _ = part1(lines)
    print(f"Part 1: {len(seenMoves)}")

    # Run part 2
    part2Result = part2(lines, seenMoves)
    print(f"Part 2: {part2Result}")


def main() -> None:
    inputFilePath = os.path.join(os.path.dirname(__file__), "input.txt")

    if not os.path.exists(inputFilePath):
        print("Error: input file does not exist")
        return

    with open(inputFilePath) as f:
        lines = parseInput(f.read())

    # print("Running Old Solution")
    # solve_old(lines)

    # print("\nRunning New Solution")
    solve(lines)


if __name__ == "__main__":
    main()
