import argparse
import os
import subprocess
import sys
from pathlib import Path

from src.graph_generator import (
    build_extension_graph,
    generate_graph_report,
)

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


INSTR_DICT_PATH = "data/instr_dict.json"
MANUAL_ROOT = Path("riscv-isa-manual")
MANUAL_SRC = MANUAL_ROOT / "src"
OUTPUT_DIR = "output"
ISA_MANUAL_REPO = "https://github.com/riscv/riscv-isa-manual"


def main():
    """
    Entry point for all three tiers.

    Tier 1 (parsing) always runs.
    Tier 2 (ISA manual cross-reference) runs unless --skip-tier2 is passed.
    Tier 3 (graph) always runs alongside Tier 1.
    Results are printed to stdout and saved under output/.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-tier2",
        action="store_true",
        help="Skip ISA manual scan and cross-reference report",
    )
    parser.add_argument(
        "--auto-clone",
        action="store_true",
        help="Clone riscv-isa-manual into ./riscv-isa-manual if missing",
    )
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Tier 1 parsing pipeline
    instruction_data = load_instruction_data(
        INSTR_DICT_PATH
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
        f"{OUTPUT_DIR}/summary.txt",
    )

    if not args.skip_tier2:

        if not MANUAL_SRC.is_dir():

            if args.auto_clone:
                subprocess.run(
                    [
                        "git",
                        "clone",
                        ISA_MANUAL_REPO,
                        str(MANUAL_ROOT),
                    ],
                    check=True,
                )

            if not MANUAL_SRC.is_dir():
                print(
                    "ERROR: ISA manual not found at riscv-isa-manual/src.\n"
                    "Clone it with:\n"
                    "  git clone https://github.com/riscv/riscv-isa-manual\n"
                    "Or re-run with:  python main.py --auto-clone\n"
                    "Or skip Tier 2 with:  python main.py --skip-tier2",
                    file=sys.stderr,
                )
                sys.exit(1)

        manual_extensions = (
            extract_extensions_from_manual(
                str(MANUAL_SRC)
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
            f"{OUTPUT_DIR}/cross_reference_report.txt",
            "w",
            encoding="utf-8",
        ) as file:

            file.write(cross_reference_report)

    else:

        print()
        print(
            "Skipping Tier 2 (--skip-tier2): "
            "no ISA manual scan or cross-reference file."
        )

    # Tier 3 graph (runs with Tier 1; does not require the manual)
    extension_graph = (
        build_extension_graph(
            instruction_data
        )
    )

    graph_report = (
        generate_graph_report(
            extension_graph
        )
    )

    print()
    print(graph_report)

    with open(
        f"{OUTPUT_DIR}/extension_graph.txt",
        "w",
        encoding="utf-8",
    ) as file:

        file.write(graph_report)


if __name__ == "__main__":
    main()