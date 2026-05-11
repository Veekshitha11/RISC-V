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

from src.normalizer import normalize_extension_name

print(normalize_extension_name("rv_zba"))
print(normalize_extension_name("RV64_ZBB"))
print(normalize_extension_name("Zicsr"))

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

from src.manual_parser import (
    extract_extensions_from_manual,
)

manual_extensions = (
    extract_extensions_from_manual(
        "riscv-isa-manual/src"
    )
)

print("\nManual Extensions")
print("-" * 40)

for extension in sorted(manual_extensions):
    print(extension)

if __name__ == "__main__":
    main()