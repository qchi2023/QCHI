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

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum CheckStatus {
    Pass,
    Fail,
    Deferred,
    Unknown,
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

    let validation_section = extract_section(&text, "## Validation checks")
        .ok_or_else(|| anyhow::anyhow!("missing or empty '## Validation checks' section"))?;

    lint_four_horsemen(validation_section)?;
    lint_symbolic_verification(&text, validation_section)?;

    println!("PASS report lint: {}", file.display());
    Ok(())
}

fn extract_section<'a>(text: &'a str, section_heading: &str) -> Option<&'a str> {
    let start = text.find(section_heading)?;
    let after_heading = &text[start + section_heading.len()..];
    let next_section = after_heading.find("\n## ").unwrap_or(after_heading.len());
    let body = after_heading[..next_section].trim();
    if body.is_empty() {
        None
    } else {
        Some(body)
    }
}

fn contains_word(text: &str, word: &str) -> bool {
    text.split(|c: char| !c.is_ascii_alphanumeric())
        .any(|tok| tok == word)
}

fn classify_status(line: &str) -> CheckStatus {
    let lower = line.to_ascii_lowercase();

    // Reject template placeholders like "PASS | FAIL | DEFERRED".
    if lower.contains("pass") && lower.contains("fail") && lower.contains('|') {
        return CheckStatus::Unknown;
    }

    let has_pass = ["pass", "passed", "ok", "verified", "valid", "holds", "satisfied"]
        .iter()
        .any(|w| contains_word(&lower, w));
    let has_fail = [
        "fail",
        "failed",
        "error",
        "contradiction",
        "mismatch",
        "invalid",
        "violation",
        "violates",
    ]
    .iter()
    .any(|w| contains_word(&lower, w));
    let has_defer = ["defer", "deferred", "pending", "todo", "tbd", "unknown"]
        .iter()
        .any(|w| contains_word(&lower, w))
        || lower.contains("not run")
        || lower.contains("n/a");

    if has_fail && !has_pass {
        CheckStatus::Fail
    } else if has_defer && !has_pass {
        CheckStatus::Deferred
    } else if has_pass {
        CheckStatus::Pass
    } else {
        CheckStatus::Unknown
    }
}

fn lint_named_check(validation_section: &str, check_name: &str, keywords: &[&str]) -> Result<()> {
    let mut matched_line = false;
    let mut saw_unknown = false;

    for line in validation_section.lines() {
        let lower = line.to_ascii_lowercase();
        if !keywords.iter().any(|kw| lower.contains(kw)) {
            continue;
        }
        matched_line = true;
        match classify_status(&lower) {
            CheckStatus::Pass => return Ok(()),
            CheckStatus::Fail => {
                bail!("{check_name} check is present but reported as failed: {line}")
            }
            CheckStatus::Deferred => {
                bail!("{check_name} check is present but deferred: {line}")
            }
            CheckStatus::Unknown => saw_unknown = true,
        }
    }

    if !matched_line {
        bail!("missing {check_name} check in '## Validation checks'");
    }
    if saw_unknown {
        bail!(
            "{check_name} check found but missing explicit PASS status in '## Validation checks'"
        );
    }
    bail!("missing {check_name} check status in '## Validation checks'");
}

fn lint_four_horsemen(validation_section: &str) -> Result<()> {
    lint_named_check(validation_section, "units", &["unit", "units", "dimensional"])?;
    lint_named_check(
        validation_section,
        "limits",
        &["limit", "limiting-case", "limiting case"],
    )?;
    lint_named_check(validation_section, "asymptotics", &["asymptotic", "asymptotics"])?;
    lint_named_check(
        validation_section,
        "consistency",
        &["consistency", "cross-check", "cross check"],
    )?;
    Ok(())
}

fn lint_symbolic_verification(text: &str, validation_section: &str) -> Result<()> {
    lint_named_check(
        validation_section,
        "symbolic verification",
        &["symbolic verification", "symbolic check", "symbolic verifier"],
    )?;

    let lower = text.to_ascii_lowercase();
    let has_tool = lower.contains("mathematica") || lower.contains("sympy");
    if !has_tool {
        bail!(
            "missing symbolic verification tool marker (must mention Mathematica or SymPy)"
        );
    }

    // Require concrete log evidence, not only a status sentence.
    let has_code_fence = text.contains("```");
    let has_log_marker = lower.contains("symbolic log")
        || lower.contains("verification log")
        || lower.contains("sympy.")
        || lower.contains("sp.")
        || lower.contains("simplify(")
        || lower.contains("fullsimplify")
        || text.contains("In[");

    if !(has_code_fence && has_log_marker) {
        bail!(
            "missing symbolic verification logs: include a fenced code block with Mathematica/SymPy commands and outcomes"
        );
    }
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
