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


VALID_REQUIREMENT_MODEL = {
    "raw_idea": "我想把模糊 AI builder 任务规划成可验证执行包。",
    "trigger_reasons": ["模糊任务直接进入执行会导致方向跑偏。"],
    "problem_statement": "AI builder 缺少从模糊想法到可执行需求模型的稳定中间层。",
    "current_state": "用户只有模糊想法，AI 容易直接进入执行。",
    "target_state": "用户获得可被 Agile 和 Harness 使用的结构化需求模型。",
    "target_users": ["AI Agent builder"],
    "usage_scenarios": ["创建 Skill 前", "设计 Agent 前", "复杂任务规划前"],
    "jobs_to_be_done": ["把模糊想法转成可执行、可验证、可交付的需求模型。"],
    "desired_outputs": ["Task Execution Pack"],
    "scope_in": ["需求挖掘", "需求建模", "进入 Agile 前的 readiness gate"],
    "scope_out": ["直接执行用户业务代码", "连接生产环境", "替代 Jira 或 Linear"],
    "constraints": ["默认中文表达", "JSON 文件是机器事实源"],
    "success_criteria": ["需求模型字段完整", "blocking questions 为空", "可进入 Agile 规划"],
    "failure_criteria": ["缺少 problem statement", "缺少目标用户", "缺少使用场景"],
    "requirement_groups": [{"name": "需求建模", "items": ["真实问题", "目标状态", "用户场景"]}],
    "priorities": [{"item": "requirement-model.json", "priority": "Must"}],
    "validation_evidence": ["valid fixture evaluator pass"],
    "blocking_questions": []
}


class V03RequirementModelTests(unittest.TestCase):
    def copy_fixture(self, fixture_name="valid-task-pack"):
        temp_dir = Path(tempfile.mkdtemp(prefix="task-pack-v03-"))
        self.addCleanup(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
        pack_dir = temp_dir / fixture_name
        shutil.copytree(FIXTURES / fixture_name, pack_dir)
        return pack_dir

    def write_json(self, path, data):
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def run_script(self, script_name, pack_dir):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script_name), str(pack_dir)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_fixture_contains_requirement_model_and_passes(self):
        pack_dir = FIXTURES / "valid-task-pack"

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((pack_dir / "requirement-model.json").exists())

    def test_missing_requirement_model_blocks_release(self):
        pack_dir = self.copy_fixture()
        requirement_model = pack_dir / "requirement-model.json"
        if requirement_model.exists():
            requirement_model.unlink()

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("requirement-model.json", result.stdout)
        self.assertIn('"release_recommendation": "block"', result.stdout)

    def test_empty_problem_statement_blocks_release(self):
        pack_dir = self.copy_fixture()
        model = dict(VALID_REQUIREMENT_MODEL)
        model["problem_statement"] = ""
        self.write_json(pack_dir / "requirement-model.json", model)

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("problem_statement", result.stdout)

    def test_missing_target_users_blocks_release(self):
        pack_dir = self.copy_fixture()
        model = dict(VALID_REQUIREMENT_MODEL)
        model["target_users"] = []
        self.write_json(pack_dir / "requirement-model.json", model)

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("target_users", result.stdout)

    def test_requirement_blocking_questions_block_without_exception(self):
        pack_dir = self.copy_fixture()
        model = dict(VALID_REQUIREMENT_MODEL)
        model["blocking_questions"] = ["目标用户尚未确认。"]
        self.write_json(pack_dir / "requirement-model.json", model)

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("blocking_questions", result.stdout)

    def test_package_manifest_must_register_requirement_model(self):
        pack_dir = self.copy_fixture()
        manifest_path = pack_dir / "package-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["artifacts"] = [
            artifact
            for artifact in manifest["artifacts"]
            if artifact.get("path") != "requirement-model.json"
        ]
        self.write_json(manifest_path, manifest)
        self.write_json(pack_dir / "requirement-model.json", VALID_REQUIREMENT_MODEL)

        result = self.run_script("validate_package_manifest.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("requirement-model.json", result.stdout)


if __name__ == "__main__":
    unittest.main()
