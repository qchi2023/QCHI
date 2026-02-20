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
4. Symbolic verification for analytical claims (Mathematica preferred; SymPy fallback).
5. Numerical verification where applicable.
6. arXiv-first source discipline.
7. Claim provenance tags:
   - REPRODUCED_FROM_SOURCE
   - INFERRED_ASSUMPTION
   - NEW_EXTENSION
8. Continuous learning loop is mandatory:
   - log failures
   - extract heuristics
   - run evals
   - run repeated-run stability checks
   - update behavior only when eval deltas and reliability metrics confirm improvement
9. Reliability target is "cannot-play-incorrectly" (high repeated-run consistency), not one-off correctness.
10. Knowledge expansion should include textbook/monograph ingestion (not only loop-learned heuristics).
11. Acquisition workflow: skill collects freely accessible sources directly and queues paywalled sources for user-provided files.
12. Multi-agent orchestration is supported via role protocols and structured inter-agent handoffs.

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
- NotebookLM-assisted workflows
- generic LLM chat interfaces
