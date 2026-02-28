# QCHI Handoff State (Session Resumption)

**To Gemini CLI:**
The user has switched machines. Read this document carefully. It contains the exact state of the QCHI project and our immediate next steps. You must resume work based on this context.

## Current Project State
*   **Repository:** `https://github.com/qchi2023/QCHI`
*   **Active Branch:** `feat/cli-development` (We created this branch to safely build the CLI without breaking `main`).
*   **Core Architecture Decision:** We have abandoned the idea of "Passive Markdown Skills." QCHI is now an **Active CLI Orchestrator** (`bin/qchi`). 
*   **How the CLI Works:** The Python script at `bin/qchi` does *not* use HTTP APIs. It uses `subprocess` to authorize and drive native host CLIs (like `gemini`, `codex`, `antigravity`) in a strict, multi-agent loop (Planner -> Derivation -> Verifier).
*   **The Problem We Are Solving:** LLMs suffer from prompt drift and conversational bias. The `qchi` CLI fixes this by intercepting the AI's output and passing it to a Rust-based Rigor Engine (`tools/qchi-lint`). If the linter fails, the CLI forces the AI into a retry loop.

## What Was Completed Today
1.  **Project Flow Documentation:** Rebuilt `QCHI_PROJECT_FLOW.html` into a highly detailed, interactive technical roadmap using Mermaid.js. It highlights the critical gaps in the Rigor Engine and Learning Loop.
2.  **LyX Authoring Protocol:** Added a strict "Safe Editing Protocol for LLMs" (Block-Level Replacement Only) to `SKILL.md` and `LYX_DIRECT_AUTHORING_PROTOCOL.md` to prevent AI from breaking LyX syntax during edits.
3.  **Mandatory Subagents:** Updated all references to enforce that **subagents are mandatory for all modes**. Sequential simulation is no longer allowed.
4.  **The Orchestrator:** Scaffolded the `bin/qchi` Python executable. It currently simulates the Planner and Derivation steps by invoking the host CLI.
5.  **Rust Setup:** Installed Rust/Cargo and successfully compiled the `tools/qchi-lint` scaffold.

## Immediate Next Steps (Where to Resume)
1.  **Wire the Linter to the CLI:** The `run_qchi_lint()` function in `bin/qchi` is currently a stub that just checks for the string "NEW_EXTENSION". **You must wire this function to execute the compiled Rust binary (`tools/qchi-lint/target/debug/qchi-lint`).**
2.  **Harden the Rust Linter:** The `src/main.rs` file inside `tools/qchi-lint/` is weak. You need to write the actual Rust logic that parses the output and enforces the "Four Horsemen" validation checks (Units, Limits, Asymptotics, Consistency) and verifies the presence of Symbolic Verification logs.

## Setup Instructions for the New Machine
Before you begin coding, ensure the new environment is ready:
1.  Verify the repo is cloned and on the `feat/cli-development` branch.
2.  Ensure Rust is installed (`cargo --version`).
3.  Ensure the AI host CLI (e.g., `gemini`) is installed and authenticated on the new system PATH.

**End of Handoff.**