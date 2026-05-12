# src/graph_generator.py

"""
Generate extension relationship graph
based on shared instructions.
"""

from collections import defaultdict
from itertools import combinations

from src.parser import get_extensions


def build_extension_graph(
    instruction_data: dict,
) -> dict:

    graph = defaultdict(lambda: defaultdict(set))

    for mnemonic, instruction_info in instruction_data.items():

        extensions = get_extensions(instruction_info)

        if len(extensions) < 2:
            continue

        name = mnemonic.lower()
        uniq = sorted(set(extensions))

        for ext1, ext2 in combinations(uniq, 2):
            graph[ext1][ext2].add(name)
            graph[ext2][ext1].add(name)

    return graph


def generate_graph_report(
    graph: dict,
) -> str:

    lines = []

    lines.append(
        "Extension Relationship Graph"
    )

    lines.append("-" * 55)

    for extension in sorted(graph):

        neighbors = graph[extension]
        nbr_list = sorted(neighbors)

        lines.append(
            f"{extension} | {len(nbr_list)} neighbor(s)"
        )

        for nbr in nbr_list:
            shared = ", ".join(
                m.upper() for m in sorted(neighbors[nbr])
            )
            lines.append(
                f"  -> {nbr} | shared: {shared}"
            )

    return "\n".join(lines)
