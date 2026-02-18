---
name: qchi-r
description: QCHI-R portable, host-agnostic research operating layer for rigorous theoretical-physics work. Use for derivation-first problem solving, paper reproduction, LyX-first artifact workflows, parameter-space studies, plot quality gates, and publication-ready claim provenance with arXiv-first references.
---

# QCHI-R

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
- Continuous learning loop is required after meaningful work:
  1) log failure patterns
  2) extract/update heuristics
  3) run evals
  4) keep changes only if eval quality improves

## Research modes
- Physics solve mode
- Paper reproduction mode
- Parameter-space/plot mode
- Publishable draft mode

See `references/WORKFLOW_MODES.md` and `references/PAPER_REPRO_FLOW.md`.
For reliability and verification enforcement, also use:
- `references/RELIABILITY_TARGETS.md`
- `references/MULTI_PATH_VERIFICATION.md`
- `references/COST_RELIABILITY_POLICY.md`.

## Quality gate
Before finalizing, pass all checks in `checklists/QUALITY_GATE.md`.

## Continuous learning loop operations
After meaningful work:
1. Record failure patterns.
2. Promote validated heuristics.
3. Run evals (including repeated-run reliability checks).
4. Track cost vs reliability.
5. Keep/revert behavior change based on eval + stability + CPIS criteria.

See:
- `references/LEARNING_LOOP_PROTOCOL.md`
- `references/RELIABILITY_TARGETS.md`
- `references/COST_RELIABILITY_POLICY.md`

Note: This skill is methodology-only. Python/Julia are for physics calculations, not for skill plumbing.