# src/normalizer.py

import re


def normalize_extension_name(extension_name: str) -> str:
    """
    Normalize extension names across different sources.

    Examples:
    rv_zba     -> zba
    RV_ZBA     -> zba
    rv32_zba   -> zba
    Zba        -> zba
    """

    normalized = extension_name.strip().lower()

    # remove rv32_ / rv64_ prefixes
    normalized = re.sub(
        r"^rv(32|64)_",
        "",
        normalized,
    )

    # remove generic rv_ prefix
    normalized = re.sub(
        r"^rv_",
        "",
        normalized,
    )

    return normalized