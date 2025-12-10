from utils.solution_base import SolutionBase
from collections import defaultdict


class Solution(SolutionBase):
    raw_input: bool = False

    def parse(self, data: list[str]) -> list[str]:
        return data

    def part1(self, data: list[str]) -> int:
        connections: defaultdict[str, list[str]] = defaultdict(list)
        for line in data:
            comp1, comp2 = line.split("-")
            connections[comp1] += [comp2]
            connections[comp2] += [comp1]

        groups_of_three: set[tuple[str, ...]] = set()
        for comp1 in connections:
            for comp2 in connections[comp1]:
                if comp2 == comp1:
                    continue
                for comp3 in connections[comp2]:
                    if comp3 != comp1 and comp1 in connections[comp3]:
                        group: tuple[str, ...] = tuple(sorted([comp1, comp2, comp3]))
                        groups_of_three.add(group)

        return sum(
            1
            for group in groups_of_three
            if any(comp.startswith("t") for comp in group)
        )

    def part2(self, data: list[str]) -> str:
        connections: defaultdict[str, list[str]] = defaultdict(list)

        for line in data:
            comp1, comp2 = line.split("-")
            connections[comp1].append(comp2)
            connections[comp2].append(comp1)

        def is_fully_connected(nodes: list[str]) -> bool:
            return all(
                all(
                    (node2 in connections[node1] and node1 in connections[node2])
                    for node2 in nodes
                    if node1 != node2
                )
                for node1 in nodes
            )

        groups: list[list[str]] = []
        remaining_groups: list[str] = sorted(list(connections.keys()))
        while remaining_groups:
            current_group: list[str] = [remaining_groups.pop(0)]
            changed = True

            while changed:
                changed = False

                for node in sorted(set(remaining_groups) - set(current_group)):
                    test_group = current_group + [node]

                    if is_fully_connected(test_group):
                        current_group.append(node)
                        changed = True

            groups.append(sorted(current_group))
            remaining_groups = [
                node for node in remaining_groups if node not in current_group
            ]

        largest_group = max(groups, key=len)
        return ",".join(sorted(largest_group))
