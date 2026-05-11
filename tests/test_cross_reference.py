# tests/test_cross_reference.py

from src.cross_reference import (
    cross_reference_extensions,
)


def test_cross_reference_results():

    json_extensions = {
        "zba",
        "zbb",
        "zicsr",
    }

    manual_extensions = {
        "zba",
        "zicsr",
        "zifencei",
    }

    results = (
        cross_reference_extensions(
            json_extensions,
            manual_extensions,
        )
    )

    assert results["matched"] == {
        "zba",
        "zicsr",
    }

    assert results["json_only"] == {
        "zbb"
    }

    assert results["manual_only"] == {
        "zifencei"
    }