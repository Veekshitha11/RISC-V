# tests/test_parser.py

from src.parser import (
    group_by_extension,
    find_multi_extension_instructions,
)


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

    assert "ADD" in grouped["rv_i"]

    assert "MUL" in grouped["rv_m"]


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

    assert "ANDN" in multi_extension

    assert (
        len(
            multi_extension["ANDN"]
        )
        == 2
    )