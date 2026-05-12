# src/manual_parser.py

"""
Extract extension references from ISA manual AsciiDoc files.
"""

import re
from pathlib import Path

from src.normalizer import normalize_extension_name


def extract_extensions_from_manual(
    manual_src_path: str,
) -> set:

    root = Path(manual_src_path)
    if not root.is_dir():
        raise FileNotFoundError(
            "ISA manual AsciiDoc directory not found: "
            f"{manual_src_path}\n"
            "Clone: git clone https://github.com/riscv/riscv-isa-manual"
        )

    # RISC-V-ish extension tokens (tune as you read real .adoc)
    extension_pattern = re.compile(
        r"\b("
        r"Z[a-z]+|"           # Zba, Zicsr
        r"Ss[a-z]+|Sm[a-z]+|Sv[a-z]+|"
        r"X[a-z]+|"
        r"[IMFDQCAVHBUE]\b"   # common single-letter extensions
        r")\b"
    )

    noise_lower = {
        "the", "this", "for", "in", "note", "section", "table",
        "type", "base", "mode", "hart", "trap",
    }

    extension_names = set()

    for adoc_file in root.rglob("*.adoc"):
        try:
            content = adoc_file.read_text(encoding="utf-8")
        except OSError as exc:
            raise RuntimeError(
                f"Failed to read {adoc_file}"
            ) from exc

        for match in extension_pattern.findall(content):
            canon = normalize_extension_name(match)
            if not canon:
                continue
            if canon.lower() in noise_lower:
                continue
            extension_names.add(canon)

    return extension_names