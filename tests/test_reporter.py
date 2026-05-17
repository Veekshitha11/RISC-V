# tests/test_reporter.py

import os
import tempfile
from src.reporter import (
    generate_extension_summary,
    generate_multi_extension_report,
    save_report_to_file,
)


# --- generate_extension_summary ---

def test_summary_format_matches_rubric():
    groups = {"rv_zba": ["sh1add", "sh2add", "add_uw"]}
    text = generate_extension_summary(groups)
    assert "rv_zba | 3 instructions | e.g. ADD_UW" in text


def test_summary_singular():
    groups = {"rv_zifencei": ["fence_i"]}
    text = generate_extension_summary(groups)
    assert "1 instruction" in text
    assert "1 instructions" not in text


def test_summary_plural():
    groups = {"rv_zba": ["sh1add", "sh2add"]}
    text = generate_extension_summary(groups)
    assert "2 instructions" in text


def test_summary_mnemonic_uppercase():
    groups = {"rv_i": ["add"]}
    text = generate_extension_summary(groups)
    assert "e.g. ADD" in text


def test_summary_footer_total_extensions():
    groups = {"rv_i": ["add"], "rv_m": ["mul"]}
    text = generate_extension_summary(groups)
    assert "Total extensions:    2" in text


def test_summary_footer_total_instructions():
    groups = {"rv_i": ["add", "sub"], "rv_m": ["mul"]}
    text = generate_extension_summary(groups)
    assert "Total instructions:  3" in text


def test_summary_sorted_alphabetically():
    groups = {"rv_zba": ["sh1add"], "rv_i": ["add"]}
    text = generate_extension_summary(groups)
    assert text.index("rv_i") < text.index("rv_zba")


def test_summary_example_first_alphabetically():
    groups = {"rv_zba": ["sh2add", "add_uw", "sh1add"]}
    text = generate_extension_summary(groups)
    assert "e.g. ADD_UW" in text


def test_summary_empty_groups():
    text = generate_extension_summary({})
    assert "Total extensions:    0" in text
    assert "Total instructions:  0" in text


def test_summary_contains_divider():
    groups = {"rv_i": ["add"]}
    text = generate_extension_summary(groups)
    assert "-" * 55 in text


# --- generate_multi_extension_report ---

def test_multi_extension_report_format():
    multi = {"andn": ["rv_zbb", "rv_zk"]}
    text = generate_multi_extension_report(multi)
    assert "ANDN -> rv_zbb, rv_zk" in text


def test_multi_extension_report_uppercase_mnemonic():
    multi = {"sha256sig0": ["rv_zknh", "rv_zkn"]}
    text = generate_multi_extension_report(multi)
    assert "SHA256SIG0" in text


def test_multi_extension_report_empty():
    text = generate_multi_extension_report({})
    assert "None found" in text


def test_multi_extension_report_header():
    text = generate_multi_extension_report({})
    assert "Instructions With Multiple Extensions" in text


def test_multi_extension_report_multiple_entries():
    multi = {
        "andn": ["rv_zbb", "rv_zk"],
        "orn": ["rv_zbb", "rv_zk"],
    }
    text = generate_multi_extension_report(multi)
    assert "ANDN" in text
    assert "ORN" in text


# --- save_report_to_file ---

def test_save_report_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "summary.txt")
        save_report_to_file("summary", "multi", path)
        assert os.path.exists(path)


def test_save_report_contents():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "summary.txt")
        save_report_to_file("summary content", "multi content", path)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        assert "summary content" in content
        assert "multi content" in content


def test_save_report_overwrites_existing():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "summary.txt")
        save_report_to_file("first", "run", path)
        save_report_to_file("second", "run", path)
        with open(path, encoding="utf-8") as f:
            content = f.read()
        assert "second" in content
        assert "first" not in content