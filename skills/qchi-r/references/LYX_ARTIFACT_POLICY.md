# LyX Artifact Policy

Maintain exactly three tracks:
- notes.lyx
- systematics_plots.lyx
- publishable_draft.lyx

Rules:
- no merging tracks
- no promotion to draft without evidence linkage
- cross references required for equations/figures/tables/sections
- assign a unique label to every equation figure table and section
- use `\ref` for all internal references do not use hardcoded numbers
- do not use `:` in `.lyx` writing/output unless explicitly overridden by user
- direct `.lyx` authoring only no conversion pipeline from markdown or tex
- follow `references/LYX_DIRECT_AUTHORING_PROTOCOL.md`
- use local LyX docs listed in `references/LYX_DOCS_INDEX.md`
