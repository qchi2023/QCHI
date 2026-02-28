#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

# QCHI CLI: The Active Methodology Straitjacket
# This CLI enforces compliance by orchestrating host CLIs (Gemini/Codex/etc.)
# through mandatory role-segregated sub-agents and local policy linting.

QCHI_CLI_VERSION = "0.4.0"

SUPPORTED_HOSTS = ["gemini", "codex", "antigravity", "opencode"]
HOST_BINARIES = {
    "gemini": "gemini",
    "codex": "codex",
    "antigravity": "antigravity",
    "opencode": "opencode",
}

HOST_INSTALL_HINTS = {
    "gemini": "Install/auth Gemini CLI, then run: gemini --help",
    "codex": "Install/auth Codex CLI, then run: codex --help",
    "antigravity": "Install/auth Antigravity CLI, then run: antigravity --help",
    "opencode": "Install/auth OpenCode CLI, then run: opencode --help",
}

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parent.parent if SCRIPT_PATH.parent.name == "bin" else SCRIPT_PATH.parent
DEFAULT_LINT_CANDIDATES = [
    REPO_ROOT / "tools" / "qchi-lint" / "target" / "debug" / "qchi-lint",
    REPO_ROOT / "tools" / "qchi-lint" / "target" / "release" / "qchi-lint",
]
DEFAULT_RUN_ARTIFACTS_ROOT = REPO_ROOT / ".qchi" / "runs"
DEFAULT_LEARNING_DIR = REPO_ROOT / "skills" / "qchi" / "learning"
DEFAULT_LEARNING_TRACK = "physics"
LEARNING_TRACKS = ["physics", "writing", "coding-plotting"]
PROJECT_HEURISTICS_TEMPLATE = "version: 1\nlast_updated: null\nheuristics: []\n"
DEFAULT_DASHBOARD_PORT = 8787
DEFAULT_DASHBOARD_BIND = "127.0.0.1"

CORE_REQUIRED_ROLES = [
    "planner",
    "derivation",
    "symbolic_verifier",
    "numeric_verifier",
    "referee",
    "integrator",
]

ROLE_DISPLAY_NAMES = {
    "planner": "Planner",
    "source_miner": "Source Miner",
    "derivation": "Derivation",
    "symbolic_verifier": "Symbolic Verifier",
    "numeric_verifier": "Numeric Verifier",
    "referee": "Referee",
    "integrator": "Integrator",
}

VALID_DECISIONS = {"pass", "fail", "deferred", "not_applicable", "unknown"}


class HostExecutionError(RuntimeError):
    pass


def positive_int(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer value: {value}") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be >= 1")
    return parsed


def canonical_mode(mode):
    return str(mode).strip().lower().replace("-", "_").replace(" ", "_")


def resolve_lint_bin(cli_value):
    if cli_value:
        return Path(cli_value).expanduser()

    env_value = os.environ.get("QCHI_LINT_BIN")
    if env_value:
        return Path(env_value).expanduser()

    for candidate in DEFAULT_LINT_CANDIDATES:
        if candidate.exists():
            return candidate

    # Default error path if no binary exists yet.
    return DEFAULT_LINT_CANDIDATES[0]


def resolve_run_artifacts_root(cli_value):
    if cli_value:
        return Path(cli_value).expanduser()

    env_value = os.environ.get("QCHI_RUN_ARTIFACTS_DIR")
    if env_value:
        return Path(env_value).expanduser()

    return DEFAULT_RUN_ARTIFACTS_ROOT


def resolve_learning_dir(cli_value):
    if cli_value:
        return Path(cli_value).expanduser()

    env_value = os.environ.get("QCHI_LEARNING_DIR")
    if env_value:
        return Path(env_value).expanduser()

    return DEFAULT_LEARNING_DIR


def infer_learning_track(mode):
    key = canonical_mode(mode)
    if any(token in key for token in ["write", "draft", "manuscript", "paper", "lyx"]):
        return "writing"
    if any(token in key for token in ["plot", "code", "coding", "benchmark", "sweep", "simulate"]):
        return "coding-plotting"
    return DEFAULT_LEARNING_TRACK


def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_text_file(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = str(content or "")
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")


def write_json_file(path, payload):
    write_text_file(path, json.dumps(payload, indent=2, sort_keys=True))


def append_jsonl_record(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def ensure_project_learning_layout(project_root):
    project_root = Path(project_root)
    for track in LEARNING_TRACKS:
        track_dir = project_root / track
        track_dir.mkdir(parents=True, exist_ok=True)

        for jsonl_name in ["runs.jsonl", "evals.jsonl", "regressions.jsonl"]:
            jsonl_path = track_dir / jsonl_name
            if not jsonl_path.exists():
                write_text_file(jsonl_path, "")

        heuristics_path = track_dir / "heuristics.yaml"
        if not heuristics_path.exists():
            write_text_file(heuristics_path, PROJECT_HEURISTICS_TEMPLATE)


def build_run_learning_record(
    *,
    run_id,
    mode,
    task_id,
    quality_gate_pass,
    status,
    host,
    task,
    accepted_attempt,
    max_retries,
    run_dir,
    reason=None,
    message=None,
    project_id="",
    learning_track="",
):
    return {
        "run_id": run_id,
        "ts": utc_now_iso(),
        "mode": mode,
        "task_id": task_id,
        "quality_gate_pass": bool(quality_gate_pass),
        "status": str(status),
        "host": host,
        "task": task,
        "accepted_attempt": accepted_attempt,
        "max_retries": max_retries,
        "run_dir": str(run_dir),
        "reason": str(reason or ""),
        "message": str(message or ""),
        "project_id": str(project_id or ""),
        "learning_track": str(learning_track or ""),
    }


def append_run_learning_records(global_runs_path, project_runs_path, record):
    written_paths = []
    errors = []
    for path in [global_runs_path, project_runs_path]:
        if not path:
            continue
        try:
            append_jsonl_record(path, record)
            written_paths.append(Path(path))
        except OSError as exc:
            errors.append(f"{path}: {exc}")

    return written_paths, errors


def required_roles_for_mode(mode):
    roles = ["planner", "derivation", "symbolic_verifier", "numeric_verifier", "referee", "integrator"]
    if canonical_mode(mode) == "paper_reproduction":
        roles.insert(1, "source_miner")
    return roles


def assert_required_roles_present(mode, role_pipeline):
    missing_core = [role for role in CORE_REQUIRED_ROLES if role not in role_pipeline]
    if missing_core:
        raise ValueError(f"missing mandatory roles: {', '.join(missing_core)}")

    if canonical_mode(mode) == "paper_reproduction" and "source_miner" not in role_pipeline:
        raise ValueError("paper_reproduction mode requires source_miner role")


def fatal_policy_failure(message, run_dir=None, on_failure=None):
    if run_dir:
        write_text_file(Path(run_dir) / "final" / "fatal_error.txt", message)
        write_json_file(
            Path(run_dir) / "final" / "summary.json",
            {
                "status": "failed",
                "reason": "policy_failure",
                "message": str(message),
                "finished_at": utc_now_iso(),
            },
        )
    if on_failure is not None:
        try:
            on_failure(
                status="failed",
                quality_gate_pass=False,
                reason="policy_failure",
                message=message,
                accepted_attempt_value=None,
            )
        except Exception as exc:
            print(f"[WARN] failed to persist learning record for policy failure: {exc}")
    print(f"\n[POLICY FAILURE] {message}")
    sys.exit(2)


def host_command(host_name, prompt):
    if host_name == "gemini":
        return ["gemini", "-p", prompt]
    if host_name == "codex":
        return ["codex", "--prompt", prompt]
    if host_name == "antigravity":
        return ["antigravity", "run", prompt]
    if host_name == "opencode":
        return ["opencode", "-c", prompt]
    raise ValueError(f"Unknown host: {host_name}")


def execute_host(host_name, prompt):
    """
    Executes the prompt using the specified local AI CLI.
    This avoids API keys by using the host's existing auth state.
    """
    cmd = host_command(host_name, prompt)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError as exc:
        hint = HOST_INSTALL_HINTS.get(host_name, "Install the host CLI and verify it is in PATH.")
        raise HostExecutionError(
            f"The host CLI '{host_name}' is not installed or not in PATH. Hint: {hint}"
        ) from exc
    except subprocess.CalledProcessError as e:
        stderr = (e.stderr or "").strip()
        stdout = (e.stdout or "").strip()
        details = stderr or stdout or f"exit code {e.returncode}"
        raise HostExecutionError(f"The host '{host_name}' returned an error: {details}") from e


def run_markdown_agent(host, role_name, instructions, task_context):
    print(f"[*] Spawning [{role_name.upper()}] Agent via {host}...")

    prompt = dedent(
        f"""
        You are the {role_name.upper()} agent within the strict QCHI Research Operating Layer.

        CRITICAL MANDATE:
        {instructions}

        TASK CONTEXT:
        {task_context}

        Output only the requested markdown artifact.
        """
    ).strip()

    try:
        return execute_host(host, prompt)
    except HostExecutionError as exc:
        raise RuntimeError(f"{role_name} execution failed: {exc}") from exc


def normalize_decision(value):
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def parse_json_payload(raw_output):
    cleaned = raw_output.strip()
    if not cleaned:
        return None, "empty output"

    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 2 and lines[-1].strip() == "```":
            cleaned = "\n".join(lines[1:-1]).strip()

    try:
        return json.loads(cleaned), None
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None, "no JSON object found"
        candidate = cleaned[start : end + 1]
        try:
            return json.loads(candidate), None
        except json.JSONDecodeError as exc:
            return None, f"invalid JSON payload: {exc}"


def validate_agent_message(payload, expected_from_role):
    if not isinstance(payload, dict):
        return None, "payload is not a JSON object"

    required_fields = [
        "task_id",
        "subtask_id",
        "from_role",
        "to_role",
        "assumptions",
        "required_outputs",
        "result_summary",
        "verification_status",
        "confidence",
        "provenance_tags",
        "blockers",
        "role_decision",
        "required_fixes",
    ]
    missing = [field for field in required_fields if field not in payload]
    if missing:
        return None, f"missing required fields: {', '.join(missing)}"

    if payload["from_role"] != expected_from_role:
        return None, f"from_role mismatch: expected {expected_from_role}, got {payload['from_role']}"

    for list_field in ["assumptions", "required_outputs", "provenance_tags", "blockers", "required_fixes"]:
        if not isinstance(payload[list_field], list):
            return None, f"field '{list_field}' must be a list"

    if not isinstance(payload["verification_status"], dict):
        return None, "verification_status must be an object"

    for status_key in ["symbolic", "numeric", "referee"]:
        status_value = normalize_decision(payload["verification_status"].get(status_key, "unknown"))
        if status_value not in VALID_DECISIONS:
            return None, f"invalid verification_status.{status_key}: {status_value}"
        payload["verification_status"][status_key] = status_value

    role_decision = normalize_decision(payload.get("role_decision", "unknown"))
    if role_decision not in VALID_DECISIONS:
        return None, f"invalid role_decision: {role_decision}"
    payload["role_decision"] = role_decision

    result_summary = str(payload["result_summary"]).strip()
    if not result_summary:
        return None, "result_summary must be non-empty"
    payload["result_summary"] = result_summary

    payload["confidence"] = str(payload["confidence"]).strip().lower() or "unknown"
    return payload, None


def compact(text, limit=500):
    t = str(text or "").strip()
    if len(t) <= limit:
        return t
    return t[:limit] + " ..."


def run_structured_agent(
    host,
    role_key,
    instructions,
    task_context,
    task_id,
    subtask_id,
    to_role,
    raw_output_hook=None,
):
    role_name = ROLE_DISPLAY_NAMES.get(role_key, role_key)
    print(f"[*] Spawning [{role_name.upper()}] Agent via {host}...")

    prompt = dedent(
        f"""
        You are the {role_name.upper()} agent within the strict QCHI Research Operating Layer.

        CRITICAL MANDATE:
        {instructions}

        TASK CONTEXT:
        {task_context}

        OUTPUT REQUIREMENT:
        Return ONLY valid JSON (no markdown, no prose around JSON) with this exact schema:
        {{
          "task_id": "{task_id}",
          "subtask_id": "{subtask_id}",
          "from_role": "{role_key}",
          "to_role": "{to_role}",
          "assumptions": ["..."],
          "required_outputs": ["..."],
          "result_summary": "...",
          "verification_status": {{
            "symbolic": "pass|fail|deferred|not_applicable|unknown",
            "numeric": "pass|fail|deferred|not_applicable|unknown",
            "referee": "pass|fail|deferred|not_applicable|unknown"
          }},
          "confidence": "low|medium|high|unknown",
          "provenance_tags": ["REPRODUCED_FROM_SOURCE|INFERRED_ASSUMPTION|NEW_EXTENSION"],
          "blockers": ["..."],
          "role_decision": "pass|fail|deferred|not_applicable|unknown",
          "required_fixes": ["..."]
        }}

        Strictly set from_role to "{role_key}".
        """
    ).strip()

    try:
        raw = execute_host(host, prompt)
    except HostExecutionError as exc:
        return None, f"{role_key} execution failed: {exc}"
    if raw_output_hook is not None:
        raw_output_hook(raw)
    payload, parse_error = parse_json_payload(raw)
    if parse_error:
        return None, f"{role_key} produced invalid JSON: {parse_error}. Output preview: {compact(raw)}"

    payload, validation_error = validate_agent_message(payload, role_key)
    if validation_error:
        return None, f"{role_key} JSON validation failed: {validation_error}. Output preview: {compact(raw)}"

    return payload, None


def run_qchi_lint(content, lint_bin):
    """
    The Enforcer: Runs the Rust qchi-lint tool.
    If this fails, the CLI will reject the LLM's output.
    """
    print("[-] Running QCHI Rigor Engine (qchi-lint)...")

    if not lint_bin.exists():
        return (
            False,
            (
                f"qchi-lint binary not found at {lint_bin}. "
                "Build it first: cargo build --manifest-path tools/qchi-lint/Cargo.toml"
            ),
        )

    tmp_file = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".md", delete=False) as handle:
            handle.write(content)
            tmp_file = Path(handle.name)

        cmd = [str(lint_bin), "report", "--file", str(tmp_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout.strip() or "Pass"

        details = result.stderr.strip() or result.stdout.strip()
        if not details:
            details = f"qchi-lint exited with status {result.returncode}"
        return False, details
    except Exception as exc:
        return False, f"Failed to run qchi-lint: {exc}"
    finally:
        if tmp_file and tmp_file.exists():
            try:
                tmp_file.unlink()
            except OSError:
                pass


def build_deriver_instructions(last_feedback=None):
    instructions = (
        "Execute the provided plan and produce a complete derivation artifact. "
        "Output markdown only with these exact section headers: "
        "## Problem framing, ## Assumptions and regime, ## Governing equations, ## Derivation, "
        "## Validation checks, ## Final result, ## Interpretation and confidence, "
        "## Claim provenance, ## References. "
        "Inside ## Validation checks, include explicit PASS/FAIL/DEFERRED status lines for: "
        "Unit check, Limiting-case check, Asymptotic check, Consistency check, Symbolic verification. "
        "Symbolic verification must name the tool (Mathematica or SymPy) and include a fenced code block "
        "with the symbolic verification log snippet and outcome. "
        "Include claim provenance tags such as REPRODUCED_FROM_SOURCE / INFERRED_ASSUMPTION / NEW_EXTENSION."
    )

    if last_feedback:
        instructions += (
            "\n\nYOUR LAST ATTEMPT FAILED POLICY GATES:\n"
            f"{last_feedback}\n"
            "Fix every failing item and regenerate a fully compliant artifact."
        )

    return instructions


def evaluate_role_gates(symbolic_msg, numeric_msg, referee_msg, integrator_msg):
    issues = []

    sym_decision = symbolic_msg["role_decision"]
    if sym_decision == "pass":
        pass
    elif sym_decision == "deferred" and symbolic_msg["blockers"]:
        # Explicit justified defer is acceptable for symbolic checks.
        pass
    else:
        issues.append(
            "symbolic_verifier must be PASS or justified DEFERRED with blockers; "
            f"got '{sym_decision}'"
        )

    num_decision = numeric_msg["role_decision"]
    if num_decision not in {"pass", "not_applicable"}:
        issues.append(f"numeric_verifier must be PASS or NOT_APPLICABLE; got '{num_decision}'")

    referee_decision = referee_msg["role_decision"]
    if referee_decision != "pass":
        issues.append(f"referee must be PASS with no unresolved critical issues; got '{referee_decision}'")

    integrator_decision = integrator_msg["role_decision"]
    if integrator_decision != "pass":
        issues.append(f"integrator blocked promotion with decision '{integrator_decision}'")

    return issues


def build_retry_feedback(gate_issues, *role_messages):
    lines = [f"- {issue}" for issue in gate_issues]

    fixes = []
    for msg in role_messages:
        for item in msg.get("required_fixes", []):
            text = str(item).strip()
            if text and text not in fixes:
                fixes.append(text)

    blockers = []
    for msg in role_messages:
        for item in msg.get("blockers", []):
            text = str(item).strip()
            if text and text not in blockers:
                blockers.append(text)

    if fixes:
        lines.append("- Required fixes from subagents:")
        for item in fixes:
            lines.append(f"  - {item}")

    if blockers:
        lines.append("- Blockers reported by subagents:")
        for item in blockers:
            lines.append(f"  - {item}")

    return "\n".join(lines)


def orchestrate(args):
    lint_bin = resolve_lint_bin(args.lint_bin)
    mode_key = canonical_mode(args.mode)
    role_pipeline = required_roles_for_mode(mode_key)
    task_id = f"qchi-{int(time.time())}"
    run_id = f"run-{task_id}"
    run_artifacts_root = resolve_run_artifacts_root(args.run_artifacts_dir)
    learning_dir = resolve_learning_dir(args.learning_dir)
    learning_track = args.learning_track or infer_learning_track(mode_key)
    global_runs_path = learning_dir / "runs.jsonl"
    project_runs_path = None
    if args.project_id:
        project_root = learning_dir / "projects" / args.project_id
        ensure_project_learning_layout(project_root)
        project_runs_path = project_root / learning_track / "runs.jsonl"

    run_dir = run_artifacts_root / task_id
    roles_dir = run_dir / "roles"
    attempts_dir = run_dir / "attempts"
    final_dir = run_dir / "final"
    for path in [roles_dir, attempts_dir, final_dir]:
        path.mkdir(parents=True, exist_ok=True)

    started_at = utc_now_iso()
    learning_record_written = False

    def persist_run_record(status, quality_gate_pass, reason="", message="", accepted_attempt_value=None):
        nonlocal learning_record_written
        if learning_record_written:
            return
        record = build_run_learning_record(
            run_id=run_id,
            mode=args.mode,
            task_id=task_id,
            quality_gate_pass=quality_gate_pass,
            status=status,
            host=args.host,
            task=args.task,
            accepted_attempt=accepted_attempt_value,
            max_retries=args.max_retries,
            run_dir=run_dir,
            reason=reason,
            message=message,
            project_id=args.project_id or "",
            learning_track=learning_track,
        )
        written_paths, errors = append_run_learning_records(global_runs_path, project_runs_path, record)
        if written_paths:
            joined = ", ".join(str(p) for p in written_paths)
            print(f"[*] Learning run record appended: {joined}")
            learning_record_written = True
        if errors:
            for item in errors:
                print(f"[WARN] Failed to append learning run record: {item}")

    write_json_file(
        run_dir / "run_context.json",
        {
            "run_id": run_id,
            "task_id": task_id,
            "started_at": started_at,
            "host": args.host,
            "mode": args.mode,
            "task": args.task,
            "max_retries": args.max_retries,
            "role_pipeline": role_pipeline,
            "lint_bin": str(lint_bin),
            "run_artifacts_root": str(run_artifacts_root),
            "run_dir": str(run_dir),
            "learning_dir": str(learning_dir),
            "learning_track": learning_track,
            "global_runs_file": str(global_runs_path),
            "project_runs_file": str(project_runs_path) if project_runs_path else "",
        },
    )

    try:
        assert_required_roles_present(mode_key, role_pipeline)
    except ValueError as exc:
        fatal_policy_failure(str(exc), run_dir=run_dir, on_failure=persist_run_record)

    def abort_run(message, reason):
        write_text_file(final_dir / "fatal_error.txt", message)
        write_json_file(
            final_dir / "summary.json",
            {
                "status": "failed",
                "reason": reason,
                "message": str(message),
                "task_id": task_id,
                "host": args.host,
                "mode": args.mode,
                "finished_at": utc_now_iso(),
            },
        )
        persist_run_record(
            status="failed",
            quality_gate_pass=False,
            reason=reason,
            message=message,
            accepted_attempt_value=accepted_attempt,
        )
        print(f"\n[FATAL ERROR] {message}")
        sys.exit(1)

    print("=========================================")
    print("    QCHI: Research Operating Layer       ")
    print("=========================================")
    print(f"Host: {args.host} | Mode: {args.mode}")
    print(f"Task: {args.task}")
    print(f"Linter: {lint_bin}")
    print(f"Role pipeline: {', '.join(role_pipeline)}")
    print(f"Run artifacts: {run_dir}\n")
    print(f"Learning runs file: {global_runs_path}")
    if project_runs_path:
        print(f"Project runs file: {project_runs_path}\n")

    planner_instructions = (
        "Decompose the task into minimal verifiable subtasks. "
        "Define assumptions, required outputs, and explicit acceptance checks."
    )
    planner_raw_path = roles_dir / "planner.raw.txt"
    planner_msg, planner_error = run_structured_agent(
        args.host,
        "planner",
        planner_instructions,
        args.task,
        task_id,
        "planner-main",
        "derivation",
        raw_output_hook=lambda raw, path=planner_raw_path: write_text_file(path, raw),
    )
    if planner_error:
        fatal_policy_failure(planner_error, run_dir=run_dir, on_failure=persist_run_record)
    write_json_file(roles_dir / "planner.json", planner_msg)

    source_msg = None
    if "source_miner" in role_pipeline:
        source_instructions = (
            "Build an arXiv-first source strategy for this reproduction task. "
            "List concrete source targets, scope coverage, and blockers."
        )
        source_raw_path = roles_dir / "source_miner.raw.txt"
        source_msg, source_error = run_structured_agent(
            args.host,
            "source_miner",
            source_instructions,
            f"User task:\n{args.task}\n\nPlanner summary:\n{planner_msg['result_summary']}",
            task_id,
            "source-plan",
            "derivation",
            raw_output_hook=lambda raw, path=source_raw_path: write_text_file(path, raw),
        )
        if source_error:
            fatal_policy_failure(source_error, run_dir=run_dir, on_failure=persist_run_record)
        write_json_file(roles_dir / "source_miner.json", source_msg)

    derivation = ""
    last_feedback = None
    accepted_attempt = None

    for attempt in range(1, args.max_retries + 1):
        print(f"\n=== Attempt {attempt}/{args.max_retries} ===")
        attempt_dir = attempts_dir / f"attempt-{attempt:03d}"
        attempt_dir.mkdir(parents=True, exist_ok=True)
        write_json_file(
            attempt_dir / "meta.json",
            {
                "attempt": attempt,
                "max_retries": args.max_retries,
                "started_at": utc_now_iso(),
                "last_feedback": last_feedback or "",
            },
        )

        derivation_context_parts = [
            f"User task:\n{args.task}",
            f"Planner summary:\n{planner_msg['result_summary']}",
            "Planner required outputs:\n" + "\n".join(planner_msg["required_outputs"] or ["(none provided)"]),
        ]
        if source_msg:
            derivation_context_parts.append(f"Source miner summary:\n{source_msg['result_summary']}")
        if last_feedback:
            derivation_context_parts.append(f"Prior gate failures to fix:\n{last_feedback}")

        deriver_instructions = build_deriver_instructions(last_feedback)
        write_text_file(attempt_dir / "derivation_context.txt", "\n\n".join(derivation_context_parts))
        write_text_file(attempt_dir / "derivation_instructions.txt", deriver_instructions)
        try:
            derivation = run_markdown_agent(
                args.host,
                f"Derivation (Attempt {attempt})",
                deriver_instructions,
                "\n\n".join(derivation_context_parts),
            )
        except RuntimeError as exc:
            abort_run(str(exc), "derivation_execution_failed")
        write_text_file(attempt_dir / "derivation.md", derivation)

        if not derivation.strip():
            print("\n[!] Quality Gate Failed: Derivation agent returned empty output")
            write_json_file(
                attempt_dir / "gate_issues.json",
                {
                    "passed": False,
                    "issues": ["derivation output was empty"],
                },
            )
            if attempt < args.max_retries:
                last_feedback = "- Derivation output was empty. Return the full required markdown artifact."
                write_text_file(attempt_dir / "retry_feedback.txt", last_feedback)
                time.sleep(2)
                continue
            abort_run("Empty derivation after maximum retries.", "empty_derivation")

        lint_pass, lint_msg = run_qchi_lint(derivation, lint_bin)
        write_json_file(
            attempt_dir / "lint.json",
            {
                "passed": lint_pass,
                "message": lint_msg,
            },
        )

        symbolic_raw_path = attempt_dir / "symbolic_verifier.raw.txt"
        symbolic_msg, symbolic_error = run_structured_agent(
            args.host,
            "symbolic_verifier",
            "Validate symbolic transformations and identities. Report exact pass/fail/deferred decision and required fixes.",
            f"Mode: {args.mode}\n\nDerivation artifact:\n{derivation}\n\nqchi-lint result: {lint_msg}",
            task_id,
            f"symbolic-attempt-{attempt}",
            "integrator",
            raw_output_hook=lambda raw, path=symbolic_raw_path: write_text_file(path, raw),
        )
        if symbolic_error:
            fatal_policy_failure(symbolic_error, run_dir=run_dir, on_failure=persist_run_record)
        write_json_file(attempt_dir / "symbolic_verifier.json", symbolic_msg)

        numeric_raw_path = attempt_dir / "numeric_verifier.raw.txt"
        numeric_msg, numeric_error = run_structured_agent(
            args.host,
            "numeric_verifier",
            "Validate numeric consistency when applicable. If not applicable, set role_decision to not_applicable and explain why.",
            f"Mode: {args.mode}\n\nDerivation artifact:\n{derivation}",
            task_id,
            f"numeric-attempt-{attempt}",
            "integrator",
            raw_output_hook=lambda raw, path=numeric_raw_path: write_text_file(path, raw),
        )
        if numeric_error:
            fatal_policy_failure(numeric_error, run_dir=run_dir, on_failure=persist_run_record)
        write_json_file(attempt_dir / "numeric_verifier.json", numeric_msg)

        referee_raw_path = attempt_dir / "referee.raw.txt"
        referee_msg, referee_error = run_structured_agent(
            args.host,
            "referee",
            "Attempt to falsify the result via hidden assumptions, boundary violations, and internal contradictions.",
            f"Mode: {args.mode}\n\nDerivation artifact:\n{derivation}",
            task_id,
            f"referee-attempt-{attempt}",
            "integrator",
            raw_output_hook=lambda raw, path=referee_raw_path: write_text_file(path, raw),
        )
        if referee_error:
            fatal_policy_failure(referee_error, run_dir=run_dir, on_failure=persist_run_record)
        write_json_file(attempt_dir / "referee.json", referee_msg)

        integrator_context = {
            "mode": args.mode,
            "lint_pass": lint_pass,
            "lint_message": lint_msg,
            "symbolic_verifier": symbolic_msg,
            "numeric_verifier": numeric_msg,
            "referee": referee_msg,
            "derivation_excerpt": compact(derivation, limit=3000),
        }
        write_json_file(attempt_dir / "integrator_context.json", integrator_context)
        integrator_raw_path = attempt_dir / "integrator.raw.txt"
        integrator_msg, integrator_error = run_structured_agent(
            args.host,
            "integrator",
            (
                "Apply QCHI gate policy. Promote only if derivation is complete, symbolic gate passes "
                "(or justified defer), numeric gate passes when applicable, referee has no unresolved critical issue, "
                "and quality gate is satisfied."
            ),
            json.dumps(integrator_context, indent=2),
            task_id,
            f"integrator-attempt-{attempt}",
            "final",
            raw_output_hook=lambda raw, path=integrator_raw_path: write_text_file(path, raw),
        )
        if integrator_error:
            fatal_policy_failure(integrator_error, run_dir=run_dir, on_failure=persist_run_record)
        write_json_file(attempt_dir / "integrator.json", integrator_msg)

        gate_issues = []
        if not lint_pass:
            gate_issues.append(f"qchi-lint failed: {lint_msg}")

        gate_issues.extend(evaluate_role_gates(symbolic_msg, numeric_msg, referee_msg, integrator_msg))
        write_json_file(
            attempt_dir / "gate_issues.json",
            {
                "passed": not gate_issues,
                "issues": gate_issues,
            },
        )

        if not gate_issues:
            print("\n[+] Quality Gate Passed with mandatory subagent evidence. Derivation accepted.")
            accepted_attempt = attempt
            break

        print("\n[!] Quality Gate Failed:")
        for issue in gate_issues:
            print(f"    - {issue}")

        if attempt < args.max_retries:
            print("[*] Forcing AI to retry and fix errors...")
            last_feedback = build_retry_feedback(
                gate_issues,
                symbolic_msg,
                numeric_msg,
                referee_msg,
                integrator_msg,
            )
            write_text_file(attempt_dir / "retry_feedback.txt", last_feedback)
            time.sleep(2)
        else:
            abort_run(
                "Agent failed to produce compliant output after maximum retries.",
                "max_retries_exceeded",
            )

    output_path = None
    if args.output_file:
        output_path = Path(args.output_file).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(derivation, encoding="utf-8")
        print(f"[*] Saved accepted derivation to {output_path}")

    write_text_file(final_dir / "derivation.md", derivation)
    write_json_file(
        final_dir / "summary.json",
        {
            "status": "success",
            "run_id": run_id,
            "task_id": task_id,
            "host": args.host,
            "mode": args.mode,
            "task": args.task,
            "role_pipeline": role_pipeline,
            "max_retries": args.max_retries,
            "accepted_attempt": accepted_attempt,
            "lint_bin": str(lint_bin),
            "run_dir": str(run_dir),
            "output_file": str(output_path) if output_path else "",
            "started_at": started_at,
            "finished_at": utc_now_iso(),
            "learning_runs_file": str(global_runs_path),
            "project_runs_file": str(project_runs_path) if project_runs_path else "",
        },
    )
    persist_run_record(
        status="completed",
        quality_gate_pass=True,
        accepted_attempt_value=accepted_attempt,
    )

    print("\n[FINAL DERIVATION OUTPUT]\n" + derivation)
    print("=========================================")
    print(f"[*] Run artifacts saved to {run_dir}")
    print("[*] QCHI Orchestration Complete.")


def command_run(args):
    orchestrate(args)
    return 0


def call_process(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    out = (result.stdout or "").strip()
    err = (result.stderr or "").strip()
    return result.returncode, out, err


def print_check(status, label, detail):
    print(f"[{status}] {label}: {detail}")


def command_doctor(args):
    lint_bin = resolve_lint_bin(args.lint_bin)
    failures = 0
    warnings = 0

    print("QCHI doctor")
    print(f"- repo: {REPO_ROOT}")
    print(f"- selected host: {args.host}")
    print(f"- lint binary path: {lint_bin}")

    selected_host_binary = HOST_BINARIES[args.host]
    if shutil.which(selected_host_binary):
        print_check("PASS", f"host ({args.host})", f"found '{selected_host_binary}' in PATH")
    else:
        print_check("FAIL", f"host ({args.host})", HOST_INSTALL_HINTS[args.host])
        failures += 1

    if args.check_all_hosts:
        for host in SUPPORTED_HOSTS:
            if host == args.host:
                continue
            binary = HOST_BINARIES[host]
            if shutil.which(binary):
                print_check("PASS", f"host ({host})", f"found '{binary}' in PATH")
            else:
                print_check("WARN", f"host ({host})", "not installed in PATH")
                warnings += 1

    if lint_bin.exists():
        if os.access(lint_bin, os.X_OK):
            print_check("PASS", "qchi-lint binary", "exists and executable")

            template_file = REPO_ROOT / "templates" / "OUTPUT_TEMPLATE.md"
            rc, out, err = call_process([str(lint_bin), "report", "--file", str(template_file)])
            if rc == 0:
                print_check("PASS", "qchi-lint report check", out or "report lint passed")
            else:
                detail = err or out or f"exit code {rc}"
                print_check("FAIL", "qchi-lint report check", detail)
                failures += 1
        else:
            print_check("FAIL", "qchi-lint binary", "exists but is not executable")
            failures += 1
    else:
        print_check(
            "FAIL",
            "qchi-lint binary",
            (
                f"not found at {lint_bin}. Build with: "
                "cargo build --manifest-path tools/qchi-lint/Cargo.toml"
            ),
        )
        failures += 1

    if shutil.which("cargo"):
        print_check("PASS", "cargo", "found in PATH")
    else:
        print_check("WARN", "cargo", "not found in PATH")
        warnings += 1

    if shutil.which("rustc"):
        print_check("PASS", "rustc", "found in PATH")
    else:
        print_check("WARN", "rustc", "not found in PATH")
        warnings += 1

    print(f"\nDoctor summary: failures={failures}, warnings={warnings}")
    return 1 if failures else 0


def run_lint_command(lint_bin, lint_args):
    if not lint_bin.exists():
        print(
            f"[FATAL ERROR] qchi-lint binary not found at {lint_bin}. "
            "Build it first: cargo build --manifest-path tools/qchi-lint/Cargo.toml"
        )
        return 1

    if not os.access(lint_bin, os.X_OK):
        print(f"[FATAL ERROR] qchi-lint binary is not executable: {lint_bin}")
        return 1

    cmd = [str(lint_bin)] + lint_args
    rc, out, err = call_process(cmd)
    if out:
        print(out)
    if err:
        print(err)
    return rc


def command_lint(args):
    lint_bin = resolve_lint_bin(args.lint_bin)
    if args.lint_command == "report":
        return run_lint_command(lint_bin, ["report", "--file", args.file])
    if args.lint_command == "jsonl":
        return run_lint_command(lint_bin, ["jsonl", "--kind", args.kind, "--file", args.file])
    print("[FATAL ERROR] unsupported lint command")
    return 1


def build_learning_dashboard():
    build_script = REPO_ROOT / "tools" / "build_learning_dashboard.py"
    if not build_script.exists():
        print(f"[FATAL ERROR] dashboard builder script missing: {build_script}")
        return 1
    rc, out, err = call_process([sys.executable, str(build_script)])
    if out:
        print(out)
    if err:
        print(err)
    return rc


def command_dashboard(args):
    if args.dashboard_command == "build":
        return build_learning_dashboard()

    if args.dashboard_command == "serve":
        if not args.skip_build:
            rc = build_learning_dashboard()
            if rc != 0:
                return rc

        url_host = args.bind
        if url_host in {"0.0.0.0", "::"}:
            url_host = "127.0.0.1"
        print(f"Serving dashboard at http://{url_host}:{args.port}/dashboard/")
        cmd = [sys.executable, "-m", "http.server", str(args.port), "--bind", args.bind]
        try:
            return subprocess.run(cmd, cwd=str(REPO_ROOT)).returncode
        except KeyboardInterrupt:
            print("\nDashboard server stopped.")
            return 0

    print("[FATAL ERROR] unsupported dashboard command")
    return 1


def git_short_commit():
    rc, out, _ = call_process(["git", "-C", str(REPO_ROOT), "rev-parse", "--short", "HEAD"])
    if rc == 0 and out:
        return out
    return "unknown"


def command_version(_args):
    print(f"qchi-cli {QCHI_CLI_VERSION}")
    print(f"repo: {REPO_ROOT}")
    print(f"git: {git_short_commit()}")
    print(f"python: {sys.version.split()[0]}")
    return 0


def add_run_args(parser):
    parser.add_argument(
        "--host",
        choices=SUPPORTED_HOSTS,
        default="gemini",
        help="Underlying AI CLI to drive (default: gemini)",
    )
    parser.add_argument("--mode", required=True, help="QCHI execution mode")
    parser.add_argument("--task", required=True, help="The physics task or ArXiv ID")
    parser.add_argument(
        "--max-retries",
        type=positive_int,
        default=3,
        help="Maximum derivation retries after quality-gate failure (default: 3)",
    )
    parser.add_argument("--output-file", help="Optional file path for writing the accepted derivation")
    parser.add_argument(
        "--lint-bin",
        help="Optional path to qchi-lint binary; defaults to env QCHI_LINT_BIN or local target path",
    )
    parser.add_argument(
        "--run-artifacts-dir",
        help="Optional run-artifact root; defaults to env QCHI_RUN_ARTIFACTS_DIR or .qchi/runs",
    )
    parser.add_argument(
        "--learning-dir",
        help="Optional learning root; defaults to env QCHI_LEARNING_DIR or skills/qchi/learning",
    )
    parser.add_argument(
        "--project-id",
        help="Optional project id for project-scoped learning logging (creates project layout if missing)",
    )
    parser.add_argument(
        "--learning-track",
        choices=LEARNING_TRACKS,
        help=(
            "Optional project track for project-scoped learning logging; "
            "defaults to inferred track by mode"
        ),
    )


def build_parser():
    parser = argparse.ArgumentParser(description="QCHI CLI Orchestrator")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run QCHI multi-agent orchestration")
    add_run_args(run_parser)
    run_parser.set_defaults(handler=command_run)

    doctor_parser = subparsers.add_parser("doctor", help="Check local environment for QCHI")
    doctor_parser.add_argument(
        "--host",
        choices=SUPPORTED_HOSTS,
        default="gemini",
        help="Primary host CLI to validate (default: gemini)",
    )
    doctor_parser.add_argument(
        "--check-all-hosts",
        action="store_true",
        help="Also check availability of all supported host CLIs",
    )
    doctor_parser.add_argument(
        "--lint-bin",
        help="Optional path to qchi-lint binary; defaults to env QCHI_LINT_BIN or local target path",
    )
    doctor_parser.set_defaults(handler=command_doctor)

    lint_parser = subparsers.add_parser("lint", help="Run qchi-lint directly")
    lint_parser.add_argument(
        "--lint-bin",
        help="Optional path to qchi-lint binary; defaults to env QCHI_LINT_BIN or local target path",
    )
    lint_subparsers = lint_parser.add_subparsers(dest="lint_command", required=True)

    lint_report = lint_subparsers.add_parser("report", help="Lint a markdown report")
    lint_report.add_argument("--file", required=True, help="Path to markdown report file")
    lint_report.set_defaults(handler=command_lint)

    lint_jsonl = lint_subparsers.add_parser("jsonl", help="Lint a learning JSONL file")
    lint_jsonl.add_argument("--kind", required=True, choices=["runs", "evals", "regressions"])
    lint_jsonl.add_argument("--file", required=True, help="Path to JSONL file")
    lint_jsonl.set_defaults(handler=command_lint)

    version_parser = subparsers.add_parser("version", help="Print QCHI CLI version")
    version_parser.set_defaults(handler=command_version)

    dashboard_parser = subparsers.add_parser("dashboard", help="Build or serve the learning dashboard UI")
    dashboard_subparsers = dashboard_parser.add_subparsers(dest="dashboard_command", required=True)

    dashboard_build = dashboard_subparsers.add_parser(
        "build",
        help="Generate dashboard/learning_data.json from learning store files",
    )
    dashboard_build.set_defaults(handler=command_dashboard)

    dashboard_serve = dashboard_subparsers.add_parser(
        "serve",
        help="Build and serve dashboard at /dashboard/",
    )
    dashboard_serve.add_argument(
        "--port",
        type=positive_int,
        default=DEFAULT_DASHBOARD_PORT,
        help=f"HTTP port for the dashboard server (default: {DEFAULT_DASHBOARD_PORT})",
    )
    dashboard_serve.add_argument(
        "--bind",
        default=DEFAULT_DASHBOARD_BIND,
        help=f"Bind address for HTTP server (default: {DEFAULT_DASHBOARD_BIND})",
    )
    dashboard_serve.add_argument(
        "--skip-build",
        action="store_true",
        help="Serve existing dashboard data without rebuilding learning_data.json",
    )
    dashboard_serve.set_defaults(handler=command_dashboard)

    return parser


def normalize_argv(argv):
    # Backward compatibility: `qchi --mode ... --task ...` maps to `qchi run ...`.
    if not argv:
        return argv

    known = {"run", "doctor", "lint", "version", "dashboard", "-h", "--help"}
    first = argv[0]
    if first in known:
        return argv
    if first.startswith("-"):
        return ["run"] + argv
    return argv


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    argv = normalize_argv(argv)

    if not argv:
        parser.print_help()
        return 1

    args = parser.parse_args(argv)
    if not hasattr(args, "handler"):
        parser.print_help()
        return 1

    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
