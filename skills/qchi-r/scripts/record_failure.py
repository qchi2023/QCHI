#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
from pathlib import Path

TEMPLATE = """## {ts}\n- Task: {task}\n- Failure Type: {ftype}\n- Symptom: {symptom}\n- Root Cause: {root}\n- Fix Applied: {fix}\n- Regression Test Added: {test}\n- Status: {status}\n\n"""


def main():
    p = argparse.ArgumentParser(description="Append a failure-pattern entry")
    p.add_argument("--file", default="failure_patterns.md")
    p.add_argument("--task", required=True)
    p.add_argument("--type", required=True, dest="ftype")
    p.add_argument("--symptom", required=True)
    p.add_argument("--root", required=True)
    p.add_argument("--fix", required=True)
    p.add_argument("--test", default="none")
    p.add_argument("--status", default="open", choices=["open", "closed"])
    args = p.parse_args()

    ts = datetime.now(timezone.utc).isoformat()
    out = TEMPLATE.format(ts=ts, task=args.task, ftype=args.ftype, symptom=args.symptom, root=args.root, fix=args.fix, test=args.test, status=args.status)

    path = Path(args.file)
    if not path.exists():
        path.write_text("# failure_patterns\n\n")
    with path.open("a", encoding="utf-8") as f:
        f.write(out)
    print(path)


if __name__ == "__main__":
    main()
