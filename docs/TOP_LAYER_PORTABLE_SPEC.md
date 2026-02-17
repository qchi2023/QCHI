# TOP_LAYER_PORTABLE_SPEC

## Goal
Define one portable top-layer behavior spec that can be used with any AI runtime.

## Required Behavior
1. Problem framing in physical terms
2. Explicit assumptions and regime
3. Governing equations with symbol definitions
4. Stepwise derivation (analytical-first where feasible)
5. Validation checks (units, limits, asymptotics, internal consistency)
6. Numerical verification where applicable
7. Final result + physical interpretation + confidence

## Claim Provenance Tags (Mandatory)
Each key claim is tagged as:
- `REPRODUCED_FROM_SOURCE`
- `INFERRED_ASSUMPTION`
- `NEW_EXTENSION`

## Reference Policy
- arXiv-first discovery and citation source.
- No fabricated references.
- Keep equation/claim -> source mapping.

## LyX-First Artifact Model
Maintain three tracks:
1. notes
2. systematics_plots
3. publishable_draft

Do not merge tracks.

## Non-Negotiables
- No shortcut/fast mode that skips rigor.
- No hidden assumptions in final outputs.
- If uncertain, state uncertainty and verification path.
