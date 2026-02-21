# Conformance Layer (Host-Agnostic)

Goal
- enforce identical pass/fail standards across hosts and models
- prevent fake compliance claims

## Required bundle for paper reproduction
Under `~/Documents/QCHI-Projects/<project-id>/artifacts/reports/`:

1. `compliance.json`
2. `repro_manifest.json`
3. `roles/source-miner.md`
4. `roles/derivation.md`
5. `roles/verifier.md`
6. `roles/referee.md`
7. `equation_coverage.json`

## Required artifact paths
- `~/Documents/QCHI-Projects/<project-id>/artifacts/lyx/notes.lyx`
- `~/Documents/QCHI-Projects/<project-id>/artifacts/lyx/systematics_plots.lyx`
- `publishable_draft.lyx` only if user explicitly requested

## Required learning paths
- `skills/qchi/learning/projects/<project-id>/physics/`
- `skills/qchi/learning/projects/<project-id>/writing/`
- `skills/qchi/learning/projects/<project-id>/coding-plotting/`

## Compliance contract
A run is PASS only if all conditions hold:
- LyX lint passes
- LyX export viability passes for `notes.lyx` and `systematics_plots.lyx`
- required role evidence files exist and are non-empty
- `compliance.json` exists with status=pass and gate summary
- `repro_manifest.json` exists with source/equation mapping entries
- `equation_coverage.json` exists and marks all in-scope equations as derived or blocked-with-reason
- project learning logs exist for all three tracks

Any missing item -> FAIL (no success claim allowed)
