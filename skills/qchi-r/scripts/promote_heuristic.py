#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Promote a heuristic with evidence reference")
    p.add_argument("--file", default="heuristics.md")
    p.add_argument("--rule", required=True)
    p.add_argument("--evidence", required=True, help="eval/failure ids or notes")
    p.add_argument("--owner", default="qchi-r")
    args = p.parse_args()

    path = Path(args.file)
    if not path.exists():
        path.write_text("# heuristics\n\n")

    ts = datetime.now(timezone.utc).isoformat()
    line = f"- [{ts}] {args.rule} (evidence: {args.evidence}; owner: {args.owner})\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(line)
    print(path)


if __name__ == "__main__":
    main()
