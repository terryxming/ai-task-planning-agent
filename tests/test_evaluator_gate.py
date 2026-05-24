import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "skills" / "ai-task-planning-agent" / "fixtures"
EVALUATOR = ROOT / "skills" / "ai-task-planning-agent" / "scripts" / "evaluate_task_pack.py"


class EvaluatorGateTests(unittest.TestCase):
    def run_evaluator(self, fixture_name):
        return subprocess.run(
            [sys.executable, str(EVALUATOR), str(FIXTURES / fixture_name)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_fixture_returns_zero(self):
        result = self.run_evaluator("valid-task-pack")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"release_recommendation": "pass"', result.stdout)

    def test_missing_tool_contract_returns_two(self):
        result = self.run_evaluator("missing-tool-contract")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('"release_recommendation": "block"', result.stdout)

    def test_blocking_open_question_returns_two(self):
        result = self.run_evaluator("blocking-open-question")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('"release_recommendation": "block"', result.stdout)

    def test_missing_recovery_path_returns_two(self):
        result = self.run_evaluator("missing-recovery-path")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('"release_recommendation": "block"', result.stdout)

    def test_markdown_manifest_conflict_returns_two(self):
        result = self.run_evaluator("markdown-manifest-conflict")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("MANIFEST_CONFLICT", result.stdout)


if __name__ == "__main__":
    unittest.main()
