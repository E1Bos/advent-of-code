from utils.solution_base import SolutionBase
import utils.helper_functions as h


class Solution(SolutionBase):
    raw_input: bool = True

    def parse(
        self, data: str
    ) -> tuple[dict[int, list[list[int]]], list[tuple[tuple[int, ...], list[int]]]]:
        split_input = h.split_groups(data)

        presents: dict[int, list[list[int]]] = {}
        for present in split_input[:-1]:
            index: int = int(present[0].removesuffix(":"))
            shape_str: list[str] = [
                line.replace("#", "1").replace(".", "0") for line in present[1:]
            ]

            shape: list[list[int]] = [[int(x) for x in line] for line in shape_str]

            presents[index] = shape

        regions: list[tuple[tuple[int, ...], list[int]]] = []
        for region in split_input[-1]:
            size_str, indexes_str = region.split(": ")

            size: tuple[int, ...] = tuple(int(x) for x in size_str.split("x"))
            indexes: list[int] = [int(x) for x in indexes_str.split(" ")]

            regions.append((size, indexes))

        return (presents, regions)

    def part1(
        self,
        data: tuple[
            dict[int, list[list[int]]], list[tuple[tuple[int, ...], list[int]]]
        ],
    ) -> int:
        presents, regions = data

        def get_area(shape: list[list[int]]) -> int:
            return sum(sum(row) for row in shape)

        total: int = 0

        for region_size, indexes in regions:
            shapes_data: list[tuple[list[list[list[int]]], int]] = []

            for index, amount in enumerate(indexes):
                if amount == 0:
                    continue

                shape = presents[index]
                rotations_set: set[tuple[tuple[int, ...], ...]] = set()
                current = shape
                for _ in range(4):
                    rotations_set.add(tuple(tuple(row) for row in current))
                    current = self.rotate_shape(current)

                rotations = [list(list(row) for row in rot) for rot in rotations_set]

                rotations.sort(key=get_area, reverse=True)

                shapes_data.append((rotations, amount))

            shapes_data.sort(
                key=lambda item: max(get_area(rotation) for rotation in item[0]),
                reverse=True,
            )

            if self.can_fit_shapes(shapes_data, region_size):
                total += 1

        return total

    def can_fit_shapes(
        self,
        shapes: list[tuple[list[list[list[int]]], int]],
        region_size: tuple[int, ...],
    ) -> bool:
        region_rows, region_cols = region_size
        number_of_cells: int = region_rows * region_cols

        total_area: int = 0
        for rotations, count in shapes:
            shape_area: int = sum(sum(row) for row in rotations[0])
            total_area += shape_area * count

        if total_area > number_of_cells:
            return False

        domains: list[dict[str, list[int] | int]] = []

        for rotations, count in shapes:
            valid_placements: set[int] = set()
            for shape in rotations:
                shape_height: int = len(shape)
                shape_width: int = len(shape[0])
                for row_start in range(region_rows - shape_height + 1):
                    for col_start in range(region_cols - shape_width + 1):
                        placement_mask: int = 0
                        for shape_row in range(shape_height):
                            for shape_col in range(shape_width):
                                if shape[shape_row][shape_col]:
                                    placement_mask |= 1 << (
                                        (row_start + shape_row) * region_cols
                                        + (col_start + shape_col)
                                    )
                        valid_placements.add(placement_mask)

            if not valid_placements:
                return False

            domains.append(
                {"placements": sorted(list(valid_placements)), "count": count}
            )

        def solve(current_domains: list[dict[str, list[int] | int]]) -> bool:
            if all(domain["count"] == 0 for domain in current_domains):
                return True

            best_domain_index: int = -1
            min_placements_count: float = float("inf")

            for domain_index, domain in enumerate(current_domains):
                if domain["count"] > 0:  # type: ignore
                    placements_count: int = len(domain["placements"])  # type: ignore
                    if placements_count == 0:
                        return False
                    if placements_count < min_placements_count:
                        min_placements_count = placements_count
                        best_domain_index = domain_index

            if best_domain_index == -1:
                return True

            target_domain: dict[str, list[int] | int] = current_domains[
                best_domain_index
            ]

            for current_placement in target_domain["placements"]:  # type: ignore
                next_domains: list[dict[str, list[int] | int]] = []
                is_possible: bool = True

                for domain_index, domain in enumerate(current_domains):
                    new_count: int = domain["count"]  # type: ignore
                    if domain_index == best_domain_index:
                        new_count -= 1

                    if new_count == 0:
                        next_domains.append({"placements": [], "count": 0})
                        continue

                    if domain_index == best_domain_index:
                        new_placements: list[int] = [
                            placement
                            for placement in domain["placements"]  # type: ignore
                            if placement > current_placement
                            and (placement & current_placement) == 0
                        ]
                    else:
                        new_placements: list[int] = [
                            placement
                            for placement in domain["placements"]  # type: ignore
                            if (placement & current_placement) == 0
                        ]

                    if not new_placements:
                        is_possible = False
                        break

                    next_domains.append(
                        {"placements": new_placements, "count": new_count}
                    )

                if is_possible:
                    if solve(next_domains):
                        return True

            return False

        return solve(domains)

    def rotate_shape(self, shape: list[list[int]]) -> list[list[int]]:
        return [list(reversed(col)) for col in zip(*shape)]
