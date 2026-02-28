# QCHI

Standalone, portable research operating layer for rigorous theoretical-physics workflows.

## Canonical Goal
Build one reusable system that works across hosts (OpenClaw, Antigravity, Cursor, OpenCode, generic LLM interfaces) while preserving rigorous behavior.

## Canonical docs
- `docs/PROJECT_INTENT.md` (source of truth)
- `docs/TOP_LAYER_PORTABLE_SPEC.md`
- `docs/WORKFLOW_PORTABLE.md`
- `docs/PORTABILITY_PLAN.md`
- `docs/INSTALL_AND_USE.md` (how to install and run)
- `docs/INSTALL_PREREQS.md` (program prerequisites)
- `docs/HOST_COMMANDS.md` (host-by-host command quickstart)
- `docs/OPENCODE_REGISTER.md` (register QCHI in OpenCode)

## Portable skill package
- Source of truth: `skills/qchi/`
- Dist artifacts are generated snapshots under `dist/` (names may vary by build history)
- Rebuild/export artifacts from current `skills/qchi/` before release

## End-to-end flow (v1)

```mermaid
flowchart TD
    A[User task] --> B[Select mode and project scope]
    B --> C[Derivation-first execution]
    C --> D[Validation checks<br/>units limits asymptotics consistency]
    D --> E[Verification<br/>symbolic + numeric where applicable]
    E --> F[Claim provenance tagging]
    F --> G[Artifact output<br/>notes.lyx systematics_plots.lyx publishable_draft.lyx]
    G --> H[Quality gate]
    H -->|pass| I[Log learning artifacts]
    H -->|fail| C

    I --> P1[Project track physics]
    I --> P2[Project track writing]
    I --> P3[Project track coding-plotting]

    P1 --> I1[runs.jsonl evals.jsonl regressions.jsonl heuristics.yaml]
    P2 --> I2[runs.jsonl evals.jsonl regressions.jsonl heuristics.yaml]
    P3 --> I3[runs.jsonl evals.jsonl regressions.jsonl heuristics.yaml]

    I1 --> J[Regression suite plus promotion gates]
    I2 --> J
    I3 --> J

    J -->|improves reliability| K[Promote heuristic or behavior]
    J -->|regression detected| L[Revert or keep as candidate]

    K --> M[Commit and push to GitHub]
    L --> M

    M --> R[Friend branch or PR contribution]
    R --> S[CI gates qchi-lint plus project-learning validator]
    S -->|pass| T[Merge to main]
    S -->|fail| U[Fix and rerun]

    T --> N[Portable reuse across hosts<br/>OpenClaw Codex Claude Code Cursor Antigravity]
```

## Quick map
- Core skill: `skills/qchi/SKILL.md`
- Project artifact layout: `skills/qchi/references/PROJECT_ARTIFACT_LAYOUT.md`
- Learning store: `skills/qchi/learning/`
- Project learning layout: `skills/qchi/references/LEARNING_PROJECT_LAYOUT.md`
- Rigor policies: `skills/qchi/references/`
- Quality gate: `skills/qchi/checklists/QUALITY_GATE.md`
- Rust lint scaffold: `tools/qchi-lint/`
- CI workflow: `.github/workflows/qchi-lint.yml`
- Conformance runner: `scripts/run_conformance.sh`

## CLI quickstart
QCHI includes an executable orchestrator at `bin/qchi`.

```bash
python3 bin/qchi doctor --host gemini
python3 bin/qchi run --host gemini --mode physics_solve --task "derive harmonic oscillator normalization"
python3 bin/qchi lint report --file templates/OUTPUT_TEMPLATE.md
python3 bin/qchi version
```

`qchi run` now saves run artifacts by default to `.qchi/runs/<task_id>/` including role outputs, attempt logs, and final summary.
Override with `--run-artifacts-dir <path>` or `QCHI_RUN_ARTIFACTS_DIR`.

The `run` command enforces mandatory role evidence:
- planner
- derivation
- symbolic_verifier
- numeric_verifier
- referee
- integrator

For `paper_reproduction` mode, `source_miner` is also mandatory.
<!-- Initializing QCHI fix phase - qchi2023 -->
