# tests/test_parser.py

from src.parser import (
    get_extensions,
    group_by_extension,
    find_multi_extension_instructions,
)


def test_get_extensions_missing():
    assert get_extensions({}) == []


def test_get_extensions_none():
    assert get_extensions({"extension": None}) == []


def test_get_extensions_string():
    assert get_extensions({"extension": "rv_zba"}) == ["rv_zba"]


def test_get_extensions_empty_list():
    assert get_extensions({"extension": []}) == []


def test_group_by_extension():

    sample_data = {
        "add": {
            "extension": ["rv_i"]
        },

        "mul": {
            "extension": ["rv_m"]
        },
    }

    grouped = group_by_extension(
        sample_data
    )

    assert "add" in grouped["rv_i"]

    assert "mul" in grouped["rv_m"]


def test_multi_extension_detection():

    sample_data = {
        "andn": {
            "extension": [
                "rv_zbb",
                "rv_zk",
            ]
        }
    }

    multi_extension = (
        find_multi_extension_instructions(
            sample_data
        )
    )

    assert "andn" in multi_extension

    assert (
        len(
            multi_extension["andn"]
        )
        == 2
    )
