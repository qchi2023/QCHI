# QCHI Desktop (Workbench Lite) Execution Plan

## Goal

Ship a Linux desktop app that feels like a lightweight VS Code/Antigravity workspace while keeping the existing QCHI Python backend and CLI as source of truth.

Primary command target:

- `qchi desktop`

Core UX target:

- Left: file explorer
- Center: tabbed editor
- Right: AI control and run output
- Bottom: terminal

Constraint:
- Interface can be VS Code-like, but we are not building a full VS Code fork.

## Why This Plan

- Full VS Code fork parity is too slow for current timeline.
- We need a shippable V1 quickly, with a path to deeper customization later.
- Existing backend APIs already provide filesystem, terminal, jobs, and status features.

## Scope

### In Scope (V1)

1. Add `desktop` subcommand in `bin/qchi`/`qchi_cli.py`.
2. Create a lightweight desktop shell (`desktop/`) based on VS Code-like layout and behavior.
3. Connect UI to existing QCHI APIs:
   - `/api/config`
   - `/api/status`
   - `/api/fs/tree`
   - `/api/fs/read`
   - `/api/fs/write`
   - `/api/terminal`
   - `/api/jobs`
   - `/api/jobs/<id>`
   - `/api/jobs/<id>/output`
4. Keep existing entry points working:
   - `qchi cli`
   - `qchi run`
   - `qchi web`
   - `qchi whatsapp serve`
5. Add Linux install/run docs for desktop mode.

### Out of Scope (V1)

1. Full deep fork of VS Code internals.
2. Rewriting backend orchestration in Rust.
3. Full marketplace/extension compatibility layer.
4. Prompt-skill-pack-driven AI behavior as the primary logic.

## Architecture (V1)

1. Backend:
   - Reuse `qchi_cli.py` web server and job pipeline.
   - Desktop launches or attaches to local backend server.
2. Frontend/Desktop:
   - Lightweight workbench shell with 4-pane layout.
   - Provider selection + physics task controls in AI panel.
3. Orchestration:
   - Existing QCHI host adapters remain primary execution path.
4. AI behavior layer:
   - QCHI-owned planner/solver/checker/refiner pipeline.
   - Structured templates and runtime state, not ad-hoc skills as core.

## Milestones

## M1: Branch + Planning + Baseline Validation

1. Create branch for desktop-lite work.
2. Commit planning docs only.
3. Validate baseline commands still run:
   - `python3 -m py_compile bin/qchi qchi_cli.py`
   - `python3 bin/qchi doctor --host codex`

Done when:
- Branch is pushed with plan docs and no destructive changes.

## M2: CLI Command Plumbing (`qchi desktop`)

1. Add `desktop` parser/subcommand.
2. Implement launcher behavior:
   - start backend if needed
   - pick available port (fallback if occupied)
   - launch desktop shell
3. Add clear logs for host/port/path.

Done when:
- `qchi desktop --help` works.
- `qchi desktop` launches app locally.

## M3: Lite Workbench UI

1. Build 4-pane IDE layout.
2. File tree open/save.
3. Tabbed editor behavior for opened files.
4. Terminal command execution panel.
5. AI task run panel and streaming/output view.

Done when:
- End-to-end user flow works from UI only.

## M4: Provider-Agnostic AI Configuration

1. Add provider selector in UI/config.
2. Support Codex/Gemini/custom command in V1.
3. Persist last-used provider and run settings.
4. Keep provider-independent physics workflow rules in backend code.

Done when:
- User can switch provider without code edits.

## M5: Packaging + Docs + Smoke Tests

1. Document Linux desktop setup and usage.
2. Verify npm-based `qchi` install path still works.
3. Add smoke test checklist in docs.

Done when:
- Fresh user can run `qchi desktop` from docs.

## Implementation Notes for Gemini Handoff

1. Keep changes minimal and incremental per milestone.
2. Do not block on perfect visuals; prioritize runnable architecture.
3. Do not regress existing CLI/WhatsApp behavior.
4. Preserve current dirty worktree files unless explicitly asked.
5. Do not introduce a VS Code fork dependency for V1.

## Suggested File Touches (Expected)

- `bin/qchi`
- `qchi_cli.py`
- `README.md`
- `docs/INSTALL_AND_USE.md`
- `docs/CHANGELOG.md`
- `desktop/` (new)

## Risks

1. Existing worktree contains many pending changes; avoid accidental staging.
2. Port collisions on local dev machine; implement auto-fallback.
3. Desktop dependencies may vary across Linux distros; document prerequisites.
4. AI behavior quality can drift if too much is delegated to free-form prompts.

## Acceptance Checklist

1. `qchi desktop` exists and runs.
2. 4-pane layout is functional.
3. File read/write works through APIs.
4. Terminal panel executes commands.
5. AI task submit + output polling works.
6. Existing commands still pass smoke checks.
7. Docs are updated with exact run steps.
8. AI flow is QCHI-controlled and provider-agnostic.
