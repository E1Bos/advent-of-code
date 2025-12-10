from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(self, data: list[str]) -> list[int]:
        return h.lmap(int, data)

    def part1(self, data: list[int]) -> int:
        parsed_disk: list[int] = []
        disk_ID = 0
        is_free_space = False

        for num in data:
            number_of_free = num
            if is_free_space:
                for _ in range(number_of_free):
                    parsed_disk.append(-1)
            else:
                for _ in range(number_of_free):
                    parsed_disk.append(disk_ID)
                disk_ID += 1

            is_free_space = not is_free_space

        left_pointer = 0
        right_pointer = len(parsed_disk) - 1

        while left_pointer < right_pointer:
            if parsed_disk[left_pointer] != -1:
                left_pointer += 1
                continue

            parsed_disk[left_pointer] = parsed_disk[right_pointer]
            parsed_disk[right_pointer] = -1
            right_pointer -= 1

        check_sum = 0
        for disk_id, char in enumerate(parsed_disk):
            if char != -1:
                check_sum += disk_id * int(char)

        return check_sum

    def part2(self, data: list[int]) -> int:
        files: dict[int, tuple[int, int]] = {}
        spaces: list[tuple[int, int]] = []

        file_id = 0
        position = 0

        for i, num in enumerate(data):
            if i % 2 == 0:
                if num == 0:
                    raise ValueError("Invalid input")

                files[file_id] = (position, num)
                file_id += 1
            else:
                if num != 0:
                    spaces.append((position, num))
            position += num

        while file_id > 0:
            file_id -= 1
            current_position, current_size = files[file_id]

            for i, (space_start, space_length) in enumerate(spaces):
                if space_start >= current_position:
                    spaces = spaces[:i]
                    break
                if current_size <= space_length:
                    files[file_id] = (space_start, current_size)

                    if current_size == space_length:
                        spaces.pop(i)
                    else:
                        spaces[i] = (
                            space_start + current_size,
                            space_length - current_size,
                        )
                    break

        total = 0
        for file_id, (position, size) in files.items():
            for i in range(position, position + size):
                total += file_id * i

        return total
