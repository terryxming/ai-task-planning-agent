#!/usr/bin/env python3
"""Validate requirement-model.json for a Task Execution Pack."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from schema_validator import load_schema, validate_schema


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


def validate(task_pack_dir: str | Path) -> dict[str, Any]:
    pack_dir = Path(task_pack_dir)
    errors: list[str] = []
    warnings: list[str] = []
    model, load_error = load_json(pack_dir / "requirement-model.json")

    if load_error:
        errors.append(load_error)
        return {"status": "fail", "errors": errors, "warnings": warnings}

    assert model is not None
    errors.extend(validate_schema(model, load_schema("requirement-model.schema.json")))

    if model.get("blocking_questions"):
        errors.append("requirement-model blocking_questions must be empty; no exception is allowed")

    status = "fail" if errors else "pass"
    return {"status": status, "errors": errors, "warnings": warnings}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "status": "fail",
                    "errors": ["usage: validate_requirement_model.py <task-pack-dir>"],
                    "warnings": [],
                },
                indent=2,
            )
        )
        return 2

    result = validate(argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
