#!/usr/bin/env python3
"""Validate agile-plan.json for a Task Execution Pack."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from schema_validator import load_schema, validate_schema


INVEST_FIELDS = ["independent", "negotiable", "valuable", "estimable", "small", "testable"]


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


def validate_story(index: int, story: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(story, dict):
        return [f"user_stories[{index}] must be an object"]
    for field in ["id", "story", "user_role", "goal", "value"]:
        if not has_value(story.get(field)):
            errors.append(f"user_stories[{index}] missing or empty {field}")
    if not isinstance(story.get("acceptance_criteria"), list) or not story.get("acceptance_criteria"):
        errors.append(f"user_stories[{index}].acceptance_criteria must be a non-empty array")
    invest = story.get("invest")
    if not isinstance(invest, dict):
        errors.append(f"user_stories[{index}].invest must be an object")
    else:
        for field in INVEST_FIELDS:
            if not has_value(invest.get(field)):
                errors.append(f"user_stories[{index}].invest missing or empty {field}")
    return errors


def validate(task_pack_dir: str | Path) -> dict[str, Any]:
    pack_dir = Path(task_pack_dir)
    errors: list[str] = []
    warnings: list[str] = []
    plan, load_error = load_json(pack_dir / "agile-plan.json")

    if load_error:
        errors.append(load_error)
        return {"status": "fail", "errors": errors, "warnings": warnings}

    assert plan is not None
    errors.extend(validate_schema(plan, load_schema("agile-plan.schema.json")))

    stories = plan.get("user_stories")
    if isinstance(stories, list):
        for index, story in enumerate(stories):
            errors.extend(validate_story(index, story))

    story_map = plan.get("story_map")
    if not isinstance(story_map, dict) or not has_value(story_map.get("activities")):
        errors.append("story_map.activities must be a non-empty array")

    mvp = plan.get("mvp")
    if not isinstance(mvp, dict) or not has_value(mvp.get("scope")) or not has_value(mvp.get("validation_hypothesis")):
        errors.append("mvp must include non-empty scope and validation_hypothesis")

    increment = plan.get("increment")
    if not isinstance(increment, dict) or not has_value(increment.get("description")) or not has_value(increment.get("verification")):
        errors.append("increment must include non-empty description and verification")

    if not isinstance(plan.get("eval_cases"), list) or not plan.get("eval_cases"):
        errors.append("eval_cases must be a non-empty array")

    status = "fail" if errors else "pass"
    return {"status": status, "errors": errors, "warnings": warnings}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "status": "fail",
                    "errors": ["usage: validate_agile_plan.py <task-pack-dir>"],
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
