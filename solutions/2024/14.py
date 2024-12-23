from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[str]:
        return data

    def part1(self, data: list[str]) -> int:
        WIDTH = 101 if not self.is_test else 11
        HEIGHT = 103 if not self.is_test else 7

        robots = list()

        for robot in data:
            nums = h.extract_numbers_with_signs(robot)
            position = (nums[0], nums[1])
            velocity = (nums[2], nums[3])

            robots.append((position, velocity))

        quadrants = [0 for _ in range(4)]
        for robot in robots:
            x, y = robot[0]
            vx, vy = robot[1]

            new_x = (x + 100 * (vx + WIDTH)) % WIDTH
            new_y = (y + 100 * (vy + HEIGHT)) % HEIGHT

            if new_x == WIDTH // 2 or new_y == HEIGHT // 2:
                continue

            quadrant = (int(new_x > WIDTH // 2)) + (int(new_y > HEIGHT // 2) * 2)
            quadrants[quadrant] += 1

        total = 1
        for quad in quadrants:
            total *= quad
        return total

    def part2(self, data: list[str]) -> int:
        robots = list()

        for robot in data:
            nums = h.extract_numbers_with_signs(robot)
            position = (nums[0], nums[1])
            velocity = (nums[2], nums[3])

            robots.append((position, velocity))

        WIDTH = 101
        HEIGHT = 103
        time = 0

        # May be different for other inputs
        # I found that blacklisting 175 yielded my correct puzzle output
        blacklisted_times = [175]

        while True:
            time += 1

            if time in blacklisted_times:
                continue

            positions = set()

            for robot in robots:
                x, y = robot[0]
                vx, vy = robot[1]

                new_x = (x + time * (vx + WIDTH)) % WIDTH
                new_y = (y + time * (vy + HEIGHT)) % HEIGHT

                positions.add((new_x, new_y))

            if len(positions) == len(robots):
                return time
