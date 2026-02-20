use anyhow::{bail, Context, Result};
use clap::{Parser, Subcommand};
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;

#[derive(Parser)]
#[command(name = "qchi-lint")]
#[command(about = "QCHI policy and artifact linter", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Lint a generated markdown report for required sections and provenance tags
    Report {
        #[arg(long)]
        file: PathBuf,
    },
    /// Validate JSONL records for required fields
    Jsonl {
        #[arg(long)]
        file: PathBuf,
        #[arg(long, value_parser = ["runs", "evals", "regressions"])]
        kind: String,
    },
}

#[derive(Debug, Deserialize)]
struct RunRecord {
    run_id: String,
    ts: String,
    mode: String,
    task_id: String,
    quality_gate_pass: bool,
    status: String,
}

#[derive(Debug, Deserialize)]
struct EvalRecord {
    eval_id: String,
    ts: String,
    run_id: String,
    suite: String,
    case_id: String,
    score: f64,
    pass: bool,
}

#[derive(Debug, Deserialize)]
struct RegressionRecord {
    regression_id: String,
    ts: String,
    suite: String,
    before_commit: String,
    after_commit: String,
    pass: bool,
    decision: String,
}

fn main() -> Result<()> {
    let cli = Cli::parse();
    match cli.command {
        Commands::Report { file } => lint_report(file),
        Commands::Jsonl { file, kind } => lint_jsonl(file, &kind),
    }
}

fn lint_report(file: PathBuf) -> Result<()> {
    let text = fs::read_to_string(&file)
        .with_context(|| format!("failed reading report {}", file.display()))?;

    let required_sections = [
        "## Problem framing",
        "## Assumptions and regime",
        "## Governing equations",
        "## Derivation",
        "## Validation checks",
        "## Final result",
        "## Interpretation and confidence",
        "## Claim provenance",
        "## References",
    ];

    let mut missing = Vec::new();
    for section in required_sections {
        if !text.contains(section) {
            missing.push(section);
        }
    }

    let has_provenance = text.contains("REPRODUCED_FROM_SOURCE")
        || text.contains("INFERRED_ASSUMPTION")
        || text.contains("NEW_EXTENSION");

    if !missing.is_empty() {
        bail!("missing required sections: {}", missing.join(", "));
    }
    if !has_provenance {
        bail!("missing provenance tags in report");
    }

    println!("PASS report lint: {}", file.display());
    Ok(())
}

fn lint_jsonl(file: PathBuf, kind: &str) -> Result<()> {
    let content = fs::read_to_string(&file)
        .with_context(|| format!("failed reading jsonl {}", file.display()))?;

    for (idx, line) in content.lines().enumerate() {
        let line_no = idx + 1;
        if line.trim().is_empty() {
            continue;
        }
        match kind {
            "runs" => {
                let rec: RunRecord = serde_json::from_str(line)
                    .with_context(|| format!("invalid runs record at line {line_no}"))?;
                if rec.run_id.is_empty()
                    || rec.ts.is_empty()
                    || rec.mode.is_empty()
                    || rec.task_id.is_empty()
                    || rec.status.is_empty()
                {
                    bail!("runs record missing required non-empty fields at line {line_no}");
                }
                let _ = rec.quality_gate_pass;
            }
            "evals" => {
                let rec: EvalRecord = serde_json::from_str(line)
                    .with_context(|| format!("invalid evals record at line {line_no}"))?;
                if rec.eval_id.is_empty()
                    || rec.ts.is_empty()
                    || rec.run_id.is_empty()
                    || rec.suite.is_empty()
                    || rec.case_id.is_empty()
                {
                    bail!("evals record missing required non-empty fields at line {line_no}");
                }
                if !(0.0..=1.0).contains(&rec.score) {
                    bail!("evals.score out of range [0,1] at line {line_no}");
                }
                let _ = rec.pass;
            }
            "regressions" => {
                let rec: RegressionRecord = serde_json::from_str(line)
                    .with_context(|| format!("invalid regressions record at line {line_no}"))?;
                if rec.regression_id.is_empty()
                    || rec.ts.is_empty()
                    || rec.suite.is_empty()
                    || rec.before_commit.is_empty()
                    || rec.after_commit.is_empty()
                    || rec.decision.is_empty()
                {
                    bail!("regressions record missing required non-empty fields at line {line_no}");
                }
                let _ = rec.pass;
            }
            _ => bail!("unsupported kind {kind}"),
        }
    }

    println!("PASS jsonl lint: {} ({})", file.display(), kind);
    Ok(())
}
