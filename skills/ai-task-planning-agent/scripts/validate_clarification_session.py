#!/usr/bin/env python3
"""Validate clarification-session.json for a Task Execution Pack."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from schema_validator import load_schema, validate_schema


QUESTION_FIELDS = ["sequence", "question", "rationale", "consequence_if_unanswered", "suggested_answer"]
CRITIQUE_FIELDS = ["role", "issue", "impact", "fields", "blocking", "recommendation"]
ROLE_FIELDS = ["role", "statement", "challenge", "supplement", "field_updates", "blocking"]


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        return None, f"missing required file: {path.name}"
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON in {path.name}: {exc}"
    if not isinstance(data, dict):
        return None, f"{path.name} must contain a JSON object"
    return data, None


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def validate_question(round_index: int, question_index: int, question: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(question, dict):
        return [f"rounds[{round_index}].questions[{question_index}] must be an object"]
    for field in QUESTION_FIELDS:
        if not has_value(question.get(field)):
            errors.append(f"rounds[{round_index}].questions[{question_index}] missing or empty {field}")
    return errors


def validate_critique(round_index: int, critique_index: int, critique: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(critique, dict):
        return [f"rounds[{round_index}].critiques[{critique_index}] must be an object"]
    for field in CRITIQUE_FIELDS:
        if field == "blocking":
            if not isinstance(critique.get(field), bool):
                errors.append(f"rounds[{round_index}].critiques[{critique_index}] blocking must be boolean")
        elif not has_value(critique.get(field)):
            errors.append(f"rounds[{round_index}].critiques[{critique_index}] missing or empty {field}")
    return errors


def validate_role_contribution(round_index: int, role_index: int, contribution: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(contribution, dict):
        return [f"rounds[{round_index}].role_contributions[{role_index}] must be an object"]
    for field in ROLE_FIELDS:
        if field == "blocking":
            if not isinstance(contribution.get(field), bool):
                errors.append(f"rounds[{round_index}].role_contributions[{role_index}] blocking must be boolean")
        elif not has_value(contribution.get(field)):
            errors.append(f"rounds[{round_index}].role_contributions[{role_index}] missing or empty {field}")
    return errors


def validate_round(round_index: int, round_data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(round_data, dict):
        return [f"rounds[{round_index}] must be an object"]

    questions = round_data.get("questions")
    if not isinstance(questions, list) or len(questions) != 5:
        errors.append(f"rounds[{round_index}].questions must contain exactly five questions")
    else:
        for question_index, question in enumerate(questions):
            errors.extend(validate_question(round_index, question_index, question))

    critiques = round_data.get("critiques")
    if not isinstance(critiques, list) or not critiques:
        errors.append(f"rounds[{round_index}].critiques must be a non-empty array")
    else:
        for critique_index, critique in enumerate(critiques):
            errors.extend(validate_critique(round_index, critique_index, critique))

    role_contributions = round_data.get("role_contributions")
    if not isinstance(role_contributions, list) or not role_contributions:
        errors.append(f"rounds[{round_index}].role_contributions must be a non-empty array")
    else:
        for role_index, contribution in enumerate(role_contributions):
            errors.extend(validate_role_contribution(round_index, role_index, contribution))

    if not has_value(round_data.get("user_answer")):
        errors.append(f"rounds[{round_index}].user_answer must be non-empty")
    if not has_value(round_data.get("revised_understanding")):
        errors.append(f"rounds[{round_index}].revised_understanding must be non-empty")
    if round_data.get("user_confirmed") is not True:
        errors.append(f"rounds[{round_index}].user_confirmed must be true before next stage")

    return errors


def validate(task_pack_dir: str | Path) -> dict[str, Any]:
    pack_dir = Path(task_pack_dir)
    errors: list[str] = []
    warnings: list[str] = []
    session, load_error = load_json(pack_dir / "clarification-session.json")

    if load_error:
        errors.append(load_error)
        return {"status": "fail", "errors": errors, "warnings": warnings}

    assert session is not None
    errors.extend(validate_schema(session, load_schema("clarification-session.schema.json")))

    rounds = session.get("rounds")
    if isinstance(rounds, list):
        for round_index, round_data in enumerate(rounds):
            errors.extend(validate_round(round_index, round_data))

    if session.get("blocking_questions"):
        errors.append("clarification-session blocking_questions must be empty before planning")

    status = "fail" if errors else "pass"
    return {"status": status, "errors": errors, "warnings": warnings}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "status": "fail",
                    "errors": ["usage: validate_clarification_session.py <task-pack-dir>"],
                    "warnings": [],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 2

    result = validate(argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
