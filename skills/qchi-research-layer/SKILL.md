---
name: qchi-research-layer
description: Portable, host-agnostic research operating layer for rigorous theoretical-physics work. Use for derivation-first problem solving, paper reproduction, LyX-first artifact workflows, parameter-space studies, plot quality gates, and publication-ready claim provenance with arXiv-first references.
---

# QCHI Research Layer

This is the canonical portable layer. Host adapters live under `adapters/`.

## Required output sections
1. Problem framing
2. Assumptions and regime
3. Governing equations
4. Derivation
5. Validation checks
6. Final result
7. Interpretation and confidence
8. Claim provenance
9. References

Use: `templates/OUTPUT_TEMPLATE.md`.

## Mandatory rules
- Analytical-first when feasible.
- No fabricated formulas/citations.
- Must run: units, limiting-case, asymptotic, and consistency checks.
- Tag key claims as REPRODUCED_FROM_SOURCE / INFERRED_ASSUMPTION / NEW_EXTENSION.
- If uncertain, disclose uncertainty + verification plan.

## Research modes
- Physics solve mode
- Paper reproduction mode
- Parameter-space/plot mode
- Publishable draft mode

See `references/WORKFLOW_MODES.md` and `references/PAPER_REPRO_FLOW.md`.

## Quality gate
Before finalizing, pass all checks in `checklists/QUALITY_GATE.md`.
