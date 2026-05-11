
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