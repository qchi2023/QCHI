# LyX Direct Authoring Protocol (v1)

Goal
- make direct `.lyx` authoring reliable without Markdown or TeX conversion

## Core rules
- write directly in `.lyx`
- no `:` in `.lyx` output unless user explicitly overrides
- assign unique labels to every equation figure table and section
- use `\ref` for internal references
- do not hardcode equation or figure numbers in prose

## Safe edit order
0. initialize files from `references/LYX_MINIMAL_TEMPLATE.lyx` (or `tools/init_lyx_artifacts.sh`)
1. create or update section shell
2. insert equations and symbols
3. add labels immediately
4. add references with `\ref`
5. insert figures and captions
6. run LyX lint checks before finalize

## Required naming pattern
- sections: `sec-<topic>-<id>`
- equations: `eq-<topic>-<id>`
- figures: `fig-<topic>-<id>`
- tables: `tab-<topic>-<id>`

## Edge cases and handling
- duplicated labels
  - rename with stable suffix `-a`, `-b`
- moved equations
  - keep label unchanged if semantic identity is unchanged
- split sections
  - keep original section label for primary section and create new labels for new sections
- removed targets
  - remove dangling `\ref` in same change set

## Safe Editing Protocol for LLMs
Because LLMs often break `.lyx` files when using standard "find and replace" tools, you MUST follow these editing rules:
1. **Block-Level Replacement Only:** Never attempt to replace a single word or sentence inside a LyX paragraph. You must replace the ENTIRE `\layout Standard` block, from the `\layout` declaration to the empty line following it.
2. **Equation Replacement:** If you need to fix a math error, replace the entire `\begin_inset Formula ... \end_inset` block. Do not try to surgically edit the LaTeX inside it.
3. **Include the Wrappers:** When providing the `old_string` for a replacement tool, always include the `\layout` or `\begin_inset` tags to ensure you are targeting the exact structural block, preventing syntax corruption.

## Quality gates for LyX edits
- zero missing labels on equation figure table section
- zero hardcoded internal numbers (Equation 3, Fig 2, Section 4)
- zero dangling references
- no colon in `.lyx` output unless explicit override

## Local lint tool
- run `python3 tools/qchi_lyx_lint.py --root .`
- this checks LyX format validity, malformed `\label`/`\ref`, label prefixes, forbidden colon, dangling refs, hardcoded numbering, and LyX export viability
- reject `.lyx` files that are markdown/plain-text disguised as LyX
- use `--no-export-check` only for emergency debugging, never for final acceptance

## Source grounding
Use these local documents first
- `references/lyx-docs/Tutorial.pdf`
- `references/lyx-docs/UserGuide.pdf`
- `references/lyx-docs/Math.pdf`
