#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def avg(scores):
    return sum(scores) / len(scores) if scores else 0.0


def main():
    p = argparse.ArgumentParser(description="Compare eval results against baseline and fail on regression")
    p.add_argument("--current", required=True, help="JSON array or object with test scores")
    p.add_argument("--baseline", required=True, help="JSON array/object baseline")
    p.add_argument("--min-delta", type=float, default=0.0, help="required avg improvement over baseline")
    p.add_argument("--out", default="eval_summary.json")
    args = p.parse_args()

    cur = json.loads(Path(args.current).read_text())
    base = json.loads(Path(args.baseline).read_text())

    cur_scores = cur["scores"] if isinstance(cur, dict) else cur
    base_scores = base["scores"] if isinstance(base, dict) else base

    cur_avg = avg(cur_scores)
    base_avg = avg(base_scores)
    delta = cur_avg - base_avg

    summary = {
        "current_avg": cur_avg,
        "baseline_avg": base_avg,
        "delta": delta,
        "pass": delta >= args.min_delta,
        "min_delta": args.min_delta,
    }

    Path(args.out).write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary))
    raise SystemExit(0 if summary["pass"] else 2)


if __name__ == "__main__":
    main()
