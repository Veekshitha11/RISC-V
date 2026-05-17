"""
Build human-readable Tier 1 reports: the per-extension summary table
(assignment line format) and a separate block listing mnemonics that
carry more than one extension tag. Writing to disk is isolated in
``save_report_to_file`` so parsing code stays free of I/O.
"""


def generate_extension_summary(extension_groups: dict) -> str:
    """
    Render the extension summary table as a single string.

    ``extension_groups`` maps raw tags to mnemonic lists (lowercase in
    our pipeline). Uses ``1 instruction`` vs ``N instructions``, sorts
    tags and picks the first mnemonic alphabetically for ``e.g.``,
    uppercased for display.
    """

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

    total_instructions = sum(
        len(v) for v in extension_groups.values()
    )
    lines.append("-" * 55)
    lines.append(f"Total extensions:    {len(extension_groups)}")
    lines.append(f"Total instructions:  {total_instructions}")

    return "\n".join(lines)


def generate_multi_extension_report(
    multi_extension_instructions: dict,
) -> str:
    """
    Render the multi-extension section (separate from the summary table).

    Keys are mnemonics (lowercase); each value is the raw tag list from
    JSON. Prints ``None found`` when the dict is empty.
    """

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
) -> None:
    """
    Write ``extension_summary`` and ``multi_extension_report`` to ``output_path``.

    Overwrites the file if it exists. Caller must ensure the parent
    directory exists (``main`` creates ``output/``).
    """

    with open(output_path, "w", encoding="utf-8") as file:

        file.write(extension_summary)
        file.write("\n\n")
        file.write(multi_extension_report)
