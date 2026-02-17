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

## Quality gate
Before finalizing, pass all checks in `checklists/QUALITY_GATE.md`.
Run helper:

`python3 scripts/quality_gate_check.py --input <response.md>`

## Continuous learning loop operations
After meaningful work:
1. Record failures:
   - `python3 scripts/record_failure.py --task ... --type ... --symptom ... --root ... --fix ...`
2. Promote validated heuristic:
   - `python3 scripts/promote_heuristic.py --rule "..." --evidence "..."`
3. Compare eval delta before/after:
   - `python3 scripts/run_evals.py --current current.json --baseline baseline.json --min-delta 0.0`
4. Keep/revert behavior change based on eval result.

See `references/LEARNING_LOOP_PROTOCOL.md`.
