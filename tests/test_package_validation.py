import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "skills" / "ai-task-planning-agent" / "fixtures"
SCRIPTS = ROOT / "skills" / "ai-task-planning-agent" / "scripts"


class PackageValidationTests(unittest.TestCase):
    def run_script(self, script_name, fixture_name):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / script_name),
                str(FIXTURES / fixture_name),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_fixture_package_manifest_passes(self):
        result = self.run_script("validate_package_manifest.py", "valid-task-pack")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"status": "pass"', result.stdout)

    def test_missing_tool_contract_fixture_fails(self):
        result = self.run_script("validate_package_manifest.py", "missing-tool-contract")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("tool-contract-matrix.json", result.stdout)

    def test_blocking_open_question_fixture_fails(self):
        result = self.run_script("validate_package_manifest.py", "blocking-open-question")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("blocking_questions", result.stdout)

    def test_valid_fixture_execution_manifest_passes(self):
        result = self.run_script("validate_execution_manifest.py", "valid-task-pack")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"status": "pass"', result.stdout)

    def test_missing_recovery_path_fixture_fails(self):
        result = self.run_script("validate_execution_manifest.py", "missing-recovery-path")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("recovery_paths", result.stdout)


if __name__ == "__main__":
    unittest.main()
