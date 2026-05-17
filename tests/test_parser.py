# tests/test_parser.py

from src.parser import (
    get_extensions,
    group_by_extension,
    find_multi_extension_instructions,
)


# --- get_extensions ---

def test_get_extensions_missing():
    assert get_extensions({}) == []


def test_get_extensions_none():
    assert get_extensions({"extension": None}) == []


def test_get_extensions_string():
    assert get_extensions({"extension": "rv_zba"}) == ["rv_zba"]


def test_get_extensions_empty_list():
    assert get_extensions({"extension": []}) == []


def test_get_extensions_normal_list():
    result = get_extensions({"extension": ["rv_i", "rv_m"]})
    assert result == ["rv_i", "rv_m"]


def test_get_extensions_single_item_list():
    result = get_extensions({"extension": ["rv_zba"]})
    assert result == ["rv_zba"]


def test_get_extensions_ignores_other_fields():
    result = get_extensions({
        "extension": ["rv_i"],
        "encoding": "...",
        "match": "0x33",
    })
    assert result == ["rv_i"]


# --- group_by_extension ---

def test_group_by_extension():
    sample_data = {
        "add": {"extension": ["rv_i"]},
        "mul": {"extension": ["rv_m"]},
    }
    grouped = group_by_extension(sample_data)
    assert "add" in grouped["rv_i"]
    assert "mul" in grouped["rv_m"]


def test_group_by_extension_multi_extension_instruction():
    sample_data = {
        "andn": {"extension": ["rv_zbb", "rv_zk"]},
    }
    grouped = group_by_extension(sample_data)
    assert "andn" in grouped["rv_zbb"]
    assert "andn" in grouped["rv_zk"]


def test_group_by_extension_missing_extension_excluded():
    sample_data = {
        "add": {"extension": ["rv_i"]},
        "mystery": {},
    }
    grouped = group_by_extension(sample_data)
    all_mnemonics = [m for ms in grouped.values() for m in ms]
    assert "mystery" not in all_mnemonics


def test_group_by_extension_empty_input():
    assert group_by_extension({}) == {}


# --- find_multi_extension_instructions ---

def test_multi_extension_detection():
    sample_data = {
        "andn": {"extension": ["rv_zbb", "rv_zk"]}
    }
    multi_extension = find_multi_extension_instructions(sample_data)
    assert "andn" in multi_extension
    assert len(multi_extension["andn"]) == 2


def test_single_extension_not_in_multi():
    sample_data = {
        "add": {"extension": ["rv_i"]},
    }
    multi_extension = find_multi_extension_instructions(sample_data)
    assert "add" not in multi_extension


def test_multi_extension_empty_input():
    assert find_multi_extension_instructions({}) == {}


def test_multi_extension_three_extensions():
    sample_data = {
        "andn": {"extension": ["rv_zbb", "rv_zk", "rv_zbkb"]},
    }
    multi_extension = find_multi_extension_instructions(sample_data)
    assert "andn" in multi_extension
    assert len(multi_extension["andn"]) == 3


# --- missing branch coverage ---

def test_load_instruction_data_file_not_found():
    from src.parser import load_instruction_data
    import pytest
    with pytest.raises(FileNotFoundError):
        load_instruction_data("nonexistent_path.json")


def test_find_multi_extension_returns_sorted():
    from src.parser import find_multi_extension_instructions
    data = {
        "andn": {"extension": ["rv_zk", "rv_zbb", "rv_zbkb"]},
    }
    result = find_multi_extension_instructions(data)
    assert result["andn"] == sorted(["rv_zk", "rv_zbb", "rv_zbkb"])