# src/reporter.py


def generate_extension_summary(extension_groups: dict) -> str:

    lines = []

    lines.append("Extension Summary")
    lines.append("-" * 55)

    for extension in sorted(extension_groups):

        instructions = extension_groups[extension]

        n = len(instructions)
        word = "instruction" if n == 1 else "instructions"
        example = sorted(instructions)[0].upper()

        lines.append(
            f"{extension} | "
            f"{n} {word} | "
            f"e.g. {example}"
        )

    return "\n".join(lines)


def generate_multi_extension_report(
    multi_extension_instructions: dict,
) -> str:

    lines = []

    lines.append(
        "\nInstructions With Multiple Extensions"
    )

    lines.append("-" * 55)

    if not multi_extension_instructions:
        lines.append("None found")

    else:
        for instruction, extensions in (
            multi_extension_instructions.items()
        ):

            lines.append(
                f"{instruction.upper()} -> "
                f"{', '.join(extensions)}"
            )

    return "\n".join(lines)


def save_report_to_file(
    extension_summary: str,
    multi_extension_report: str,
    output_path: str,
):

    with open(output_path, "w", encoding="utf-8") as file:

        file.write(extension_summary)
        file.write("\n\n")
        file.write(multi_extension_report)