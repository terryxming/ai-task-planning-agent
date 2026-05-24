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


class V04ClarificationCouncilTests(unittest.TestCase):
    def copy_fixture(self, fixture_name="valid-task-pack"):
        temp_dir = Path(tempfile.mkdtemp(prefix="task-pack-v04-clarification-"))
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

    def load_session(self, pack_dir):
        return json.loads((pack_dir / "clarification-session.json").read_text(encoding="utf-8"))

    def write_session(self, pack_dir, session):
        (pack_dir / "clarification-session.json").write_text(
            json.dumps(session, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def test_valid_clarification_session_passes_validator(self):
        result = self.run_script("validate_clarification_session.py", FIXTURES / "valid-task-pack")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"status": "pass"', result.stdout)

    def test_missing_clarification_session_blocks_evaluator(self):
        pack_dir = self.copy_fixture()
        (pack_dir / "clarification-session.json").unlink()

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("clarification-session.json", result.stdout)
        self.assertIn('"release_recommendation": "block"', result.stdout)

    def test_each_round_requires_exactly_five_questions_with_rationale(self):
        pack_dir = self.copy_fixture()
        session = self.load_session(pack_dir)
        session["rounds"][0]["questions"][0]["rationale"] = ""
        self.write_session(pack_dir, session)

        result = self.run_script("validate_clarification_session.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("rationale", result.stdout)

    def test_unconfirmed_round_blocks_next_stage(self):
        pack_dir = self.copy_fixture()
        session = self.load_session(pack_dir)
        session["rounds"][0]["user_confirmed"] = False
        self.write_session(pack_dir, session)

        result = self.run_script("evaluate_task_pack.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("user_confirmed", result.stdout)

    def test_missing_critique_blocks_clarification(self):
        pack_dir = self.copy_fixture()
        session = self.load_session(pack_dir)
        session["rounds"][0]["critiques"] = []
        self.write_session(pack_dir, session)

        result = self.run_script("validate_clarification_session.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("critiques", result.stdout)

    def test_role_contribution_must_bind_impacted_fields(self):
        pack_dir = self.copy_fixture()
        session = self.load_session(pack_dir)
        session["rounds"][0]["role_contributions"][0]["field_updates"] = []
        self.write_session(pack_dir, session)

        result = self.run_script("validate_clarification_session.py", pack_dir)

        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("field_updates", result.stdout)


if __name__ == "__main__":
    unittest.main()
