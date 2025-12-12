from typing import Callable
from utils.solution_base import SolutionBase
import utils.helper_functions as h
from collections import defaultdict
import networkx as nx  # type: ignore


class Solution(SolutionBase):
    raw_input: bool = True
    skip_empty_tests: bool = True

    compute: dict[str, Callable[[int, int], int]] = {
        "AND": lambda x, y: x & y,
        "OR": lambda x, y: x | y,
        "XOR": lambda x, y: x ^ y,
    }

    def parse(
        self, data: str
    ) -> tuple[defaultdict[str, int], dict[str, tuple[str, str, str]]]:
        wires_raw, commands_raw = h.split_groups(data)
        wires: defaultdict[str, int] = defaultdict(
            int, {v.strip(): int(x) for v, x in [s.split(":") for s in wires_raw]}
        )

        commands: dict[str, tuple[str, str, str]] = {}
        for command in commands_raw:
            in1, comp, in2, out = command.replace("->", " ").split()
            commands[out] = (in1, in2, comp)
        commands = dict(sorted(commands.items()))

        return wires, commands

    def part1(
        self, data: tuple[defaultdict[str, int], dict[str, tuple[str, str, str]]]
    ) -> int:
        wires, commands = data

        outputs: dict[str, int] = {}
        unprocessed_commands: set[str] = set(commands)

        while unprocessed_commands:
            for out in unprocessed_commands.copy():
                in1, in2, comp = commands[out]

                in1_val = wires.get(in1, None)
                in2_val = wires.get(in2, None)

                if in1_val is None or in2_val is None:
                    continue

                output = self.compute[comp](in1_val, in2_val)

                if out.startswith("z"):
                    outputs[out] = output
                else:
                    wires[out] = output

                unprocessed_commands.remove(out)

        sorted_outputs = sorted(outputs.items(), key=lambda x: x[0], reverse=True)

        return int("".join(str(output) for _, output in sorted_outputs), 2)

    def part2(
        self, data: tuple[defaultdict[str, int], dict[str, tuple[str, str, str]]]
    ) -> str:
        wires: dict[str, int]
        commands: dict[str, tuple[str, str, str]]
        wires, commands = data

        command_graph: nx.DiGraph[str] = nx.DiGraph(
            {dst: [src1, src2] for dst, (src1, src2, _) in commands.items()}
        )
        sorted_command_graph: list[str] = list(nx.topological_sort(command_graph))[::-1]

        for node in sorted_command_graph:
            if node in commands:
                wire1: str
                wire2: str
                operation: str
                wire1, wire2, operation = commands[node]
                wires[node] = self.compute[operation](wires[wire1], wires[wire2])

        operation_per_wire: defaultdict[str, set[str]] = defaultdict(set)
        for wire1, wire2, operation in commands.values():
            operation_per_wire[wire1].add(operation)
            operation_per_wire[wire2].add(operation)

        wrong_wires: set[str] = set()
        for output, (wire1, wire2, operation) in commands.items():
            if output.startswith("z") and operation != "XOR":
                self.debug("case 1")
                wrong_wires.add(output)
            elif operation == "XOR" and all(
                x[0] not in ("x", "y", "z") for x in (output[0], wire1[0], wire2[0])
            ):
                self.debug("case 2")
                wrong_wires.add(output)
            elif operation != "OR":
                if (operation == "AND") == ("OR" not in operation_per_wire[output]):
                    self.debug("case 3")
                    wrong_wires.add(output)
            self.debug(wrong_wires)

        self.debug(wrong_wires)

        return ",".join(
            sorted(
                wrong_wires
                - {
                    next(
                        output
                        for (output, (wire1, wire2, _)) in commands.items()
                        if "x00" in (wire1, wire2)
                    ),
                    "z45",
                }
            )
        )
