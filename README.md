# RISC-V Instruction Set Explorer

## Project Description

A metadata exploration and reconciliation tool for parsing and analyzing RISC-V instruction-extension relationships from the RISC-V Extensions Landscape repository and the official RISC-V ISA manual.

---

## Setup and run

1. **Clone this repository**:

```bash
git clone https://github.com/Veekshitha11/RISC-V.git
cd RISC-V
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Clone the ISA manual** (required for Tier 2):

```bash
git clone https://github.com/riscv/riscv-isa-manual
```

   You should have `riscv-isa-manual/src/` with `.adoc` files before running Tier 2.

4. **Run the program** (Tier 1 + Tier 2 + Tier 3 in one command):

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

5. **Tests**:

```bash
pytest
```

Instruction metadata is read from `data/instr_dict.json`. The landscape project that publishes it is:

https://github.com/rpsene/riscv-extensions-landscape

Copy or download `instr_dict.json` into `data/` when you want a newer snapshot.

---

## Sample output

**Tier 1 — extension summary (excerpt)**

```text
Extension Summary
-------------------------------------------------------
rv_zba | 3 instructions | e.g. SH1ADD
rv_zbb | 17 instructions | e.g. ANDN
rv_zbc | 3 instructions | e.g. CLMUL
...
-------------------------------------------------------
Total extensions:    114
Total instructions:  1343
```

**Tier 1 — instructions with multiple extensions (excerpt)**

```text
Instructions With Multiple Extensions
-------------------------------------------------------
ANDN -> rv_zbb, rv_zkn, rv_zks, rv_zk, rv_zbkb
CLMUL -> rv_zbc, rv_zkn, rv_zks, rv_zk, rv_zbkc
SHA256SIG0 -> rv_zknh, rv_zkn, rv_zk
```

**Tier 2 — cross-reference (excerpt)**

```text
Cross Reference Summary
-------------------------------------------------------
Matched Extensions: 57
JSON Only Extensions: 29
Manual Only Extensions: 85

57 matched, 29 in JSON only, 85 in manual only

Matched Extensions
-------------------------------------------------------
A
C
D
F
I
M
Zba
Zbb
Zicsr
...
```

Numbers depend on your `instr_dict.json` snapshot and ISA manual revision.

**Tier 3 — graph (excerpt)**

```text
Extension Relationship Graph
-------------------------------------------------------
rv_zbb | 4 neighbor(s)
  -> rv_zbkb | shared: ANDN, ORN, ROL, ROR, XNOR
  -> rv_zk | shared: ANDN, ORN, ROL, ROR, XNOR
  -> rv_zkn | shared: ANDN, ORN, ROL, ROR, XNOR
  -> rv_zks | shared: ANDN, ORN, ROL, ROR, XNOR
rv_zbc | 4 neighbor(s)
  -> rv_zbkc | shared: CLMUL, CLMULH
  -> rv_zk | shared: CLMUL, CLMULH
  ...
```

A GraphViz DOT file is also written to `output/extension_graph.dot`
and can be rendered at https://graphviz.online

<img width="1568" height="563" alt="image" src="https://github.com/user-attachments/assets/b82ed023-e30c-4231-b4f5-de3f0a10c60c" />


---

## What "JSON only" and "manual only" mean

- **JSON only** — An extension tag appears in `instr_dict.json` (after normalization), but no matching extension name was found in the scanned ISA manual `.adoc` files. Often newer or vendor-specific extensions, or limits of regex extraction.
- **Manual only** — A name was picked up from the manual, but no instruction in your JSON is tagged with that extension after normalization. Can be ratified chapters not in the snapshot, or false positives from loose patterns.

---

## Implemented Features

### Tier 1

- Parse instruction metadata from `instr_dict.json`
- Group instructions by extension tags
- Generate extension summary reports with instruction counts and example mnemonics
- Detect instructions belonging to multiple extensions

### Tier 2

- Extract extension references from ISA manual AsciiDoc files
- Normalize extension naming across repositories
- Cross-reference extension metadata between datasets
- Report matched, JSON-only, and manual-only extensions with count summary

### Tier 3

- Unit tests using `pytest`
- Extension relationship graph generation (text and GraphViz DOT format)
- Shared instruction dependency visualization

---

## Architecture

- `parser.py` → instruction parsing and grouping
- `reporter.py` → Tier 1 report generation
- `normalizer.py` → canonical extension normalization
- `manual_parser.py` → ISA manual extension extraction
- `cross_reference.py` → extension reconciliation and mismatch reporting
- `graph_generator.py` → extension relationship graph generation

---

## Design Decisions

- Extension names are **normalized to one canonical form** (for example `rv_zba` and `Zba` both become `Zba`) before cross-referencing so JSON and manual sets compare fairly.
- **Single-letter base extensions** (`I`, `M`, `F`, …) use an explicit mapping table after stripping `rv_` / `rv32_` / `rv64_` prefixes. Title-casing or a generic regex alone is not enough: `rv_i` must become `I`, not `Zi`, and `rv64_i` is treated as `RV64I`, not the same as base `I`.
- Instructions are modeled as **many-to-many relationships** between mnemonics and extension tags. An instruction like `ANDN` belonging to five extensions is handled correctly.
- ISA manual extraction uses **lightweight regex** on `.adoc` text instead of a full AsciiDoc parser. A noise list of common English words and known author surnames from the manual's contributor sections prevents false positives.
- The **extension relationship graph is built instruction-first**: for each instruction belonging to two or more extensions, an edge is added between every pair of those extensions and the shared mnemonic is recorded on that edge. Building extension-first would not naturally surface the shared instruction evidence.
- The graph is written as both a **human-readable text file** and a **GraphViz DOT file** so evaluators can visualize it instantly at https://graphviz.online without installing anything.
- Report generation is **separated from parsing logic** for modularity — each module can be tested and replaced independently.

---

## Assumptions

- Extension tags from JSON and tokens from the manual converge after normalization.
- Some regex extraction noise from ISA manual sources is filtered explicitly.
- Instructions without usable extension metadata (`null`, missing key, or empty list) are skipped silently.
- The ISA manual is not bundled in this repo — it is a runtime dependency cloned separately.

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
