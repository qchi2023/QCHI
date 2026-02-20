# QCHI

Standalone, portable research operating layer for rigorous theoretical-physics workflows.

## Canonical Goal
Build one reusable system that works across hosts (OpenClaw, Antigravity, Cursor, OpenCode, generic LLM interfaces) while preserving rigorous behavior.

## Canonical docs
- `docs/PROJECT_INTENT.md` (source of truth)
- `docs/TOP_LAYER_PORTABLE_SPEC.md`
- `docs/WORKFLOW_PORTABLE.md`
- `docs/PORTABILITY_PLAN.md`

## Portable skill package
- `skills/qchi-r/`
- OpenClaw package output: `dist/qchi-r.skill`
- Generic package output: `dist/qchi-r-portable.zip`

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

    I --> I1[runs.jsonl]
    I --> I2[evals.jsonl]
    I --> I3[regressions.jsonl]
    I --> I4[heuristics.yaml]

    I1 --> J[Regression suite]
    I2 --> J
    I3 --> J
    I4 --> J

    J -->|improves reliability| K[Promote heuristic or behavior]
    J -->|regression detected| L[Revert or keep as candidate]

    K --> M[Commit and push to GitHub]
    L --> M

    M --> N[Portable reuse across hosts<br/>OpenClaw Codex Claude Code Cursor Antigravity]
```

## Quick map
- Core skill: `skills/qchi-r/SKILL.md`
- Learning store: `skills/qchi-r/learning/`
- Rigor policies: `skills/qchi-r/references/`
- Quality gate: `skills/qchi-r/checklists/QUALITY_GATE.md`
- Rust lint scaffold: `tools/qchi-lint/`
- CI workflow: `.github/workflows/qchi-lint.yml`
