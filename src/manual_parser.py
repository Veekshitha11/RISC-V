# src/manual_parser.py

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

            extension_names.add(normalized)

    return extension_names