# main.py

from src.parser import (
    load_instruction_data,
    group_by_extension,
    find_multi_extension_instructions,
)


def main():

    instruction_data = load_instruction_data(
        "data/instr_dict.json"
    )

    extension_groups = group_by_extension(
        instruction_data
    )

    multi_extension_instructions = (
        find_multi_extension_instructions(
            instruction_data
        )
    )

    print("\nExtension Summary")
    print("-" * 55)

    for extension in sorted(extension_groups):

        instructions = extension_groups[extension]

        print(
            f"{extension} | "
            f"{len(instructions)} instructions | "
            f"e.g. {instructions[0]}"
        )

    print("\nInstructions With Multiple Extensions")
    print("-" * 55)

    if not multi_extension_instructions:
        print("None found")

    else:
        for instruction, extensions in (
            multi_extension_instructions.items()
        ):

            print(
                f"{instruction} -> "
                f"{', '.join(extensions)}"
            )


if __name__ == "__main__":
    main()