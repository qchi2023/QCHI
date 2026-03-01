# QCHI Project Brief

## What We Are Building

QCHI is a physics-focused multi-agent system with three user interfaces:

1. `qchi cli` for terminal-first usage.
2. `qchi desktop` for a VS Code/Antigravity-style desktop app.
3. `qchi whatsapp` for chat-based control and responses.

Optional:

4. `qchi web` can remain as fallback, but desktop is the primary UI target.

## Product Direction (Final Intent)

- Core purpose: solve and learn physics tasks over time.
- Multi-agent behavior: agents can collaborate, critique, and improve outputs.
- Continuous learning: logs, runs, evaluations, and regressions should improve future performance.
- Provider flexibility: user can choose AI host/provider (Codex, Gemini, custom command, etc.).
- Control surface: everything should be operable from desktop UI or WhatsApp, with CLI always available.

## UX Target

Desktop app should feel like Antigravity/VS Code:

- Left: file tree/workspace explorer.
- Center: tabbed editor for files and outputs.
- Right: AI panel (task input, agent activity, run output, logs).
- Bottom: terminal panel.

## What Is Already Done

- CLI subcommands implemented in `bin/qchi`:
  - `run`
  - `doctor`
  - `lint`
  - `version`
- Backward compatibility kept:
  - `python3 bin/qchi --mode ... --task ...` still maps to `run`.
- `doctor` checks host availability, `qchi-lint`, and Rust toolchain.
- `lint` supports:
  - `qchi lint report --file <md>`
  - `qchi lint jsonl --kind <runs|evals|regressions> --file <jsonl>`
- Docs updated:
  - `README.md`
  - `docs/INSTALL_AND_USE.md`
  - `docs/HOST_COMMANDS.md`
  - `docs/CHANGELOG.md`
- npm package exists (`qchi-cli`) and exposes `qchi` command through:
  - `npm/bin/qchi.js`

## Current Gaps

- Desktop app command (`qchi desktop`) is not implemented yet.
- Current web UI quality is below target.
- "Always-on" WhatsApp production workflow needs stronger service setup (systemd/supervisor + docs).
- End-to-end UX parity across CLI/Desktop/WhatsApp is incomplete.

## Engineering Decision

Primary direction: VS Code-based desktop product with custom QCHI behavior.

Practical implementation path:
- Use Code-OSS as the base (VS Code open-source core).
- Build QCHI as a first-class extension/workbench integration.
- Keep QCHI Python backend as orchestration engine.
- Keep provider layer open so user can choose any AI host/provider.

Important scope control:
- V1 should avoid deep core patching of VS Code internals.
- Prefer extension-level customization + branding + commands first.
- If needed later, move to deeper fork changes in V2+.

## Lite VS Code Profile (Required)

QCHI desktop should be a lightweight Code-OSS distribution, not full heavyweight VS Code.

V1 constraints:
- Keep only features needed for QCHI workflow: explorer, editor tabs, terminal, QCHI AI panel.
- Disable/remove non-essential built-in extensions and views.
- Disable telemetry and update checks for this custom build.
- Keep startup fast and memory usage lower than stock full setup.
- Physics-first UX: QCHI controls should be top-level, not buried.

Packaging goal:
- Linux-first build artifact that launches quickly and feels minimal.

## Required Commands (Target)

User should be able to run:

1. `qchi cli`
2. `qchi run --host <provider> --mode physics_solve --task "..."`
3. `qchi desktop`
4. `qchi whatsapp serve ...`

Optional:

5. `qchi web`

## Backend APIs To Reuse

Desktop should consume existing endpoints:

- `/api/config`
- `/api/status`
- `/api/fs/tree`
- `/api/fs/read`
- `/api/fs/write`
- `/api/terminal`
- `/api/jobs`
- `/api/jobs/<id>`
- `/api/jobs/<id>/output`

## Definition Of Done (V1)

1. `qchi desktop` opens a Linux desktop app.
2. Desktop has 4-pane IDE layout (left files, center editor, right AI, bottom terminal).
3. Task submission from desktop runs through existing job pipeline.
4. File read/write works from desktop.
5. Terminal execution works from desktop.
6. CLI and WhatsApp commands still function.
7. npm installation still works for CLI on Linux.
8. Setup and run docs are updated and reproducible.
9. Desktop build follows Lite profile (minimal features, fast startup).

## Definition Of Done (V2)

1. Robust WhatsApp always-on deployment guide (systemd service).
2. Run artifact logging and replay in desktop.
3. Learning dashboards integrated in desktop.
4. Physics benchmark loop and regression reporting exposed in UI.

## Immediate Next Work

1. Bootstrap Code-OSS workspace locally (checked-out source, buildable state).
2. Create `qchi-vscode-extension/` with:
   - provider-agnostic AI adapters
   - physics task command palette actions
   - agent output/log panels
3. Add `qchi desktop` launcher command to start the customized desktop product.
4. Integrate extension with existing local backend APIs.
5. Verify Linux run flow and document install/build/run.

## AI Provider Flexibility (Requirement)

QCHI desktop must support selectable providers at runtime:

1. Codex/OpenAI-compatible endpoint.
2. Gemini.
3. Anthropic (if configured).
4. Local models (e.g., Ollama) through compatible adapter.
5. Custom command template adapter (advanced users).
