# tests/test_cross_reference.py

from src.cross_reference import (
    cross_reference_extensions,
    generate_cross_reference_report,
    normalize_json_extensions,
    levenshtein_distance,
    fuzzy_match,
)


# --- levenshtein_distance ---

def test_levenshtein_identical():
    assert levenshtein_distance("Zba", "Zba") == 0


def test_levenshtein_empty_a():
    assert levenshtein_distance("", "Zba") == 3


def test_levenshtein_empty_b():
    assert levenshtein_distance("Zba", "") == 3


def test_levenshtein_one_edit():
    # Svinval vs Svinval_h — distance 2 (underscore + h)
    assert levenshtein_distance("svinval", "svinval_h") == 2


def test_levenshtein_completely_different():
    assert levenshtein_distance("Zba", "Xyz") == 3


# --- fuzzy_match ---

def test_fuzzy_match_exact_hit():
    result = fuzzy_match("Zba", {"Zba", "Zbb", "Zicsr"})
    assert result == "Zba"


def test_fuzzy_match_near_miss():
    # Svinval_h is close to Svinval (similarity ~0.78)
    result = fuzzy_match("Svinval_h", {"Svinval", "Zba", "Zicsr"})
    assert result == "Svinval"


def test_fuzzy_match_no_candidate():
    # Completely different — should return None
    result = fuzzy_match("Zvqldot8i", {"Zba", "Zbb", "I", "M"})
    assert result is None


def test_fuzzy_match_empty_candidates():
    result = fuzzy_match("Zba", set())
    assert result is None


def test_fuzzy_match_threshold_respected():
    # At threshold 0.99 nothing should match except identical
    result = fuzzy_match("Svinval_h", {"Svinval"}, threshold=0.99)
    assert result is None


# --- cross_reference_extensions ---

def test_cross_reference_exact_matched():
    json_ext = {"Zba", "Zbb", "Zicsr"}
    manual_ext = {"Zba", "Zicsr", "Zifencei"}
    results = cross_reference_extensions(
        json_ext, manual_ext, fuzzy=False
    )
    assert "Zba" in results["matched"]
    assert "Zicsr" in results["matched"]
    assert "Zbb" in results["json_only"]
    assert "Zifencei" in results["manual_only"]


def test_cross_reference_all_matched():
    json_ext = {"I", "M", "Zba"}
    manual_ext = {"I", "M", "Zba"}
    results = cross_reference_extensions(
        json_ext, manual_ext, fuzzy=False
    )
    assert len(results["json_only"]) == 0
    assert len(results["manual_only"]) == 0
    assert len(results["matched"]) == 3


def test_cross_reference_all_unmatched():
    json_ext = {"Zba"}
    manual_ext = {"Zicsr"}
    results = cross_reference_extensions(
        json_ext, manual_ext, fuzzy=False
    )
    assert len(results["matched"]) == 0
    assert "Zba" in results["json_only"]
    assert "Zicsr" in results["manual_only"]


def test_cross_reference_empty_sets():
    results = cross_reference_extensions(
        set(), set(), fuzzy=False
    )
    assert results["matched"] == set()
    assert results["json_only"] == set()
    assert results["manual_only"] == set()


def test_cross_reference_fuzzy_catches_near_miss():
    # Svinval_h should fuzzy-match to Svinval
    json_ext = {"Svinval_h"}
    manual_ext = {"Svinval"}
    results = cross_reference_extensions(
        json_ext, manual_ext, fuzzy=True
    )
    # Should be in matched (with fuzzy annotation) not json_only
    matched_names = {m.replace(" (fuzzy)", "") for m in results["matched"]}
    assert "Svinval_h" in matched_names
    assert "Svinval_h" not in results["json_only"]


def test_cross_reference_fuzzy_disabled():
    # When fuzzy=False near-miss stays in json_only
    json_ext = {"Svinval_h"}
    manual_ext = {"Svinval"}
    results = cross_reference_extensions(
        json_ext, manual_ext, fuzzy=False
    )
    assert "Svinval_h" in results["json_only"]


def test_cross_reference_results():
    json_extensions = {"Zba", "Zbb", "Zicsr"}
    manual_extensions = {"Zba", "Zicsr", "Zifencei"}
    results = cross_reference_extensions(
        json_extensions, manual_extensions, fuzzy=False
    )
    assert "Zba" in results["matched"]
    assert "Zicsr" in results["matched"]
    assert "Zbb" in results["json_only"]
    assert "Zifencei" in results["manual_only"]


# --- generate_cross_reference_report ---

def test_count_line_in_report():
    results = {
        "matched": {"I"},
        "json_only": {"Zba"},
        "manual_only": {"Zicsr"},
    }
    text = generate_cross_reference_report(results)
    assert "1 matched, 1 in JSON only, 1 in manual only" in text


def test_report_contains_all_sections():
    results = {
        "matched": {"I"},
        "json_only": {"Zba"},
        "manual_only": {"Zicsr"},
    }
    text = generate_cross_reference_report(results)
    assert "Matched Extensions" in text
    assert "JSON Only Extensions" in text
    assert "Manual Only Extensions" in text


def test_report_empty_sets():
    results = {
        "matched": set(),
        "json_only": set(),
        "manual_only": set(),
    }
    text = generate_cross_reference_report(results)
    assert "0 matched, 0 in JSON only, 0 in manual only" in text


# --- normalize_json_extensions ---

def test_normalize_json_extensions_uses_canonical_names():
    extension_groups = {
        "rv_i": ["add"],
        "rv_zba": ["sh1add"],
    }
    assert normalize_json_extensions(extension_groups) == {"I", "Zba"}


def test_normalize_json_extensions_skips_empty_canonical():
    extension_groups = {
        "rv_i": ["add"],
        "": ["bad"],
    }
    assert normalize_json_extensions(extension_groups) == {"I"}


def test_normalize_json_extensions_empty_input():
    assert normalize_json_extensions({}) == set()