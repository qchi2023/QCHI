#!/usr/bin/env python3
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(cmd):
    return subprocess.run(cmd, check=False, text=True, capture_output=True)


def test_quality_gate():
    sample = ROOT / "examples" / "sample_response.md"
    r = run(["python3", str(SCRIPTS / "quality_gate_check.py"), "--input", str(sample)])
    assert r.returncode == 0, r.stderr + r.stdout


def test_eval_compare_with_stability_and_cpis():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        cur = td / "cur.json"
        base = td / "base.json"
        run1 = td / "run1.json"
        run2 = td / "run2.json"
        run3 = td / "run3.json"
        out = td / "out.json"

        cur.write_text(json.dumps({"scores": [9, 8, 9]}))
        base.write_text(json.dumps({"scores": [7, 8, 7]}))
        run1.write_text(json.dumps({"scores": [9, 9, 8]}))
        run2.write_text(json.dumps({"scores": [8, 9, 8]}))
        run3.write_text(json.dumps({"scores": [9, 8, 9]}))

        r = run([
            "python3", str(SCRIPTS / "run_evals.py"),
            "--current", str(cur),
            "--baseline", str(base),
            "--current-runs", str(run1), str(run2), str(run3),
            "--min-delta", "0.5",
            "--max-spread", "1.5",
            "--max-stddev", "0.75",
            "--cpis-min", "0.66",
            "--pass-threshold", "8.0",
            "--out", str(out),
        ])
        assert r.returncode == 0, r.stderr + r.stdout
        summary = json.loads(out.read_text())
        assert summary["pass"] is True
        assert "cpis" in summary


def test_failure_heuristic_and_cost_logs():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        fp = td / "failure_patterns.md"
        hp = td / "heuristics.md"
        cp = td / "cost_reliability.jsonl"

        r1 = run([
            "python3", str(SCRIPTS / "record_failure.py"),
            "--file", str(fp), "--task", "paper-x", "--type", "mismatch",
            "--symptom", "fig2 drift", "--root", "wrong grid", "--fix", "refined sweep", "--status", "closed"
        ])
        r2 = run([
            "python3", str(SCRIPTS / "promote_heuristic.py"),
            "--file", str(hp), "--rule", "Always cross-check sweep density", "--evidence", "eval#12"
        ])
        r3 = run([
            "python3", str(SCRIPTS / "log_cost_reliability.py"),
            "--file", str(cp), "--run-id", "r1", "--protocol", "multi-path-v1",
            "--tokens", "12000", "--seconds", "45", "--pass-flag", "true", "--mean-score", "8.7", "--cpis", "0.9"
        ])

        assert r1.returncode == 0 and r2.returncode == 0 and r3.returncode == 0
        assert cp.exists() and cp.read_text().strip() != ""


if __name__ == "__main__":
    test_quality_gate()
    test_eval_compare_with_stability_and_cpis()
    test_failure_heuristic_and_cost_logs()
    print("PASS")
