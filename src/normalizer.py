# tests/test_normalizer.py

from src.normalizer import (
    normalize_extension_name,
    normalize_tag,
)


# --- base single-letter extensions ---

def test_rv_i():
    assert normalize_extension_name("rv_i") == "I"


def test_rv_m():
    assert normalize_extension_name("rv_m") == "M"


def test_rv_a():
    assert normalize_extension_name("rv_a") == "A"


def test_rv_f():
    assert normalize_extension_name("rv_f") == "F"


def test_rv_d():
    assert normalize_extension_name("rv_d") == "D"


def test_rv_c():
    assert normalize_extension_name("rv_c") == "C"


def test_rv_v():
    assert normalize_extension_name("rv_v") == "V"


def test_rv_h():
    assert normalize_extension_name("rv_h") == "H"


def test_rv_q():
    assert normalize_extension_name("rv_q") == "Q"


# --- rv64_ prefix ---

def test_rv64_i():
    assert normalize_extension_name("rv64_i") == "RV64I"


def test_rv64_zbb():
    assert normalize_extension_name("rv64_zbb") == "Zbb"


# --- Z extensions ---

def test_rv_zba():
    assert normalize_extension_name("rv_zba") == "Zba"


def test_rv_zknh():
    assert normalize_extension_name("rv_zknh") == "Zknh"


def test_rv_zicsr():
    assert normalize_extension_name("rv_zicsr") == "Zicsr"


def test_rv_zifencei():
    assert normalize_extension_name("rv_zifencei") == "Zifencei"


# --- S prefix family ---

def test_rv_smrnmi():
    assert normalize_extension_name("rv_smrnmi") == "Smrnmi"


def test_rv_svinval():
    assert normalize_extension_name("rv_svinval") == "Svinval"


def test_rv_ssctr():
    assert normalize_extension_name("rv_ssctr") == "Ssctr"


# --- manual-style names (already canonical) ---

def test_manual_zicsr():
    assert normalize_extension_name("Zicsr") == "Zicsr"


def test_manual_zba():
    assert normalize_extension_name("Zba") == "Zba"


# --- uppercase input ---

def test_uppercase_z_extension():
    assert normalize_extension_name("ZBA") == "Zba"


# --- edge cases ---

def test_none_returns_empty():
    assert normalize_extension_name(None) == ""


def test_blank_string_returns_empty():
    assert normalize_extension_name("") == ""


def test_whitespace_only_returns_empty():
    assert normalize_extension_name("   ") == ""


# --- normalize_tag alias ---

def test_normalize_tag_alias():
    assert normalize_tag("rv_zba") == "Zba"


def test_normalize_tag_none():
    assert normalize_tag(None) == ""


# --- missing branch coverage ---

def test_rv_ss_prefix():
    from src.normalizer import normalize_extension_name
    assert normalize_extension_name("rv_ssaia") == "Ssaia"


def test_rv_sv_prefix():
    from src.normalizer import normalize_extension_name
    assert normalize_extension_name("rv_svpbmt") == "Svpbmt"


def test_rv_x_prefix():
    from src.normalizer import normalize_extension_name
    result = normalize_extension_name("rv_xvendor")
    assert result == "Xvendor"


def test_rv32_base_extension():
    from src.normalizer import normalize_extension_name
    assert normalize_extension_name("rv32_i") == "I"


def test_plain_lowercase_word():
    from src.normalizer import normalize_extension_name
    assert normalize_extension_name("zba") == "Zba"


def test_already_canonical_sm():
    from src.normalizer import normalize_extension_name
    assert normalize_extension_name("Smstateen") == "Smstateen"