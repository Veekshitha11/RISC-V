"""
Build a text graph of extension pairs that share at least one instruction.

The graph is built **instruction-first**: each mnemonic contributes edges
only among its own tag list, so every edge is backed by concrete shared
mnemonics. Iterating extension pairs first would not attach the right
evidence to each edge.
"""

from collections import defaultdict
from itertools import combinations

from src.parser import get_extensions


def build_extension_graph(
    instruction_data: dict,
) -> dict:
    """
    Return ``graph[ext_a][ext_b]`` as a set of shared mnemonics (lowercase).

    ``instruction_data`` is the full instruction dict. Instructions with
    fewer than two extensions after ``get_extensions`` are skipped.
    """

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
    """
    Render ``graph`` as plain text: neighbor counts and shared mnemonics.

    ``graph`` must match the structure produced by ``build_extension_graph``.
    """

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
