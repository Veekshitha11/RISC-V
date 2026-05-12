# RISC-V Instruction Set Explorer

## Project Description

A metadata exploration and reconciliation tool for parsing and analyzing RISC-V instruction-extension relationships from the RISC-V Extensions Landscape repository and the official RISC-V ISA manual.

---

## Setup and run

1. **Clone the ISA manual** (required for Tier 2). From the project root:

   ```bash
   git clone https://github.com/riscv/riscv-isa-manual
   ```

   You should have `riscv-isa-manual/src/` with `.adoc` files before running Tier 2.

2. **Install dependencies** (uses `pytest` from `requirements.txt`):

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the program** (Tier 1 + Tier 2 + Tier 3 in one command):

   ```bash
   python main.py
   ```

   - **Tier 1 only** (no manual on disk):  

     ```bash
     python main.py --skip-tier2
     ```

   - **Clone the manual automatically** if `riscv-isa-manual/src` is missing:  

     ```bash
     python main.py --auto-clone
     ```

4. **Tests**:

   ```bash
   pytest
   ```

Instruction metadata is read from `data/instr_dict.json` (from the extensions landscape project). Replace or refresh that file if you need a newer snapshot.

---

## Sample output (illustrative)

**Tier 1 — extension summary (excerpt)**

```text
Extension Summary
-------------------------------------------------------
rv_zba | 4 instructions | e.g. SH1ADD
```

**Tier 2 — cross-reference (excerpt)**

```text
Cross Reference Summary
-------------------------------------------------------
42 matched, 3 in JSON only, 5 in manual only

Matched Extensions
-------------------------------------------------------
I
Zba
...
```

Numbers depend on your `instr_dict.json` and manual revision.

**Tier 3 — graph (excerpt)**

```text
Extension Relationship Graph
-------------------------------------------------------
rv_zbb | 1 neighbor(s)
  -> rv_zk | shared: ANDN
```

---

## What “JSON only” and “manual only” mean

- **JSON only** — An extension tag appears in `instr_dict.json` (after normalization), but no matching extension name was found in the scanned ISA manual `.adoc` files. Often newer or vendor-specific extensions, or limits of regex extraction.
- **Manual only** — A name was picked up from the manual, but no instruction in your JSON is tagged with that extension after normalization. Can be ratified chapters you did not ship in the snapshot, or false positives from loose patterns.

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

- Extension names are **normalized to one canonical form** (for example `rv_zba` and `Zba` both become `Zba`) before cross-referencing so JSON and manual sets compare fairly.
- **Single-letter base extensions** (`I`, `M`, `F`, …) use an explicit mapping table after stripping `rv_` / `rv32_` / `rv64_` prefixes. Title-casing or a generic regex alone is not enough: `rv_i` must become `I`, not `Zi`, and `rv64_i` is treated as **`RV64I`**, not the same as base `I`.
- Instructions are modeled as many-to-many relationships between mnemonics and extension tags.
- ISA manual extraction uses **lightweight regex** on `.adoc` text instead of a full AsciiDoc parser; a small noise list and tight patterns reduce false positives.
- Report generation is separated from parsing logic for modularity.

---

## Assumptions

- Extension tags from JSON and tokens from the manual converge after normalization.
- Some regex extraction noise from ISA manual sources is filtered explicitly.
- Instructions without usable extension metadata (`null`, missing key, or empty list) are skipped.

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
```
