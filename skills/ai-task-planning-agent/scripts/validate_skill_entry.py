#!/usr/bin/env python3
"""Validate the ai-task-planning-agent SKILL.md entry contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


MAX_LINES = 125
MAX_CHARS = 9000
REQUIRED_FRONTMATTER_FIELDS = {"name", "description"}
REQUIRED_DESCRIPTION_FRAGMENT = "把模糊 AI builder 任务规划为可验证的 Task Execution Pack"
REQUIRED_REFERENCES = [
    "references/frontdoor-orchestrator.md",
    "references/clarification-engine.md",
    "references/clarification-council.md",
    "references/requirement-discovery-modeling.md",
    "references/agile-value-planner.md",
    "references/harness-execution-planner.md",
    "references/role-council.md",
    "references/delivery-packager.md",
    "references/evaluator-release-gate.md",
    "references/governance-layer.md",
    "references/skill-governance.md",
]
REQUIRED_SCRIPTS = [
    "scripts/validate_package_manifest.py",
    "scripts/validate_clarification_session.py",
    "scripts/validate_requirement_model.py",
    "scripts/validate_agile_plan.py",
    "scripts/validate_execution_manifest.py",
    "scripts/evaluate_task_pack.py",
    "scripts/render_artifact_index.py",
    "scripts/validate_skill_entry.py",
]
REQUIRED_FACT_SOURCES = [
    "package-manifest.json",
    "clarification-session.json",
    "requirement-model.json",
    "agile-plan.json",
    "execution-manifest.json",
    "tool-contract-matrix.json",
    "eval-plan.json",
]


def parse_frontmatter(content: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return {}, ["frontmatter must start with ---"]
    try:
        end_index = lines[1:].index("---") + 1
    except ValueError:
        return {}, ["frontmatter must end with ---"]

    fields: dict[str, str] = {}
    for line in lines[1:end_index]:
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    extra_fields = set(fields) - REQUIRED_FRONTMATTER_FIELDS
    missing_fields = REQUIRED_FRONTMATTER_FIELDS - set(fields)
    if extra_fields:
        errors.append(f"frontmatter has unsupported fields: {sorted(extra_fields)}")
    if missing_fields:
        errors.append(f"frontmatter missing fields: {sorted(missing_fields)}")
    return fields, errors


def path_exists_if_local(skill_path: Path, relative_path: str) -> bool:
    candidate = skill_path.parent / relative_path
    return candidate.exists()


def validate(skill_path: str | Path) -> dict[str, list[str] | str]:
    path = Path(skill_path)
    errors: list[str] = []
    warnings: list[str] = []

    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {"status": "fail", "errors": [f"missing required file: {path}"], "warnings": warnings}

    fields, frontmatter_errors = parse_frontmatter(content)
    errors.extend(frontmatter_errors)

    if fields.get("name") != "ai-task-planning-agent":
        errors.append("frontmatter name must be ai-task-planning-agent")
    description = fields.get("description", "")
    if REQUIRED_DESCRIPTION_FRAGMENT not in description:
        errors.append("description must keep the default Chinese product trigger")
    if not re.search(r"[\u4e00-\u9fff]", description):
        errors.append("description must include Chinese text")

    lines = content.splitlines()
    if len(lines) > MAX_LINES or len(content) > MAX_CHARS:
        errors.append("SKILL.md too long; move domain knowledge into references")

    for relative_path in REQUIRED_REFERENCES:
        if relative_path not in content:
            errors.append(f"SKILL.md missing required reference: {relative_path}")
        elif not path_exists_if_local(path, relative_path):
            errors.append(f"required reference path does not exist: {relative_path}")

    for relative_path in REQUIRED_SCRIPTS:
        if relative_path not in content:
            errors.append(f"SKILL.md missing required script: {relative_path}")
        elif not path_exists_if_local(path, relative_path):
            errors.append(f"required script path does not exist: {relative_path}")

    for fact_source in REQUIRED_FACT_SOURCES:
        if f"缺少 `{fact_source}`" not in content:
            errors.append(f"SKILL.md hard failures must mention {fact_source}")

    return {"status": "fail" if errors else "pass", "errors": errors, "warnings": warnings}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "status": "fail",
                    "errors": ["usage: validate_skill_entry.py <path-to-SKILL.md>"],
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
