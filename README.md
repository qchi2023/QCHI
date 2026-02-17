# QCHI-AI Portable Top Layer

Portable, model-agnostic top-layer spec for a rigorous physics-theorist assistant.

## Purpose
Build once, run on any AI stack (ChatGPT, Claude, Gemini, local models, OpenClaw wrappers).

## Repo Structure
- `docs/` canonical specs and workflows
- `templates/` reusable prompt and output templates
- `checklists/` execution and quality gates
- `scripts/` deterministic helpers (optional)
- `examples/` sample tasks and expected output patterns
- `tests/` lightweight validation harnesses
- `dist/` packaged exports

## Operating Rules
1. Rigor first, no shortcut mode.
2. Derivation before conclusion.
3. Explicit assumptions + validity regime.
4. Units, limits, asymptotics, consistency checks required.
5. arXiv-first citation discipline.
6. Clear separation of reproduced vs inferred vs extension claims.

## Build Process
1. Finalize canonical docs in `docs/`.
2. Add model-agnostic templates in `templates/`.
3. Add checklists and validator scripts.
4. Validate with examples/tests.
5. Export OpenClaw-compatible skill package from this repo.

## Git Workflow
- Branch: `main`
- Commit after each meaningful block
- Keep concise changelog entries in `docs/CHANGELOG.md`
