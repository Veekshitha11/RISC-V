# tests/test_normalizer.py

from src.normalizer import (
    normalize_extension_name,
)


def test_remove_rv_prefix():

    assert (
        normalize_extension_name(
            "rv_zba"
        )
        == "zba"
    )


def test_remove_rv64_prefix():

    assert (
        normalize_extension_name(
            "rv64_zbb"
        )
        == "zbb"
    )


def test_lowercase_conversion():

    assert (
        normalize_extension_name(
            "Zicsr"
        )
        == "zicsr"
    )