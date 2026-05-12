# src/parser.py

import json
from collections import defaultdict


# reads instr_dict.json and returns parsed JSON
def load_instruction_data(file_path: str) -> dict:

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_extensions(instruction_info: dict) -> list:

    ext = instruction_info.get("extension", [])

    if ext is None:
        return []

    if isinstance(ext, str):
        return [ext]

    if isinstance(ext, list):
        return ext

    return []


# group instructions by extension
def group_by_extension(instruction_data: dict) -> dict:

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


# instructions with more than one extension
def find_multi_extension_instructions(
    instruction_data: dict,
) -> dict:

    multi_extension_instructions = {}

    for instruction_name, instruction_info in instruction_data.items():

        extensions = get_extensions(instruction_info)

        if len(extensions) > 1:

            multi_extension_instructions[
                instruction_name.lower()
            ] = extensions

    return multi_extension_instructions
