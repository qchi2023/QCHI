#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--suite", default="skills/qchi/learning/benchmarks/baseline_v1.json")
    p.add_argument("--out", default="skills/qchi/learning/benchmarks/last_run_summary.json")
    args = p.parse_args()

    suite_path = Path(args.suite)
    data = json.loads(suite_path.read_text(encoding="utf-8"))

    cases = data.get("cases", [])
    required = {"case_id", "domain", "mode", "target", "required_checks"}

    errors = []
    for i, case in enumerate(cases, start=1):
        missing = [k for k in required if k not in case]
        if missing:
            errors.append(f"case#{i} missing fields: {', '.join(missing)}")

    summary = {
        "suite": data.get("suite", "unknown"),
        "version": data.get("version", 0),
        "case_count": len(cases),
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
