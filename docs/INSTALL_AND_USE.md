# Install and Use QCHI

This repo contains a portable skill core at `skills/qchi/`.

## A) OpenClaw install

1. Build package
```bash
# from repo root
python3 scripts/package_skill.py skills/qchi dist
```

2. Install in OpenClaw
- Copy `dist/qchi.skill` to the target machine
- Import/install it in your OpenClaw skill manager

3. Use
- Ask tasks that match the skill scope, for example
  - "work on unfinished project X"
  - "reproduce arXiv:XXXX.XXXXX"
  - "run parameter-space analysis for ..."

## B) Generic host use (Codex, Claude Code, Cursor, Antigravity)

1. Use canonical instructions from
- `skills/qchi/SKILL.md`
- `skills/qchi/references/`

2. Apply host adapter notes from
- `skills/qchi/adapters/openclaw.md`
- `skills/qchi/adapters/cursor.md`
- `skills/qchi/adapters/antigravity.md`
- `skills/qchi/adapters/opencode.md`
- `skills/qchi/adapters/generic.md`

3. Keep learning logs in
- `skills/qchi/learning/`
- `skills/qchi/learning/projects/<project-id>/...`

## C) Expected behavior defaults
- Full serious mode by default
- Paper reproduction defaults to multi-agent unless user asks single-agent
- `publishable_draft.lyx` only when explicitly requested
- Direct `.lyx` writing workflow only

## D) Verification
- CI workflow: `.github/workflows/qchi-lint.yml`
- Rust lint scaffold: `tools/qchi-lint/`
- Project-learning layout validator: `tools/validate_project_learning.py`
