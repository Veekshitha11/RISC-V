"""
Scan the official ISA manual ``src/**/*.adoc`` tree for extension name
tokens. This is regex-based, not a full AsciiDoc parse: patterns favor
RISC-V-shaped names (``Z*``, ``Ss*``, single-letter bases) and a small
noise list drops common English words if they ever slip through.
"""

import re
from pathlib import Path

from src.normalizer import normalize_extension_name


def extract_extensions_from_manual(
    manual_src_path: str,
) -> set:
    """
    Walk ``manual_src_path`` recursively and return a set of canonical
    extension names found in ``.adoc`` files.

    Raises ``FileNotFoundError`` if ``manual_src_path`` is not a directory
    (clone the manual first). Raises ``RuntimeError`` if a file cannot be
    read. Empty trees yield an empty set.
    """

    root = Path(manual_src_path)
    if not root.is_dir():
        raise FileNotFoundError(
            "ISA manual AsciiDoc directory not found: "
            f"{manual_src_path}\n"
            "Clone: git clone https://github.com/riscv/riscv-isa-manual"
        )

    # Tight token shapes reduce junk; we still normalize so manual ``Zba``
    # and JSON ``rv_zba`` can match after canonicalization elsewhere.
    extension_pattern = re.compile(
        r"\b("
        r"Z[a-z]+|"
        r"Ss[a-z]+|Sm[a-z]+|Sv[a-z]+|"
        r"X[a-z]+|"
        r"[IMFDQCAVHBUE]\b"
        r")\b"
    )

    # ``The`` / ``Note`` / ``hart`` never match the regex as full tokens,
    # but this set catches odd lowercase normalizations if patterns widen.
    noise_lower = {
        "the", "this", "for", "in", "note", "section", "table",
        "type", "base", "mode", "hart", "trap",
        # Author surnames from ISA manual contributor lists that match
        # Z-extension and S-extension patterns and cause false positives
        "zabrocki", "zandijk", "zhang", "zhao", "zhou", "zimmer",
        "zack", "zane", "zara", "scheid", "schmidt", "shaked",
        "shanbhogue", "scott", "shadow", "shall", "since",
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
