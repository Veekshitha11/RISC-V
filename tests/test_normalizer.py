# tests/test_normalizer.py

from src.normalizer import (
    normalize_extension_name,
    normalize_tag,
)


def test_rv_zba():
    assert normalize_extension_name("rv_zba") == "Zba"


def test_normalize_tag_alias():
    assert normalize_tag("rv_zba") == "Zba"


def test_rv64_zbb():
    assert normalize_extension_name("rv64_zbb") == "Zbb"


def test_rv_i():
    assert normalize_extension_name("rv_i") == "I"


def test_rv64_i():
    assert normalize_extension_name("rv64_i") == "RV64I"


def test_manual_zicsr():
    assert normalize_extension_name("Zicsr") == "Zicsr"


def test_uppercase_z_extension():
    assert normalize_extension_name("ZBA") == "Zba"


def test_none_returns_empty():
    assert normalize_extension_name(None) == ""
