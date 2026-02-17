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


def test_eval_compare():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        cur = td / "cur.json"
        base = td / "base.json"
        out = td / "out.json"
        cur.write_text(json.dumps({"scores": [9, 8, 9]}))
        base.write_text(json.dumps({"scores": [7, 8, 7]}))
        r = run(["python3", str(SCRIPTS / "run_evals.py"), "--current", str(cur), "--baseline", str(base), "--min-delta", "0.5", "--out", str(out)])
        assert r.returncode == 0, r.stderr + r.stdout


def test_failure_and_heuristic_logs():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        fp = td / "failure_patterns.md"
        hp = td / "heuristics.md"
        r1 = run(["python3", str(SCRIPTS / "record_failure.py"), "--file", str(fp), "--task", "paper-x", "--type", "mismatch", "--symptom", "fig2 drift", "--root", "wrong grid", "--fix", "refined sweep", "--status", "closed"])
        r2 = run(["python3", str(SCRIPTS / "promote_heuristic.py"), "--file", str(hp), "--rule", "Always cross-check sweep density", "--evidence", "eval#12"])
        assert r1.returncode == 0 and r2.returncode == 0


if __name__ == "__main__":
    test_quality_gate()
    test_eval_compare()
    test_failure_and_heuristic_logs()
    print("PASS")
