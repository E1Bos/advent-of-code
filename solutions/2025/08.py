from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[tuple[int, int, int]]:
        return_list: list[tuple[int, int, int]] = []
        for line in data:
            parts = tuple(map(int, line.split(",")))
            if len(parts) != 3:
                raise ValueError(f"Line '{line}' does not have exactly 3 integers.")
            return_list.append(parts)
        return return_list

    def part1(self, data: list[tuple[int, int, int]]) -> int:
        max_connections: int = 10 if self.is_test else 1000

        all_distances: list[
            tuple[float, tuple[int, int, int], tuple[int, int, int]]
        ] = []
        total_boxes: int = len(data)
        for box_one_index in range(total_boxes):
            for box_two_index in range(box_one_index + 1, total_boxes):
                dist = self.calculate_straight_line_distance(
                    data[box_one_index], data[box_two_index]
                )
                all_distances.append((dist, data[box_one_index], data[box_two_index]))

        all_distances.sort(key=lambda x: x[0])

        connections: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
        for box_one_index in range(min(len(all_distances), max_connections)):
            _, box1, box2 = all_distances[box_one_index]
            connections.append((box1, box2))

        chains: list[set[tuple[int, int, int]]] = []
        for pair in connections:
            found_indices: list[int] = []
            for index, chain in enumerate(chains):
                if pair[0] in chain or pair[1] in chain:
                    found_indices.append(index)

            if not found_indices:
                chains.append(set(pair))
            else:
                new_chain = set(pair)
                for index in sorted(found_indices, reverse=True):
                    new_chain.update(chains.pop(index))
                chains.append(new_chain)

        chain_lengths = [len(chain) for chain in chains]
        chain_lengths.sort(reverse=True)

        if len(chain_lengths) < 3:
            raise ValueError("Less than 3 chains found.")

        return chain_lengths[0] * chain_lengths[1] * chain_lengths[2]

    def part2(self, data: list[tuple[int, int, int]]) -> int:
        edges: list[tuple[float, int, int]] = []
        total_boxes: int = len(data)

        for box_one_index in range(total_boxes):
            for box_two_index in range(box_one_index + 1, total_boxes):
                dist = self.calculate_straight_line_distance(
                    data[box_one_index], data[box_two_index]
                )
                edges.append((dist, box_one_index, box_two_index))

        edges.sort(key=lambda x: x[0])

        parent = list(range(total_boxes))
        num_components = total_boxes

        def find(index: int) -> int:
            if parent[index] != index:
                parent[index] = find(parent[index])
            return parent[index]

        def union(element_a: int, element_b: int) -> bool:
            parent_a = find(element_a)
            parent_b = find(element_b)
            if parent_a != parent_b:
                parent[parent_a] = parent_b
                return True
            return False

        for _, source_box_index, second_box_index in edges:
            if union(source_box_index, second_box_index):
                num_components -= 1

                if num_components == 1:
                    box1 = data[source_box_index]
                    box2 = data[second_box_index]
                    return box1[0] * box2[0]

        raise ValueError("MST not completed; input may be invalid.")

    def calculate_straight_line_distance(
        self, point1: tuple[int, int, int], point2: tuple[int, int, int]
    ) -> float:
        return (
            (point1[0] - point2[0]) ** 2
            + (point1[1] - point2[1]) ** 2
            + (point1[2] - point2[2]) ** 2
        ) ** 0.5
