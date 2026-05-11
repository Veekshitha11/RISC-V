# RISC-V Instruction Set Explorer

## Project Description

A metadata exploration and reconciliation tool for parsing and analyzing RISC-V instruction-extension relationships from the RISC-V Extensions Landscape repository and the official RISC-V ISA manual.

---

## Implemented Features

### Tier 1

- Parse instruction metadata from `instr_dict.json`
- Group instructions by extension tags
- Generate extension summary reports
- Detect instructions belonging to multiple extensions

### Tier 2

- Extract extension references from ISA manual AsciiDoc files
- Normalize extension naming across repositories
- Cross-reference extension metadata between datasets
- Detect unmatched extensions between the ISA manual and instruction metadata

### Tier 3

- Unit tests using `pytest`
- Extension relationship graph generation
- Shared instruction dependency visualization

---

## Architecture

- `parser.py` → instruction parsing and grouping
- `reporter.py` → Tier-1 report generation
- `normalizer.py` → canonical extension normalization
- `manual_parser.py` → ISA manual extension extraction
- `cross_reference.py` → extension reconciliation and mismatch reporting
- `graph_generator.py` → extension relationship graph generation

---

## Design Decisions

- Extension names are normalized before cross-referencing
- Instructions are modeled as many-to-many relationships
- ISA manual extraction uses lightweight regex parsing instead of full AsciiDoc parsing
- Report generation is separated from parsing logic for modularity

---

## Assumptions

- Extension tags are treated as case-insensitive after normalization
- Some regex extraction noise from ISA manual sources is filtered explicitly
- Instructions without extension metadata are ignored

---

## Project Structure

```text
src/
tests/
data/
output/
main.py
requirements.txt
pytest.ini