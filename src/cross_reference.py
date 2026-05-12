# src/cross_reference.py

"""
Cross-reference normalized extension names between datasets.
"""

from src.normalizer import (
    normalize_extension_name,
)


def normalize_json_extensions(
    extension_groups: dict,
) -> set:

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