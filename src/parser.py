"""
Load ``instr_dict.json`` and derive per-extension instruction lists plus
multi-extension membership. The landscape file is inconsistent: the
``extension`` field may be missing, ``null``, a bare string, or a list—
``get_extensions`` normalizes that before grouping so Tier 1 counts stay
correct.
"""

import json
from collections import defaultdict


def load_instruction_data(file_path: str) -> dict:
    """
    Read a JSON object from ``file_path`` (typically ``data/instr_dict.json``).

    Returns the top-level dict keyed by instruction mnemonic. Raises
    ``FileNotFoundError`` or ``JSONDecodeError`` from ``open`` / ``json.load``
    if the path or file content is invalid.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_extensions(instruction_info: dict) -> list:
    """
    Return extension tag(s) for one instruction entry as a list of strings.

    ``instruction_info`` is the inner dict for one mnemonic. Missing key,
    ``None``, or ``[]`` yield ``[]``; a single string becomes a one-element
    list so callers never iterate characters by mistake. Unknown types
    yield ``[]``.
    """

    ext = instruction_info.get("extension", [])

    if ext is None:
        return []

    if isinstance(ext, str):
        return [ext]

    if isinstance(ext, list):
        return ext

    return []


def group_by_extension(instruction_data: dict) -> dict:
    """
    Map each raw extension tag to a list of instruction mnemonics (lowercase).

    ``instruction_data`` is the full dict from ``load_instruction_data``.
    Entries with no usable extensions are skipped. Returns a plain dict
    suitable for reporting (keys are tags like ``rv_zba``).
    """

    extension_groups = defaultdict(list)

    for instruction_name, instruction_info in instruction_data.items():

        extensions = get_extensions(instruction_info)

        if not extensions:
            continue

        for extension in extensions:
            extension_groups[extension].append(
                instruction_name.lower()
            )

    return extension_groups


def find_multi_extension_instructions(
    instruction_data: dict,
) -> dict:
    """
    Return mnemonics that list more than one extension tag.

    Values are the raw tag lists from JSON (order preserved). Instructions
    with zero or one extension after ``get_extensions`` are omitted.
    """

    multi_extension_instructions = {}

    for instruction_name, instruction_info in instruction_data.items():

        extensions = get_extensions(instruction_info)

        if len(extensions) > 1:

            multi_extension_instructions[
                instruction_name.lower()
            ] = extensions

    return multi_extension_instructions
