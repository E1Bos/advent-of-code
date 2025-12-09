from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[tuple[int, int]]:
        parsed: list[tuple[int, int]] = []
        for line in data:
            parts = tuple(map(int, line.split(",")))
            if len(parts) != 2:
                raise ValueError(f"Line '{line}' does not have exactly 2 integers.")
            parsed.append(parts)
        return parsed

    def part1(self, data: list[tuple[int, int]]) -> int:
        max_size: int = 0

        total_points = len(data)
        for p1_index in range(total_points):
            for p2_index in range(p1_index + 1, total_points):
                area = self.calculate_rectangle_area(data[p1_index], data[p2_index])

                if area <= max_size:
                    continue

                max_size = area

        return max_size

    def part2(self, data: list[tuple[int, int]]) -> int:
        total_size: int = len(data)

        edges: list[tuple[tuple[int, int], tuple[int, int]]] = []
        for index in range(total_size):
            point1 = data[index]
            point2 = data[(index + 1) % total_size]
            edges.append((point1, point2))

        max_area: int = 0

        for p1_index in range(total_size):
            for p2_index in range(p1_index + 1, total_size):
                point1: tuple[int, int] = data[p1_index]
                point2: tuple[int, int] = data[p2_index]

                min_x, max_x = min(point1[0], point2[0]), max(point1[0], point2[0])
                min_y, max_y = min(point1[1], point2[1]), max(point1[1], point2[1])

                area: int = (max_x - min_x + 1) * (max_y - min_y + 1)

                if area <= max_area:
                    continue

                inside_boundary: bool = True
                for (edge_x1, edge_y1), (edge_x2, edge_y2) in edges:
                    if edge_x1 == edge_x2:
                        edge_x = edge_x1
                        min_edge_y, max_edge_y = (
                            min(edge_y1, edge_y2),
                            max(edge_y1, edge_y2),
                        )

                        if min_x < edge_x < max_x:
                            if max(min_y, min_edge_y) < min(max_y, max_edge_y):
                                inside_boundary = False
                                break
                    else:
                        edge_y = edge_y1
                        min_edge_x, max_edge_x = (
                            min(edge_x1, edge_x2),
                            max(edge_x1, edge_x2),
                        )

                        if min_y < edge_y < max_y:
                            if max(min_x, min_edge_x) < min(max_x, max_edge_x):
                                inside_boundary = False
                                break

                if not inside_boundary:
                    continue

                midpoint_x: int = (min_x + max_x) // 2
                midpoint_y: int = (min_y + max_y) // 2

                intersections: int = 0
                for (edge_x1, edge_y1), (edge_x2, edge_y2) in edges:
                    if edge_x1 == edge_x2:
                        min_edge_y, max_edge_y = (
                            min(edge_y1, edge_y2),
                            max(edge_y1, edge_y2),
                        )
                        if min_edge_y <= midpoint_y < max_edge_y:
                            if edge_x1 > midpoint_x:
                                intersections += 1

                if intersections % 2 == 1:
                    max_area = area

        return max_area

    def calculate_rectangle_area(
        self, point1: tuple[int, int], point2: tuple[int, int]
    ) -> int:
        if point1 == point2:
            return 0

        width = abs(point1[0] - point2[0]) + 1
        height = abs(point1[1] - point2[1]) + 1

        return width * height
