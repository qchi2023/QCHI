---
name: qchi-top-layer
description: Unified top-layer for rigorous physics-theorist execution across QCHI-AI workflows. Use for physics problem solving, paper reproduction, LyX-first research artifacts, arXiv-first citation mapping, parameter-space studies, plotting quality gates, and publishable draft preparation with strict claim provenance.
---

# QCHI Top Layer

Run a rigor-first physics workflow with explicit assumptions, derivations, checks, provenance, and reproducibility.

## Required output contract

Always include these sections:
1. Problem framing
2. Assumptions and regime
3. Governing equations
4. Derivation
5. Validation checks
6. Final result
7. Interpretation and confidence
8. Claim provenance
9. References

Use template: `templates/OUTPUT_TEMPLATE.md`.

## Non-negotiables

- No shortcut/fast mode that skips rigor.
- No fabricated formulas or citations.
- Analytical-first when feasible, then numerical verification when applicable.
- Mandatory checks: units, limits, asymptotics, and one consistency check.
- Tag major claims as:
  - `REPRODUCED_FROM_SOURCE`
  - `INFERRED_ASSUMPTION`
  - `NEW_EXTENSION`

## Paper reproduction mode

Ask first:
- arXiv ID/version
- target equations/figures/theorems
- acceptable numeric tolerance
- desired depth (core vs full dossier)

Then follow `references/PAPER_REPRO_FLOW.md`.

## Artifact policy (LyX-first)

Maintain three separate tracks:
- notes
- systematics_plots
- publishable_draft

Do not merge tracks. Follow `references/LYX_ARTIFACT_POLICY.md`.

## Plot/parameter policy

- Default figure format: SVG.
- Use coarse-to-fine parameter sweeps.
- Attach metadata for each batch and link plots to source run.

See:
- `references/PARAMETER_SPACE_POLICY.md`
- `references/PLOTTING_POLICY.md`

## Quality gate

Before final output, pass all checks in:
- `checklists/QUALITY_GATE.md`

If a check fails, report failure and required corrective action.
