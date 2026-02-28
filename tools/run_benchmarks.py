#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[1]
DEFAULT_SUITE = REPO_ROOT / "skills" / "qchi" / "learning" / "benchmarks" / "baseline_v1.json"
DEFAULT_OUT = REPO_ROOT / "skills" / "qchi" / "learning" / "benchmarks" / "last_run_summary.json"
DEFAULT_LEARNING_DIR = REPO_ROOT / "skills" / "qchi" / "learning"
DEFAULT_EVALS_FILE = DEFAULT_LEARNING_DIR / "evals.jsonl"
DEFAULT_REGRESSIONS_FILE = DEFAULT_LEARNING_DIR / "regressions.jsonl"
DEFAULT_QCHI_BIN = REPO_ROOT / "bin" / "qchi"
DEFAULT_SWEEP_RUNS_ROOT = REPO_ROOT / ".qchi" / "sweeps"
REQUIRED_CASE_FIELDS = ("case_id", "domain", "mode", "target", "required_checks")
TRACK_CHOICES = ("physics", "writing", "coding-plotting")


def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def positive_int(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer value: {value}") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be >= 1")
    return parsed


def bounded_score(value):
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid float value: {value}") from exc
    if parsed < 0.0 or parsed > 1.0:
        raise argparse.ArgumentTypeError("must be in range [0, 1]")
    return parsed


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def append_jsonl(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def call_process(cmd, cwd=None):
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )


def short_text(text, limit=240):
    text = str(text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def git_commit_ref(ref):
    result = call_process(["git", "-C", str(REPO_ROOT), "rev-parse", "--short", ref])
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return "unknown"


def normalize_suite_cases(cases, errors):
    normalized = []
    seen = set()
    for idx, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            errors.append(f"case#{idx} must be a JSON object")
            continue

        missing = [field for field in REQUIRED_CASE_FIELDS if field not in case]
        if missing:
            errors.append(f"case#{idx} missing fields: {', '.join(missing)}")
            continue

        case_id = str(case.get("case_id", "")).strip()
        if not case_id:
            errors.append(f"case#{idx} has empty case_id")
            continue
        if case_id in seen:
            errors.append(f"duplicate case_id: {case_id}")
            continue
        seen.add(case_id)

        normalized.append(
            {
                "case_id": case_id,
                "domain": str(case.get("domain", "")).strip(),
                "mode": str(case.get("mode", "")).strip(),
                "target": str(case.get("target", "")).strip(),
                "required_checks": case.get("required_checks", []),
            }
        )
    return normalized


def load_suite(path):
    errors = []
    suite_path = Path(path)
    data = read_json(suite_path)
    cases = data.get("cases", [])
    if not isinstance(cases, list):
        errors.append("suite.cases must be a list")
        cases = []
    normalized_cases = normalize_suite_cases(cases, errors)
    return data, normalized_cases, errors


def parse_results_payload(path):
    payload = read_json(path)
    if isinstance(payload, dict) and "cases" in payload:
        rows = payload["cases"]
    elif isinstance(payload, dict):
        rows = []
        for key, value in payload.items():
            row = dict(value or {})
            row["case_id"] = key
            rows.append(row)
    elif isinstance(payload, list):
        rows = payload
    else:
        raise ValueError("results payload must be a list, an object, or an object with 'cases'")

    if not isinstance(rows, list):
        raise ValueError("results.cases must be a list")
    return rows


def normalize_results(rows):
    out = {}
    errors = []
    for idx, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"results row#{idx} must be a JSON object")
            continue

        case_id = str(row.get("case_id", "")).strip()
        if not case_id:
            errors.append(f"results row#{idx} missing case_id")
            continue
        if case_id in out:
            errors.append(f"duplicate results entry for case_id={case_id}")
            continue

        raw_pass = row.get("pass")
        if raw_pass is None:
            errors.append(f"results row#{idx} missing pass for case_id={case_id}")
            continue
        if not isinstance(raw_pass, bool):
            errors.append(f"results row#{idx} pass must be boolean for case_id={case_id}")
            continue

        raw_score = row.get("score")
        if raw_score is None:
            score = 1.0 if raw_pass else 0.0
        else:
            try:
                score = float(raw_score)
            except (TypeError, ValueError):
                errors.append(f"results row#{idx} score must be numeric for case_id={case_id}")
                continue
            if score < 0.0 or score > 1.0:
                errors.append(f"results row#{idx} score out of range [0,1] for case_id={case_id}")
                continue

        out[case_id] = {
            "pass": raw_pass,
            "score": score,
            "run_id": str(row.get("run_id", "")).strip(),
            "reason": str(row.get("reason", "")).strip(),
        }
    return out, errors


def infer_case_track(case):
    domain = str(case.get("domain", "")).strip().lower()
    if domain in TRACK_CHOICES:
        return domain
    mode = str(case.get("mode", "")).strip().lower()
    if "write" in mode or "paper" in mode:
        return "writing"
    if any(token in mode for token in ("plot", "code", "coding", "benchmark", "sweep", "simulate")):
        return "coding-plotting"
    return "physics"


def find_new_run_dir(run_root, before_names):
    if not run_root.exists():
        return None
    candidates = [item for item in run_root.iterdir() if item.is_dir() and item.name not in before_names]
    if not candidates:
        return None
    return max(candidates, key=lambda item: item.stat().st_mtime)


def read_run_summary(run_dir):
    if not run_dir:
        return {}
    summary_path = Path(run_dir) / "final" / "summary.json"
    if not summary_path.exists():
        return {}
    try:
        return read_json(summary_path)
    except Exception:
        return {}


def execute_suite_case(case, args, sweep_id, run_root):
    before_names = set()
    if run_root.exists():
        before_names = {item.name for item in run_root.iterdir() if item.is_dir()}
    else:
        run_root.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        str(Path(args.qchi_bin).expanduser()),
        "run",
        "--host",
        args.host,
        "--mode",
        case["mode"],
        "--task",
        case["target"],
        "--max-retries",
        str(args.max_retries),
        "--run-artifacts-dir",
        str(run_root),
        "--learning-dir",
        str(args.learning_dir),
    ]
    if args.lint_bin:
        cmd.extend(["--lint-bin", args.lint_bin])
    if args.project_id:
        cmd.extend(["--project-id", args.project_id])
    if args.learning_track:
        cmd.extend(["--learning-track", args.learning_track])

    result = call_process(cmd, cwd=REPO_ROOT)
    run_dir = find_new_run_dir(run_root, before_names)
    run_summary = read_run_summary(run_dir)

    status = str(run_summary.get("status", "")).strip().lower()
    passed = result.returncode == 0 and status == "success"
    run_id = str(run_summary.get("run_id", "")).strip()
    if not run_id:
        run_id = f"run-{sweep_id}-{case['case_id']}"

    reason_parts = []
    if not passed:
        if run_summary.get("reason"):
            reason_parts.append(str(run_summary.get("reason")))
        if run_summary.get("message"):
            reason_parts.append(str(run_summary.get("message")))
        if result.returncode != 0 and not reason_parts:
            reason_parts.append(f"qchi run exited with status {result.returncode}")
        if not reason_parts:
            reason_parts.append(short_text(result.stderr or result.stdout))

    return {
        "case_id": case["case_id"],
        "mode": case["mode"],
        "target": case["target"],
        "track": args.learning_track or infer_case_track(case),
        "pass": passed,
        "score": 1.0 if passed else 0.0,
        "run_id": run_id,
        "reason": " | ".join(part for part in reason_parts if part).strip(),
        "run_dir": str(run_dir) if run_dir else "",
        "returncode": result.returncode,
    }


def build_eval_record(sweep_id, suite_name, case_outcome, idx):
    return {
        "eval_id": f"eval-{sweep_id}-{idx:03d}",
        "ts": utc_now_iso(),
        "run_id": case_outcome["run_id"],
        "suite": suite_name,
        "case_id": case_outcome["case_id"],
        "score": float(case_outcome["score"]),
        "pass": bool(case_outcome["pass"]),
        "regression": not bool(case_outcome["pass"]),
        "mode": case_outcome.get("mode", ""),
        "target": case_outcome.get("target", ""),
        "track": case_outcome.get("track", ""),
        "reason": case_outcome.get("reason", ""),
    }


def compute_metrics(case_outcomes, score_threshold):
    if not case_outcomes:
        return {
            "pass_count": 0,
            "fail_count": 0,
            "score_mean": None,
            "score_min": None,
            "score_max": None,
            "score_stddev": None,
            "score_spread": None,
            "cpis": None,
            "cpis_hits": 0,
        }

    scores = [float(item["score"]) for item in case_outcomes]
    pass_count = sum(1 for item in case_outcomes if item["pass"])
    fail_count = len(case_outcomes) - pass_count
    cpis_hits = sum(1 for item in case_outcomes if item["pass"] and float(item["score"]) >= score_threshold)
    cpis = cpis_hits / len(case_outcomes)
    spread = max(scores) - min(scores)
    stddev = pstdev(scores) if len(scores) > 1 else 0.0

    return {
        "pass_count": pass_count,
        "fail_count": fail_count,
        "score_mean": mean(scores),
        "score_min": min(scores),
        "score_max": max(scores),
        "score_stddev": stddev,
        "score_spread": spread,
        "cpis": cpis,
        "cpis_hits": cpis_hits,
    }


def load_baseline_score_mean(path):
    if not path:
        return None
    baseline_path = Path(path).expanduser()
    if not baseline_path.exists():
        return None
    try:
        baseline = read_json(baseline_path)
    except Exception:
        return None

    metrics = baseline.get("metrics", {})
    if isinstance(metrics, dict) and metrics.get("score_mean") is not None:
        try:
            return float(metrics.get("score_mean"))
        except (TypeError, ValueError):
            return None

    raw_value = baseline.get("score_mean")
    if raw_value is None:
        return None
    try:
        return float(raw_value)
    except (TypeError, ValueError):
        return None


def build_regression_record(
    *,
    sweep_id,
    suite_name,
    passed,
    failed_cases,
    decision,
    before_commit,
    after_commit,
    metrics,
):
    return {
        "regression_id": f"reg-{sweep_id}",
        "ts": utc_now_iso(),
        "suite": suite_name,
        "before_commit": before_commit,
        "after_commit": after_commit,
        "pass": bool(passed),
        "critical_failures": int(failed_cases),
        "decision": decision,
        "cpis": metrics.get("cpis"),
        "score_mean": metrics.get("score_mean"),
        "score_stddev": metrics.get("score_stddev"),
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="QCHI benchmark and regression sweep runner",
    )
    parser.add_argument("--suite", default=str(DEFAULT_SUITE))
    parser.add_argument("--out", default=str(DEFAULT_OUT))

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute every suite case via `qchi run`",
    )
    parser.add_argument(
        "--results-file",
        help="Use provided case outcomes instead of executing host runs",
    )
    parser.add_argument(
        "--no-log",
        action="store_true",
        help="Do not append eval/regression rows to learning JSONL files",
    )

    parser.add_argument("--learning-dir", default=str(DEFAULT_LEARNING_DIR))
    parser.add_argument("--evals-file", default=str(DEFAULT_EVALS_FILE))
    parser.add_argument("--regressions-file", default=str(DEFAULT_REGRESSIONS_FILE))

    parser.add_argument("--cpis-threshold", type=bounded_score, default=0.90)
    parser.add_argument("--score-threshold", type=bounded_score, default=0.90)
    parser.add_argument("--min-runs", type=positive_int, default=10)
    parser.add_argument("--min-delta", type=float, default=0.0)
    parser.add_argument("--max-spread", type=bounded_score, default=0.30)
    parser.add_argument("--max-stddev", type=bounded_score, default=0.20)
    parser.add_argument(
        "--baseline-summary",
        help="Optional previous summary JSON for delta-vs-baseline check",
    )

    parser.add_argument("--before-commit", default=git_commit_ref("HEAD~1"))
    parser.add_argument("--after-commit", default=git_commit_ref("HEAD"))

    parser.add_argument("--qchi-bin", default=str(DEFAULT_QCHI_BIN))
    parser.add_argument("--host", default="gemini")
    parser.add_argument("--max-retries", type=positive_int, default=3)
    parser.add_argument("--lint-bin")
    parser.add_argument("--run-artifacts-dir")
    parser.add_argument("--project-id")
    parser.add_argument("--learning-track", choices=TRACK_CHOICES)
    return parser.parse_args()


def build_case_outcomes(args, cases, suite_errors, sweep_id):
    mode = "validate"
    case_outcomes = []

    if args.execute and args.results_file:
        suite_errors.append("use either --execute or --results-file, not both")
        return mode, case_outcomes

    if args.execute:
        mode = "execute"
        run_root = (
            Path(args.run_artifacts_dir).expanduser()
            if args.run_artifacts_dir
            else DEFAULT_SWEEP_RUNS_ROOT / sweep_id / "runs"
        )
        for case in cases:
            case_outcomes.append(execute_suite_case(case, args, sweep_id, run_root))
        return mode, case_outcomes

    if args.results_file:
        mode = "results"
        try:
            rows = parse_results_payload(Path(args.results_file).expanduser())
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
            suite_errors.append(f"invalid results file: {exc}")
            return mode, case_outcomes

        result_map, result_errors = normalize_results(rows)
        suite_errors.extend(result_errors)

        for case in cases:
            result = result_map.get(case["case_id"])
            if not result:
                suite_errors.append(f"missing result for case_id={case['case_id']}")
                case_outcomes.append(
                    {
                        "case_id": case["case_id"],
                        "mode": case["mode"],
                        "target": case["target"],
                        "track": args.learning_track or infer_case_track(case),
                        "pass": False,
                        "score": 0.0,
                        "run_id": f"run-results-missing-{case['case_id']}",
                        "reason": "missing result row",
                    }
                )
                continue
            case_outcomes.append(
                {
                    "case_id": case["case_id"],
                    "mode": case["mode"],
                    "target": case["target"],
                    "track": args.learning_track or infer_case_track(case),
                    "pass": result["pass"],
                    "score": float(result["score"]),
                    "run_id": result["run_id"] or f"run-results-{case['case_id']}",
                    "reason": result["reason"],
                }
            )
        return mode, case_outcomes

    return mode, case_outcomes


def main():
    args = parse_args()
    sweep_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suite_data, cases, errors = load_suite(Path(args.suite).expanduser())
    mode, case_outcomes = build_case_outcomes(args, cases, errors, sweep_id)

    metrics = compute_metrics(case_outcomes, score_threshold=args.score_threshold)
    baseline_score_mean = load_baseline_score_mean(args.baseline_summary)
    mean_delta = None
    if metrics["score_mean"] is not None and baseline_score_mean is not None:
        mean_delta = metrics["score_mean"] - baseline_score_mean

    cpis_pass = True
    min_runs_pass = True
    spread_pass = True
    stddev_pass = True
    delta_pass = True
    mode_failures = []

    if mode in {"execute", "results"} and not errors:
        if metrics["fail_count"] > 0:
            mode_failures.append(f"{metrics['fail_count']} case(s) failed")

        if len(case_outcomes) < args.min_runs:
            min_runs_pass = False
            mode_failures.append(
                f"insufficient runs for CPIS target: required >= {args.min_runs}, got {len(case_outcomes)}"
            )

        if metrics["cpis"] is None or metrics["cpis"] < args.cpis_threshold:
            cpis_pass = False
            mode_failures.append(
                f"CPIS below threshold: {metrics['cpis']} < {args.cpis_threshold}"
            )

        if metrics["score_spread"] is not None and metrics["score_spread"] > args.max_spread:
            spread_pass = False
            mode_failures.append(
                f"score spread above threshold: {metrics['score_spread']} > {args.max_spread}"
            )

        if metrics["score_stddev"] is not None and metrics["score_stddev"] > args.max_stddev:
            stddev_pass = False
            mode_failures.append(
                f"score stddev above threshold: {metrics['score_stddev']} > {args.max_stddev}"
            )

        if mean_delta is not None and mean_delta < args.min_delta:
            delta_pass = False
            mode_failures.append(
                f"mean score delta below threshold: {mean_delta} < {args.min_delta}"
            )

    decision = "promote"
    if mode == "validate":
        decision = "validate_only"
    summary_status = "pass"
    all_errors = list(errors)
    if mode in {"execute", "results"}:
        all_errors.extend(mode_failures)
    if all_errors:
        summary_status = "fail"
        decision = "hold"

    suite_name = suite_data.get("suite", "unknown")
    summary = {
        "suite": suite_name,
        "version": suite_data.get("version", 0),
        "mode": mode,
        "sweep_id": sweep_id,
        "case_count": len(cases),
        "evaluated_case_count": len(case_outcomes),
        "status": summary_status,
        "decision": decision,
        "errors": all_errors,
        "metrics": {
            "pass_count": metrics["pass_count"],
            "fail_count": metrics["fail_count"],
            "score_mean": metrics["score_mean"],
            "score_min": metrics["score_min"],
            "score_max": metrics["score_max"],
            "score_spread": metrics["score_spread"],
            "score_stddev": metrics["score_stddev"],
            "cpis": metrics["cpis"],
            "cpis_hits": metrics["cpis_hits"],
            "cpis_threshold": args.cpis_threshold,
            "score_threshold": args.score_threshold,
            "cpis_pass": cpis_pass,
            "min_runs_required": args.min_runs,
            "min_runs_pass": min_runs_pass,
            "stability": {
                "baseline_score_mean": baseline_score_mean,
                "mean_delta": mean_delta,
                "min_delta": args.min_delta,
                "delta_pass": delta_pass,
                "max_spread": args.max_spread,
                "spread_pass": spread_pass,
                "max_stddev": args.max_stddev,
                "stddev_pass": stddev_pass,
            },
        },
        "cases": case_outcomes,
    }

    out_path = Path(args.out).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    if mode in {"execute", "results"} and not args.no_log and case_outcomes:
        evals_path = Path(args.evals_file).expanduser()
        regressions_path = Path(args.regressions_file).expanduser()
        for idx, outcome in enumerate(case_outcomes, start=1):
            append_jsonl(evals_path, build_eval_record(sweep_id, suite_name, outcome, idx))

        regression_record = build_regression_record(
            sweep_id=sweep_id,
            suite_name=suite_name,
            passed=(summary_status == "pass"),
            failed_cases=metrics["fail_count"],
            decision=decision,
            before_commit=str(args.before_commit or "unknown"),
            after_commit=str(args.after_commit or "unknown"),
            metrics=summary["metrics"],
        )
        append_jsonl(regressions_path, regression_record)
        summary["learning_logs"] = {
            "evals_file": str(evals_path),
            "regressions_file": str(regressions_path),
        }
        out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0 if summary_status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
