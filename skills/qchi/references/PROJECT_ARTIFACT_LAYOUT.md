# Project Artifact Layout

This defines where AI must save project outputs.

## Root
- `projects/<project-id>/`

## Required subfolders
- `projects/<project-id>/artifacts/lyx/`
- `projects/<project-id>/artifacts/plots/`
- `projects/<project-id>/artifacts/data/`
- `projects/<project-id>/artifacts/reports/`

## LyX files
Save LyX tracks here
- `projects/<project-id>/artifacts/lyx/notes.lyx`
- `projects/<project-id>/artifacts/lyx/systematics_plots.lyx`
- `projects/<project-id>/artifacts/lyx/publishable_draft.lyx` (only if explicitly requested)

## Plot and numeric outputs
- figures: `projects/<project-id>/artifacts/plots/`
- raw arrays/tables: `projects/<project-id>/artifacts/data/`
- run summaries and check reports: `projects/<project-id>/artifacts/reports/`

## Learning linkage
Project learning remains in
- `skills/qchi/learning/projects/<project-id>/physics/`
- `skills/qchi/learning/projects/<project-id>/writing/`
- `skills/qchi/learning/projects/<project-id>/coding-plotting/`

## Rules
- never mix outputs from different projects in the same artifact folder
- use stable project id format `proj-<name>-<yyyy>`
- for paper reproduction create a subfolder under plots/data using arXiv id
