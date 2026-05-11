# src/manual_parser.py

"""
Extract extension references from ISA manual AsciiDoc files.
"""

import re
from pathlib import Path

from src.normalizer import (
    normalize_extension_name,
)


def extract_extensions_from_manual(
    manual_src_path: str,
) -> set:

    extension_names = set()

    adoc_files = Path(
        manual_src_path
    ).rglob("*.adoc")

    # matches:
    # Zba, Zicsr, Zifencei, M, F, D, V
    extension_pattern = re.compile(
        r"\b(?:Z[a-zA-Z0-9]+|[MFDVCAHQS])\b"
    )

    valid_prefixes = (
        "z",
        "m",
        "f",
        "d",
        "v",
        "s",
        "a",
        "c",
        "h",
        "q",
    )

    ignored_terms = {
        "zero",
        "zeroes",
        "zeros",
        "zhang",
        "zabrocki",
        "zandijk",
    }

    for adoc_file in adoc_files:

        try:
            content = adoc_file.read_text(
                encoding="utf-8"
            )

        except Exception:
            continue

        matches = extension_pattern.findall(
            content
        )

        for match in matches:

            normalized = (
                normalize_extension_name(
                    match
                )
            )

            if len(normalized) < 2:
                continue

            if normalized in ignored_terms:
                continue

            if not normalized.startswith(
                valid_prefixes
            ):
                continue

            extension_names.add(normalized)

    return extension_names