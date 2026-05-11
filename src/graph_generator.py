# src/graph_generator.py

"""
Generate extension relationship graph
based on shared instructions.
"""

from collections import defaultdict
from itertools import combinations


def build_extension_graph(
    instruction_data: dict,
) -> dict:

    graph = defaultdict(set)

    for instruction_info in (
        instruction_data.values()
    ):

        extensions = instruction_info.get(
            "extension",
            []
        )

        # graph relationships only matter
        # when instructions belong to
        # multiple extensions
        if len(extensions) < 2:
            continue

        # create pairwise relationships
        for ext1, ext2 in combinations(
            extensions,
            2,
        ):

            graph[ext1].add(ext2)
            graph[ext2].add(ext1)

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

        connected_extensions = sorted(
            graph[extension]
        )

        lines.append(
            f"{extension} -> "
            f"{', '.join(connected_extensions)}"
        )

    return "\n".join(lines)