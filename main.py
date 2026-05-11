# main.py

from src.parser import (
    load_instruction_data,
    group_by_extension,
    find_multi_extension_instructions,
)

from src.reporter import (
    generate_extension_summary,
    generate_multi_extension_report,
    save_report_to_file,
)

from src.manual_parser import (
    extract_extensions_from_manual,
)

from src.cross_reference import (
    normalize_json_extensions,
    cross_reference_extensions,
    generate_cross_reference_report,
)


def main():

    # Tier 1 parsing pipeline
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

    extension_summary = (
        generate_extension_summary(
            extension_groups
        )
    )

    multi_extension_report = (
        generate_multi_extension_report(
            multi_extension_instructions
        )
    )

    print(extension_summary)
    print()
    print(multi_extension_report)

    save_report_to_file(
        extension_summary,
        multi_extension_report,
        "output/summary.txt",
    )

    # Tier 2 ISA extraction
    manual_extensions = (
        extract_extensions_from_manual(
            "riscv-isa-manual/src"
        )
    )

    json_extensions = (
        normalize_json_extensions(
            extension_groups
        )
    )

    cross_reference_results = (
        cross_reference_extensions(
            json_extensions,
            manual_extensions,
        )
    )

    cross_reference_report = (
        generate_cross_reference_report(
            cross_reference_results
        )
    )

    print()
    print(cross_reference_report)

    with open(
        "output/cross_reference_report.txt",
        "w",
        encoding="utf-8",
    ) as file:

        file.write(cross_reference_report)


if __name__ == "__main__":
    main()