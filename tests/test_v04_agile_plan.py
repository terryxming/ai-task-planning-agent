import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "skills" / "ai-task-planning-agent" / "fixtures"
SCRIPTS = ROOT / "skills" / "ai-task-planning-agent" / "scripts"


class V04AgilePlanTests(unittest.TestCase):
    def copy_fixture(self, fixture_name="valid-task-pack"):
        temp_dir = Path(tempfile.mkdtemp(prefix="task-pack-v04-agile-"))
        self.addCleanup(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
        pack_dir = temp_dir / fixture_name
        shutil.copytree(FIXTURES / fixture_name, pack_dir)
        return pack_dir

    def run_script(self, script_name, pack_dir):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script_name), str(pack_dir)],
            capture_output=True,
            text=True,
            check=False,
        )

    def load_plan(self, pack_dir):
        return json.loads((pack_dir / "agile-plan.json").read_text(encoding="utf-8"))

    def write_plan(self, pack_dir, plan):
        (pack_dir / "agile-plan.json").write_text(
            json.dumps(plan, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def test_valid_agile_plan_passes_validator(self):
        result = self.run_script("validate_agile_plan.py", FIXTURES / "valid-task-pack")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"status": "pass"', result.stdout)

    def test_missing_agile_plan_blocks_evaluator(self):
        pack_dir = self.copy_fixture()
        (pack_dir / "agile-plan.json").unlink()

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("agile-plan.json", result.stdout)
        self.assertIn('"release_recommendation": "block"', result.stdout)

    def test_story_without_acceptance_criteria_blocks(self):
        pack_dir = self.copy_fixture()
        plan = self.load_plan(pack_dir)
        plan["user_stories"][0]["acceptance_criteria"] = []
        self.write_plan(pack_dir, plan)

        result = self.run_script("validate_agile_plan.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("acceptance_criteria", result.stdout)

    def test_story_without_complete_invest_blocks(self):
        pack_dir = self.copy_fixture()
        plan = self.load_plan(pack_dir)
        del plan["user_stories"][0]["invest"]["testable"]
        self.write_plan(pack_dir, plan)

        result = self.run_script("validate_agile_plan.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("invest", result.stdout)

    def test_missing_mvp_blocks(self):
        pack_dir = self.copy_fixture()
        plan = self.load_plan(pack_dir)
        plan["mvp"] = {}
        self.write_plan(pack_dir, plan)

        result = self.run_script("validate_agile_plan.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("mvp", result.stdout)

    def test_missing_eval_cases_blocks(self):
        pack_dir = self.copy_fixture()
        plan = self.load_plan(pack_dir)
        plan["eval_cases"] = []
        self.write_plan(pack_dir, plan)

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("eval_cases", result.stdout)


if __name__ == "__main__":
    unittest.main()
