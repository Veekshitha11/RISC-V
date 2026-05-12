# tests/test_graph_generator.py

from src.graph_generator import (
    build_extension_graph,
    generate_graph_report,
)


def test_shared_instruction_creates_edge_with_mnemonic():

    data = {
        "andn": {
            "extension": [
                "rv_zbb",
                "rv_zk",
            ],
        },
    }

    graph = build_extension_graph(data)

    assert graph["rv_zbb"]["rv_zk"] == {"andn"}
    assert graph["rv_zk"]["rv_zbb"] == {"andn"}


def test_no_shared_instruction_means_empty_graph():

    data = {
        "add": {
            "extension": ["rv_i"],
        },
        "mul": {
            "extension": ["rv_m"],
        },
    }

    graph = build_extension_graph(data)

    assert len(graph) == 0


def test_graph_report_mentions_shared_mnemonic():

    data = {
        "andn": {
            "extension": ["rv_zbb", "rv_zk"],
        },
    }

    graph = build_extension_graph(data)
    text = generate_graph_report(graph)

    assert "ANDN" in text
    assert "shared:" in text
