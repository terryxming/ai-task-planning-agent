#!/usr/bin/env python3
"""Validate execution-manifest.json for a Task Execution Pack."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "task_goal",
    "non_goals",
    "input_contract",
    "output_contract",
    "context_contracts",
    "workflow_steps",
    "sandbox_rules",
    "acceptance_criteria",
    "failure_criteria",
    "trace_requirements",
    "recovery_paths",
    "regression_cases",
]


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


def require_non_empty_list(data: dict[str, Any], field: str, errors: list[str]) -> None:
    value = data.get(field)
    if not isinstance(value, list):
        errors.append(f"{field} must be an array")
    elif not value:
        errors.append(f"{field} must be non-empty")


def validate(task_pack_dir: str | Path) -> dict[str, Any]:
    pack_dir = Path(task_pack_dir)
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = pack_dir / "execution-manifest.json"
    manifest, load_error = load_json(manifest_path)

    if load_error:
        errors.append(load_error)
        return {"status": "fail", "errors": errors, "warnings": warnings}

    assert manifest is not None

    for field in REQUIRED_FIELDS:
        if field not in manifest:
            errors.append(f"missing required field: {field}")

    require_non_empty_list(manifest, "trace_requirements", errors)
    require_non_empty_list(manifest, "recovery_paths", errors)
    require_non_empty_list(manifest, "regression_cases", errors)

    status = "fail" if errors else "pass"
    return {"status": status, "errors": errors, "warnings": warnings}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "status": "fail",
                    "errors": ["usage: validate_execution_manifest.py <task-pack-dir>"],
                    "warnings": [],
                },
                indent=2,
            )
        )
        return 2

    result = validate(argv[1])
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
