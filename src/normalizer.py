"""
Convert RISC-V extension labels from JSON and the ISA manual into one
canonical string so two sources can be compared set-to-set. Handles
``rv_*`` / ``rv32_*`` / ``rv64_*`` prefixes and special cases like
``rv64_i`` (RV64I) versus base ``rv_i`` (I).
"""

import re
from typing import Optional


# Title-casing or regex-only rules break single-letter bases: e.g. ``rv_i``
# must become ``I``, not ``Zi``. Unknown letters still map here when the
# slug is exactly one character after prefix strip.
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
    Return the canonical extension name for cross-referencing.

    ``extension_name`` is a tag or manual token (e.g. ``rv_zba``,
    ``Zba``). Returns ``""`` for ``None``, empty, or whitespace-only
    input. ``rv64_i`` becomes ``RV64I``; ``rv_i`` becomes ``I``.
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


def normalize_tag(tag: str) -> str:
    """
    Same as ``normalize_extension_name``; use when the input is known
    to be a JSON extension tag. ``None`` and blank inputs return ``""``.
    """

    return normalize_extension_name(tag)
