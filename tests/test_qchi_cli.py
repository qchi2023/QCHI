import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import qchi_cli


REPO_ROOT = Path(__file__).resolve().parents[1]
BIN_QCHI = REPO_ROOT / "bin" / "qchi"


class QchiCliTests(unittest.TestCase):
    def test_normalize_argv_legacy_maps_to_run(self):
        argv = ["--mode", "physics_solve", "--task", "demo"]
        self.assertEqual(qchi_cli.normalize_argv(argv)[0], "run")

    def test_infer_learning_track(self):
        self.assertEqual(qchi_cli.infer_learning_track("paper_reproduction"), "writing")
        self.assertEqual(qchi_cli.infer_learning_track("plot_sweep"), "coding-plotting")
        self.assertEqual(qchi_cli.infer_learning_track("physics_solve"), "physics")

    def test_project_learning_layout_creation(self):
        with tempfile.TemporaryDirectory() as td:
            project_root = Path(td) / "projects" / "proj-demo-2026"
            qchi_cli.ensure_project_learning_layout(project_root)

            for track in qchi_cli.LEARNING_TRACKS:
                for filename in ["runs.jsonl", "evals.jsonl", "regressions.jsonl", "heuristics.yaml"]:
                    self.assertTrue((project_root / track / filename).exists())

    def test_append_run_learning_records(self):
        with tempfile.TemporaryDirectory() as td:
            temp_root = Path(td)
            global_runs = temp_root / "runs.jsonl"
            project_runs = temp_root / "projects" / "proj-demo-2026" / "physics" / "runs.jsonl"

            record = qchi_cli.build_run_learning_record(
                run_id="run-test-001",
                mode="physics_solve",
                task_id="qchi-test",
                quality_gate_pass=True,
                status="completed",
                host="codex",
                task="test task",
                accepted_attempt=1,
                max_retries=3,
                run_dir=temp_root / "run",
            )

            written, errors = qchi_cli.append_run_learning_records(global_runs, project_runs, record)
            self.assertFalse(errors)
            self.assertEqual(len(written), 2)

            global_rows = [json.loads(x) for x in global_runs.read_text(encoding="utf-8").splitlines() if x.strip()]
            project_rows = [json.loads(x) for x in project_runs.read_text(encoding="utf-8").splitlines() if x.strip()]
            self.assertEqual(len(global_rows), 1)
            self.assertEqual(len(project_rows), 1)
            self.assertEqual(global_rows[0]["run_id"], "run-test-001")

    def test_dashboard_help_via_wrapper(self):
        result = subprocess.run(
            [sys.executable, str(BIN_QCHI), "dashboard", "--help"],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(REPO_ROOT),
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("build", result.stdout)
        self.assertIn("serve", result.stdout)

    def test_regression_sweep_via_wrapper_results_mode(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            suite_path = root / "suite.json"
            results_path = root / "results.json"
            out_path = root / "summary.json"

            suite_path.write_text(
                json.dumps(
                    {
                        "suite": "test-suite",
                        "version": 1,
                        "cases": [
                            {
                                "case_id": "case-a",
                                "domain": "physics",
                                "mode": "physics_solve",
                                "target": "task a",
                                "required_checks": ["consistency"],
                            },
                            {
                                "case_id": "case-b",
                                "domain": "writing",
                                "mode": "paper_reproduction",
                                "target": "task b",
                                "required_checks": ["provenance"],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            results_path.write_text(
                json.dumps(
                    {
                        "cases": [
                            {"case_id": "case-a", "pass": True, "score": 0.95, "run_id": "run-a"},
                            {"case_id": "case-b", "pass": True, "score": 0.97, "run_id": "run-b"},
                        ]
                    }
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(BIN_QCHI),
                    "regression",
                    "sweep",
                    "--suite",
                    str(suite_path),
                    "--out",
                    str(out_path),
                    "--results-file",
                    str(results_path),
                    "--no-log",
                    "--min-runs",
                    "1",
                ],
                capture_output=True,
                text=True,
                check=False,
                cwd=str(REPO_ROOT),
            )
            self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)

            summary = json.loads(out_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "pass")
            self.assertEqual(summary["mode"], "results")
            self.assertEqual(summary["evaluated_case_count"], 2)
            self.assertGreaterEqual(summary["metrics"]["cpis"], 0.9)


if __name__ == "__main__":
    unittest.main()
