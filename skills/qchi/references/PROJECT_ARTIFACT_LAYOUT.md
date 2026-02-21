# Project Artifact Layout

This defines where AI must save project outputs.

## Root
- `~/Documents/QCHI-Projects/<project-id>/`

## Required subfolders
- `~/Documents/QCHI-Projects/<project-id>/artifacts/lyx/`
- `~/Documents/QCHI-Projects/<project-id>/artifacts/plots/`
- `~/Documents/QCHI-Projects/<project-id>/artifacts/data/`
- `~/Documents/QCHI-Projects/<project-id>/artifacts/reports/`

## LyX files
Save LyX tracks here
- `~/Documents/QCHI-Projects/<project-id>/artifacts/lyx/notes.lyx`
- `~/Documents/QCHI-Projects/<project-id>/artifacts/lyx/systematics_plots.lyx`
- `~/Documents/QCHI-Projects/<project-id>/artifacts/lyx/publishable_draft.lyx` (only if explicitly requested)

## Plot and numeric outputs
- figures: `~/Documents/QCHI-Projects/<project-id>/artifacts/plots/`
- raw arrays/tables: `~/Documents/QCHI-Projects/<project-id>/artifacts/data/`
- run summaries and check reports: `~/Documents/QCHI-Projects/<project-id>/artifacts/reports/`

## Learning linkage
Project learning remains in
- `skills/qchi/learning/projects/<project-id>/physics/`
- `skills/qchi/learning/projects/<project-id>/writing/`
- `skills/qchi/learning/projects/<project-id>/coding-plotting/`

## Rules
- never mix outputs from different projects in the same artifact folder
- use stable project id format `proj-<name>-<yyyy>`
- for paper reproduction create a subfolder under plots/data using arXiv id
