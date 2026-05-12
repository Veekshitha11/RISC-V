
"""
Normalize extension names across different metadata sources.
"""

import re
from typing import Optional


# Single-letter ISA / common manual tokens after slug strip (rv_i -> i)
_BASE_SLUG = {
    "i": "I",
    "m": "M",
    "a": "A",
    "f": "F",
    "d": "D",
    "c": "C",
    "v": "V",
    "h": "H",
    "q": "Q",
    "e": "E",
    "g": "G",
    "b": "B",
    "l": "L",
    "n": "N",
    "p": "P",
    "r": "R",
    "s": "S",
    "t": "T",
    "u": "U",
    "w": "W",
    "x": "X",
    "y": "Y",
    "z": "Z",
}


def normalize_extension_name(extension_name: str) -> str:
    """
    Map JSON tags and manual tokens to one canonical string for
    comparison (e.g. rv_zba and Zba -> Zba, rv_i and I -> I).
    """

    if extension_name is None:
        return ""

    raw = str(extension_name).strip()
    if not raw:
        return ""

    lower = raw.lower()

    arch: Optional[int] = None
    if lower.startswith("rv64_"):
        arch = 64
        lower = lower[5:]
    elif lower.startswith("rv32_"):
        arch = 32
        lower = lower[5:]
    elif lower.startswith("rv_"):
        lower = lower[3:]

    lower = lower.lower()
    if not lower:
        return ""

    if lower in _BASE_SLUG:
        if lower == "i" and arch == 64:
            return "RV64I"
        return _BASE_SLUG[lower]

    if lower.startswith("z") and len(lower) >= 2:
        return "Z" + lower[1:]

    if lower.startswith("x") and len(lower) >= 2:
        return "X" + lower[1:]

    if lower.startswith("ss") and len(lower) >= 3:
        return "Ss" + lower[2:]

    if lower.startswith("sm") and len(lower) >= 3:
        return "Sm" + lower[2:]

    if lower.startswith("sv") and len(lower) >= 3:
        return "Sv" + lower[2:]

    if re.fullmatch(r"[a-z]+", lower):
        return lower[0].upper() + lower[1:]

    return lower[0].upper() + lower[1:] if lower else ""


# Alias for tests / API clarity
def normalize_tag(tag: str) -> str:
    return normalize_extension_name(tag)
