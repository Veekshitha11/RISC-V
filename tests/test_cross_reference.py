# tests/test_cross_reference.py

from src.cross_reference import (
    cross_reference_extensions,
    generate_cross_reference_report,
)


def test_cross_reference_results():

    json_extensions = {
        "Zba",
        "Zbb",
        "Zicsr",
    }

    manual_extensions = {
        "Zba",
        "Zicsr",
        "Zifencei",
    }

    results = (
        cross_reference_extensions(
            json_extensions,
            manual_extensions,
        )
    )

    assert results["matched"] == {
        "Zba",
        "Zicsr",
    }

    assert results["json_only"] == {
        "Zbb"
    }

    assert results["manual_only"] == {
        "Zifencei"
    }


def test_count_line_in_report():

    results = {
        "matched": {"I"},
        "json_only": {"Zba"},
        "manual_only": {"Zicsr"},
    }

    text = generate_cross_reference_report(results)

    assert "1 matched, 1 in JSON only, 1 in manual only" in text
