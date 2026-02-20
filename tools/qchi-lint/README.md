# qchi-lint (Rust)

Policy and artifact linter for QCHI v1.

## Scope
- Lint generated report markdown for required QCHI sections and provenance tags.
- Lint learning-store JSONL files for required fields and basic score bounds.

## Build
Requires Rust toolchain (cargo).

```bash
cd tools/qchi-lint
cargo build --release
```

## Usage
```bash
# report structure
cargo run -- report --file ../../skills/qchi-r/templates/OUTPUT_TEMPLATE.md

# learning logs
cargo run -- jsonl --kind runs --file ../../skills/qchi-r/learning/runs.jsonl
cargo run -- jsonl --kind evals --file ../../skills/qchi-r/learning/evals.jsonl
cargo run -- jsonl --kind regressions --file ../../skills/qchi-r/learning/regressions.jsonl
```
