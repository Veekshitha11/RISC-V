# RISC-V Instruction Set Explorer


## Project Description

A metadata exploration tool for parsing and analyzing RISC-V instruction-extension relationships from the RISC-V Extensions Landscape repository.

## Implemented Features

- Parse instruction metadata from instr_dict.json
- Group instructions by extension tags
- Generate extension summary reports
- Detect instructions belonging to multiple extensions
- Export reports to output/summary.txt

## Project Structure

- src/parser.py      -> parsing and grouping logic
- src/reporter.py    -> report generation
- main.py            -> orchestration pipeline

## How To Run
 
 ```bash
py main.py
```
## Assumptions

- Instructions without extension tags are skipped
- Extension tags are treated as case-sensitive




