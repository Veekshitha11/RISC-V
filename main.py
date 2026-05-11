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
    print(multi_extension_report)

    save_report_to_file(
        extension_summary,
        multi_extension_report,
        "output/summary.txt",
    )

    # Tier 2 ISA manual extraction
    manual_extensions = (
        extract_extensions_from_manual(
            "riscv-isa-manual/src"
        )
    )

    print("\nManual Extensions")
    print("-" * 40)

    for extension in sorted(manual_extensions):
        print(extension)

    # Cross-reference pipeline
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

    print("\nCross Reference Summary")
    print("-" * 55)

    print(
        f"Matched Extensions: "
        f"{len(cross_reference_results['matched'])}"
    )

    print(
        f"JSON Only Extensions: "
        f"{len(cross_reference_results['json_only'])}"
    )

    print(
        f"Manual Only Extensions: "
        f"{len(cross_reference_results['manual_only'])}"
    )


if __name__ == "__main__":
    main()