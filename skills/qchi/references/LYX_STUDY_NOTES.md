# LyX Study Notes for QCHI (from official manuals)

Source set studied
- `references/lyx-docs/Tutorial.pdf`
- `references/lyx-docs/UserGuide.pdf`
- `references/lyx-docs/Math.pdf`

Extraction workspace
- `references/lyx-docs/extracted/Tutorial.txt`
- `references/lyx-docs/extracted/UserGuide.txt`
- `references/lyx-docs/extracted/Math.txt`

## Core operational lessons

1) LyX is structure-first, not freeform text
- Content must be inside valid document/header/body blocks.
- Layouts and insets drive semantics.

2) Labels and cross-references are first-class
- Use labels for sections/equations/floats and cross-reference those labels.
- Hardcoded numbering is fragile and should be rejected.

3) Math authoring must use proper math constructs
- Math mode/insets are required for formulas.
- Plain text pseudo-equations are invalid for robust export.

4) Export is the real validity test
- A `.lyx` file that cannot export to LaTeX/PDF is not acceptable.
- Conformance should treat export failure as hard fail.

5) Bibliography/citations are structured objects
- Citation management should remain in LyX structures, not ad-hoc plain text replacements.

## QCHI implications

A) Mandatory preflight for any reproduction run
- Initialize target LyX files from template.
- Ensure template can export before writing domain content.

B) Mandatory postflight
- LyX lint + export check must pass for `notes.lyx` and `systematics_plots.lyx`.
- If export fails, run is fail regardless of textual quality.

C) Authoring guardrails
- No hardcoded internal numbering.
- Labels required for structured references.
- Reject markdown/plain-text disguised as `.lyx`.

## Immediate protocol direction

- Keep strict conformance gate as final authority.
- Continue strengthening label/reference checks to mirror real LyX semantics.
- Add targeted test corpus of valid/invalid LyX fixtures for regression testing of lint.
