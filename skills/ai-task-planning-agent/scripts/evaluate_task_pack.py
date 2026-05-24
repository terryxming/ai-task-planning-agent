#!/usr/bin/env python3
"""Evaluate a Task Execution Pack release gate."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from validate_execution_manifest import validate as validate_execution_manifest
from validate_package_manifest import validate as validate_package_manifest
from validate_requirement_model import validate as validate_requirement_model
from validate_clarification_session import validate as validate_clarification_session
from validate_agile_plan import validate as validate_agile_plan
from schema_validator import load_schema, validate_schema


TOOL_REQUIRED_FIELDS = [
    "side_effects",
    "permission_level",
    "failure_modes",
    "retry_policy",
    "rollback_policy",
    "audit_evidence",
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


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def validate_tool_contracts(pack_dir: Path) -> list[str]:
    failures: list[str] = []
    data, load_error = load_json(pack_dir / "tool-contract-matrix.json")
    if load_error:
        return [load_error]

    assert data is not None
    failures.extend(validate_schema(data, load_schema("tool-contract-matrix.schema.json")))
    tools = data.get("tools")
    if not isinstance(tools, list) or not tools:
        return ["tool-contract-matrix.json tools must be a non-empty array"]

    for index, tool in enumerate(tools):
        if not isinstance(tool, dict):
            failures.append(f"tools[{index}] must be an object")
            continue
        for field in TOOL_REQUIRED_FIELDS:
            if not has_value(tool.get(field)):
                failures.append(f"tools[{index}] missing or empty required field: {field}")
    return failures


def validate_eval_plan(pack_dir: Path) -> list[str]:
    data, load_error = load_json(pack_dir / "eval-plan.json")
    if load_error:
        return [load_error]

    assert data is not None
    schema_errors = validate_schema(data, load_schema("eval-plan.schema.json"))
    if schema_errors:
        return schema_errors
    negative_cases = data.get("negative_cases")
    if not isinstance(negative_cases, list) or not negative_cases:
        return ["eval-plan.json negative_cases must be a non-empty array"]
    return []


def detect_markdown_manifest_conflict(pack_dir: Path) -> list[str]:
    task_brief_path = pack_dir / "task-brief.md"
    try:
        task_brief = task_brief_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ["missing required file: task-brief.md"]
    if "MANIFEST_CONFLICT" in task_brief:
        return ["task-brief.md contains MANIFEST_CONFLICT marker"]
    return []


def evaluate(task_pack_dir: str | Path) -> dict[str, Any]:
    pack_dir = Path(task_pack_dir)
    hard_failures: list[str] = []
    warnings: list[str] = []

    package_result = validate_package_manifest(pack_dir)
    hard_failures.extend(f"package-manifest: {error}" for error in package_result["errors"])
    warnings.extend(f"package-manifest: {warning}" for warning in package_result["warnings"])

    clarification_result = validate_clarification_session(pack_dir)
    hard_failures.extend(f"clarification-session: {error}" for error in clarification_result["errors"])
    warnings.extend(f"clarification-session: {warning}" for warning in clarification_result["warnings"])

    requirement_result = validate_requirement_model(pack_dir)
    hard_failures.extend(f"requirement-model: {error}" for error in requirement_result["errors"])
    warnings.extend(f"requirement-model: {warning}" for warning in requirement_result["warnings"])

    agile_result = validate_agile_plan(pack_dir)
    hard_failures.extend(f"agile-plan: {error}" for error in agile_result["errors"])
    warnings.extend(f"agile-plan: {warning}" for warning in agile_result["warnings"])

    execution_result = validate_execution_manifest(pack_dir)
    hard_failures.extend(f"execution-manifest: {error}" for error in execution_result["errors"])
    warnings.extend(f"execution-manifest: {warning}" for warning in execution_result["warnings"])

    hard_failures.extend(f"tool-contract-matrix: {error}" for error in validate_tool_contracts(pack_dir))
    hard_failures.extend(f"eval-plan: {error}" for error in validate_eval_plan(pack_dir))
    hard_failures.extend(
        f"markdown-manifest-conflict: {error}"
        for error in detect_markdown_manifest_conflict(pack_dir)
    )

    release_recommendation = "block" if hard_failures else "pass"
    return {
        "status": "fail" if hard_failures else "pass",
        "hard_failures": hard_failures,
        "warnings": warnings,
        "release_recommendation": release_recommendation,
    }


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3) or (len(argv) == 3 and argv[2] != "--write-result"):
        print(
            json.dumps(
                {
                    "status": "fail",
                    "hard_failures": ["usage: evaluate_task_pack.py <task-pack-dir> [--write-result]"],
                    "warnings": [],
                    "release_recommendation": "block",
                },
                indent=2,
            )
        )
        return 2

    result = evaluate(argv[1])
    if len(argv) == 3:
        result_path = Path(argv[1]) / "evaluation-result.json"
        result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["release_recommendation"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
