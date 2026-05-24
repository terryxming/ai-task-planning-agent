import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "ai-task-planning-agent" / "SKILL.md"
VALIDATOR = ROOT / "skills" / "ai-task-planning-agent" / "scripts" / "validate_skill_entry.py"


class V04SkillGovernanceTests(unittest.TestCase):
    def run_validator(self, path):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(path)],
            capture_output=True,
            text=True,
            check=False,
        )

    def write_temp_skill(self, content):
        temp_dir = tempfile.TemporaryDirectory(prefix="skill-entry-v04-")
        self.addCleanup(temp_dir.cleanup)
        path = Path(temp_dir.name) / "SKILL.md"
        path.write_text(content, encoding="utf-8")
        return path

    def test_current_skill_entry_passes_governance(self):
        result = self.run_validator(SKILL)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"status": "pass"', result.stdout)

    def test_skill_entry_requires_v04_scripts(self):
        content = SKILL.read_text(encoding="utf-8").replace(
            "- `scripts/validate_clarification_session.py <task-pack-dir>`\n",
            "",
        )
        path = self.write_temp_skill(content)

        result = self.run_validator(path)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("validate_clarification_session.py", result.stdout)

    def test_skill_entry_requires_chinese_description(self):
        content = SKILL.read_text(encoding="utf-8").replace(
            "把模糊 AI builder 任务规划为可验证的 Task Execution Pack",
            "Plan fuzzy AI builder tasks into verifiable Task Execution Packs",
        )
        path = self.write_temp_skill(content)

        result = self.run_validator(path)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("description", result.stdout)

    def test_skill_entry_rejects_overgrown_domain_knowledge(self):
        content = SKILL.read_text(encoding="utf-8") + "\n" + ("额外领域知识\n" * 130)
        path = self.write_temp_skill(content)

        result = self.run_validator(path)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("too long", result.stdout)

    def test_skill_entry_requires_v04_fact_sources_in_hard_failures(self):
        content = SKILL.read_text(encoding="utf-8").replace("- 缺少 `agile-plan.json`。\n", "")
        path = self.write_temp_skill(content)

        result = self.run_validator(path)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("agile-plan.json", result.stdout)


if __name__ == "__main__":
    unittest.main()
