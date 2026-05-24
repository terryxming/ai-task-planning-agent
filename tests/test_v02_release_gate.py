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


class V02ReleaseGateTests(unittest.TestCase):
    def copy_fixture(self, fixture_name="valid-task-pack"):
        temp_dir = Path(tempfile.mkdtemp(prefix="task-pack-"))
        self.addCleanup(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
        pack_dir = temp_dir / fixture_name
        shutil.copytree(FIXTURES / fixture_name, pack_dir)
        return pack_dir

    def write_json(self, path, data):
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def run_script(self, script_name, pack_dir, *extra_args):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script_name), str(pack_dir), *extra_args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_package_manifest_schema_rejects_invalid_release_recommendation(self):
        pack_dir = self.copy_fixture()
        manifest_path = pack_dir / "package-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["release_recommendation"] = "ship"
        self.write_json(manifest_path, manifest)

        result = self.run_script("validate_package_manifest.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("release_recommendation", result.stdout)
        self.assertIn("enum", result.stdout)

    def test_tool_contract_schema_rejects_missing_input_schema(self):
        pack_dir = self.copy_fixture()
        matrix_path = pack_dir / "tool-contract-matrix.json"
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        matrix["tools"][0].pop("input_schema")
        self.write_json(matrix_path, matrix)

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("input_schema", result.stdout)

    def test_eval_plan_schema_rejects_missing_manual_review_required(self):
        pack_dir = self.copy_fixture()
        eval_path = pack_dir / "eval-plan.json"
        eval_plan = json.loads(eval_path.read_text(encoding="utf-8"))
        eval_plan.pop("manual_review_required")
        self.write_json(eval_path, eval_plan)

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("manual_review_required", result.stdout)

    def test_blocking_question_waiver_requires_expiration_condition(self):
        pack_dir = self.copy_fixture()
        manifest_path = pack_dir / "package-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["blocking_questions"] = ["Which repository should the downstream AI modify?"]
        manifest["human_waivers"] = [
            {
                "item": "repository target",
                "reason": "Owner approved local-only planning.",
                "accepted_risk": "Pack may need retargeting before execution.",
                "scope": "This fixture only.",
                "owner": "fixture owner"
            }
        ]
        manifest["release_recommendation"] = "block"
        self.write_json(manifest_path, manifest)

        result = self.run_script("validate_package_manifest.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("expiration_condition", result.stdout)

    def test_evaluator_can_write_evaluation_result_json(self):
        pack_dir = self.copy_fixture()

        result = self.run_script("evaluate_task_pack.py", pack_dir, "--write-result")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        result_path = pack_dir / "evaluation-result.json"
        self.assertTrue(result_path.exists())
        evaluation = json.loads(result_path.read_text(encoding="utf-8"))
        self.assertEqual(evaluation["release_recommendation"], "pass")

    def test_readme_uses_chinese_as_default_language(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("## 快速验证", readme)
        self.assertIn("非目标", readme)
        self.assertNotIn("AI Task Planning Agent helps", readme)


if __name__ == "__main__":
    unittest.main()
