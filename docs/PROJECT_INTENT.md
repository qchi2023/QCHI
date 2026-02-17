# QCHI Project Intent (Canonical)

QCHI is a standalone research operating layer for theoretical physics work.

## What QCHI is
A rigor-first workflow system that helps run real research tasks end-to-end:
- physics derivation and model analysis
- paper reproduction and validation
- parameter-space exploration and plotting
- claim provenance and citation discipline
- reproducible artifact generation

## What QCHI is not
- Not a chatbot persona project.
- Not only a prompt snippet.
- Not only an OpenClaw skill.

## Mandatory behavior
1. Analytical-first reasoning when feasible.
2. Explicit assumptions + validity regime.
3. Mandatory checks: units, limits, asymptotics, consistency.
4. Numerical verification where applicable.
5. arXiv-first source discipline.
6. Claim provenance tags:
   - REPRODUCED_FROM_SOURCE
   - INFERRED_ASSUMPTION
   - NEW_EXTENSION
7. Continuous learning loop is mandatory:
   - log failures
   - extract heuristics
   - run evals
   - update behavior only when eval deltas confirm improvement

## Artifact tracks (LyX-first)
- `notes.lyx`
- `systematics_plots.lyx`
- `publishable_draft.lyx`

Keep tracks separate.

## Portability objective
QCHI must be runnable across multiple AI hosts via adapters:
- OpenClaw
- Antigravity
- Cursor
- OpenCode
- generic LLM chat interfaces
