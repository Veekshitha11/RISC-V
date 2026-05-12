"""
Compare extension sets from ``instr_dict.json`` (after canonicalization)
with names scraped from the ISA manual. ``json_only`` usually means the
landscape lists an extension the manual scan did not pick up yet—often
newer or vendor-specific packs, or limits of regex on AsciiDoc.
"""

from src.normalizer import (
    normalize_extension_name,
)


def normalize_json_extensions(
    extension_groups: dict,
) -> set:
    """
    Build the set of canonical extension names implied by Tier 1 grouping.

    ``extension_groups`` keys are raw tags (e.g. ``rv_zba``). Tags that
    normalize to ``""`` are skipped so bad keys do not enter the set.
    """

    normalized_extensions = set()

    for extension in extension_groups:

        normalized = (
            normalize_extension_name(
                extension
            )
        )

        if not normalized:
            continue

        normalized_extensions.add(
            normalized
        )

    return normalized_extensions


def cross_reference_extensions(
    json_extensions: set,
    manual_extensions: set,
) -> dict:
    """
    Split two canonical-name sets into matched, JSON-only, and manual-only.

    Both inputs must already use the same normalization as
    ``normalize_extension_name``. Returns dict keys ``matched``,
    ``json_only``, and ``manual_only`` (each a set, possibly empty).
    """

    matched = (
        json_extensions &
        manual_extensions
    )

    json_only = (
        json_extensions -
        manual_extensions
    )

    manual_only = (
        manual_extensions -
        json_extensions
    )

    return {
        "matched": matched,
        "json_only": json_only,
        "manual_only": manual_only,
    }


def generate_cross_reference_report(
    cross_reference_results: dict,
) -> str:
    """
    Format ``cross_reference_results`` as a stable, sorted text report.

    Expects keys ``matched``, ``json_only``, ``manual_only``. Includes the
    assignment-style count line plus three labeled sections.
    """

    matched = sorted(
        cross_reference_results["matched"]
    )

    json_only = sorted(
        cross_reference_results["json_only"]
    )

    manual_only = sorted(
        cross_reference_results["manual_only"]
    )

    lines = []

    lines.append(
        "Cross Reference Summary"
    )

    lines.append("-" * 55)

    lines.append(
        f"Matched Extensions: {len(matched)}"
    )

    lines.append(
        f"JSON Only Extensions: {len(json_only)}"
    )

    lines.append(
        f"Manual Only Extensions: {len(manual_only)}"
    )

    lines.append("")

    lines.append(
        f"{len(matched)} matched, {len(json_only)} in JSON only, "
        f"{len(manual_only)} in manual only"
    )

    lines.append("")

    lines.append(
        "Matched Extensions"
    )

    lines.append("-" * 55)

    for extension in matched:
        lines.append(extension)

    lines.append("")

    lines.append(
        "JSON Only Extensions"
    )

    lines.append("-" * 55)

    for extension in json_only:
        lines.append(extension)

    lines.append("")

    lines.append(
        "Manual Only Extensions"
    )

    lines.append("-" * 55)

    for extension in manual_only:
        lines.append(extension)

    return "\n".join(lines)
