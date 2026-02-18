#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path


def avg(scores):
    return sum(scores) / len(scores) if scores else 0.0


def stddev(scores):
    if not scores:
        return 0.0
    m = avg(scores)
    return math.sqrt(sum((x - m) ** 2 for x in scores) / len(scores))


def load_scores(path: str):
    obj = json.loads(Path(path).read_text())
    return obj["scores"] if isinstance(obj, dict) else obj


def main():
    p = argparse.ArgumentParser(description="Compare evals with stability + CPIS checks")
    p.add_argument("--current", required=True, help="JSON array or object with scores")
    p.add_argument("--baseline", required=True, help="JSON array/object baseline")
    p.add_argument("--current-runs", nargs="*", default=[], help="optional repeated-run score files")
    p.add_argument("--min-delta", type=float, default=0.0, help="required avg improvement")
    p.add_argument("--max-spread", type=float, default=1.5, help="max allowed spread for repeated-run means")
    p.add_argument("--max-stddev", type=float, default=0.75, help="max allowed stddev across repeated-run means")
    p.add_argument("--cpis-min", type=float, default=0.90, help="minimum CPIS threshold")
    p.add_argument("--pass-threshold", type=float, default=8.0, help="run mean to count as pass for CPIS")
    p.add_argument("--out", default="eval_summary.json")
    args = p.parse_args()

    cur_scores = load_scores(args.current)
    base_scores = load_scores(args.baseline)

    cur_avg = avg(cur_scores)
    base_avg = avg(base_scores)
    delta = cur_avg - base_avg

    run_means = []
    if args.current_runs:
        for path in args.current_runs:
            run_means.append(avg(load_scores(path)))
    else:
        run_means = [cur_avg]

    spread = (max(run_means) - min(run_means)) if run_means else 0.0
    run_std = stddev(run_means)
    cpis = sum(1 for m in run_means if m >= args.pass_threshold) / len(run_means) if run_means else 0.0

    pass_delta = delta >= args.min_delta
    pass_stability = spread <= args.max_spread and run_std <= args.max_stddev
    pass_cpis = cpis >= args.cpis_min

    summary = {
        "current_avg": cur_avg,
        "baseline_avg": base_avg,
        "delta": delta,
        "run_means": run_means,
        "spread": spread,
        "stddev": run_std,
        "cpis": cpis,
        "thresholds": {
            "min_delta": args.min_delta,
            "max_spread": args.max_spread,
            "max_stddev": args.max_stddev,
            "cpis_min": args.cpis_min,
            "pass_threshold": args.pass_threshold,
        },
        "passes": {
            "delta": pass_delta,
            "stability": pass_stability,
            "cpis": pass_cpis,
        },
        "pass": pass_delta and pass_stability and pass_cpis,
    }

    Path(args.out).write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary))
    raise SystemExit(0 if summary["pass"] else 2)


if __name__ == "__main__":
    main()
