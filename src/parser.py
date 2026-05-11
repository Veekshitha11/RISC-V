# src/parser.py

import json
from collections import defaultdict


# reads instr_dict.json and returns parsed JSON
def load_instruction_data(file_path: str) -> dict:

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# group instructions by extension
def group_by_extension(instruction_data: dict) -> dict:

    extension_groups = defaultdict(list)

    for instruction_name, instruction_info in instruction_data.items():

        extensions = instruction_info.get("extension", [])

        # skip malformed entries with no extension tags
        if not extensions:
            continue

        for extension in extensions:
            extension_groups[extension].append(
                instruction_name.upper()
            )

    return extension_groups


# instructions with more than one extension
def find_multi_extension_instructions(
    instruction_data: dict,
) -> dict:

    multi_extension_instructions = {}

    for instruction_name, instruction_info in instruction_data.items():

        extensions = instruction_info.get("extension", [])

        # some instructions may belong to multiple extensions
        if len(extensions) > 1:

            multi_extension_instructions[
                instruction_name.upper()
            ] = extensions

    return multi_extension_instructions