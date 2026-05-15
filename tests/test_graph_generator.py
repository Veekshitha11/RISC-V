# tests/test_graph_generator.py

from src.graph_generator import (
    build_extension_graph,
    generate_graph_report,
    generate_dot_output,
)


# --- build_extension_graph ---

def test_shared_instruction_creates_edge_with_mnemonic():
    data = {
        "andn": {"extension": ["rv_zbb", "rv_zk"]},
    }
    graph = build_extension_graph(data)
    assert graph["rv_zbb"]["rv_zk"] == {"andn"}
    assert graph["rv_zk"]["rv_zbb"] == {"andn"}


def test_no_shared_instruction_means_empty_graph():
    data = {
        "add": {"extension": ["rv_i"]},
        "mul": {"extension": ["rv_m"]},
    }
    graph = build_extension_graph(data)
    assert len(graph) == 0


def test_multiple_shared_instructions():
    data = {
        "andn": {"extension": ["rv_zbb", "rv_zk"]},
        "orn":  {"extension": ["rv_zbb", "rv_zk"]},
    }
    graph = build_extension_graph(data)
    assert "andn" in graph["rv_zbb"]["rv_zk"]
    assert "orn" in graph["rv_zbb"]["rv_zk"]


def test_three_extensions_two_pairs():
    data = {
        "andn": {"extension": ["rv_zbb", "rv_zk", "rv_zbkb"]},
    }
    graph = build_extension_graph(data)
    # All three pairs must be connected
    assert "rv_zk" in graph["rv_zbb"]
    assert "rv_zbkb" in graph["rv_zbb"]
    assert "rv_zbkb" in graph["rv_zk"]


def test_single_extension_instruction_not_in_graph():
    data = {
        "add": {"extension": ["rv_i"]},
    }
    graph = build_extension_graph(data)
    assert "rv_i" not in graph


def test_empty_input():
    graph = build_extension_graph({})
    assert graph == {}


def test_missing_extension_field_excluded():
    data = {
        "add":     {"extension": ["rv_i"]},
        "mystery": {},
    }
    graph = build_extension_graph(data)
    assert len(graph) == 0


# --- generate_graph_report ---

def test_graph_report_mentions_shared_mnemonic():
    data = {
        "andn": {"extension": ["rv_zbb", "rv_zk"]},
    }
    graph = build_extension_graph(data)
    text = generate_graph_report(graph)
    assert "ANDN" in text
    assert "shared:" in text


def test_graph_report_mentions_both_extensions():
    data = {
        "andn": {"extension": ["rv_zbb", "rv_zk"]},
    }
    graph = build_extension_graph(data)
    text = generate_graph_report(graph)
    assert "rv_zbb" in text
    assert "rv_zk" in text


def test_graph_report_empty_graph():
    text = generate_graph_report({})
    assert "No shared" in text or len(text) > 0


# --- generate_dot_output ---

def test_dot_output_starts_with_graph():
    data = {
        "andn": {"extension": ["rv_zbb", "rv_zk"]},
    }
    graph = build_extension_graph(data)
    dot = generate_dot_output(graph)
    assert dot.startswith("graph extension_graph {")


def test_dot_output_contains_edge():
    data = {
        "andn": {"extension": ["rv_zbb", "rv_zk"]},
    }
    graph = build_extension_graph(data)
    dot = generate_dot_output(graph)
    assert "rv_zbb" in dot
    assert "rv_zk" in dot
    assert "--" in dot


def test_dot_output_edge_label_shows_count():
    data = {
        "andn": {"extension": ["rv_zbb", "rv_zk"]},
        "orn":  {"extension": ["rv_zbb", "rv_zk"]},
    }
    graph = build_extension_graph(data)
    dot = generate_dot_output(graph)
    # 2 shared instructions — label should say 2
    assert '[label="2"]' in dot


def test_dot_output_empty_graph():
    dot = generate_dot_output({})
    assert dot.startswith("graph extension_graph {")
    assert dot.endswith("}")