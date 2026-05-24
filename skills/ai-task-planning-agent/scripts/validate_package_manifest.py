#!/usr/bin/env python3
"""Validate package-manifest.json for a Task Execution Pack."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = [
    "schema_version",
    "package_id",
    "status",
    "target_downstream_ai",
    "known_facts",
    "assumptions",
    "open_questions",
    "blocking_questions",
    "artifacts",
    "quality_gates",
    "human_waivers",
    "release_recommendation",
]

REQUIRED_ARTIFACTS = [
    "package-manifest.json",
    "task-brief.md",
    "agile-plan.md",
    "execution-manifest.json",
    "tool-contract-matrix.json",
    "eval-plan.json",
    "role-decision-log.md",
    "human-review-report.md",
    "governance-report.md",
    "artifact-index.md",
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


def validate(task_pack_dir: str | Path) -> dict[str, Any]:
    pack_dir = Path(task_pack_dir)
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = pack_dir / "package-manifest.json"
    manifest, load_error = load_json(manifest_path)

    if load_error:
        errors.append(load_error)
        return {"status": "fail", "errors": errors, "warnings": warnings}

    assert manifest is not None

    for field in REQUIRED_FIELDS:
        if field not in manifest:
            errors.append(f"missing required field: {field}")

    for artifact in REQUIRED_ARTIFACTS:
        if not (pack_dir / artifact).exists():
            errors.append(f"missing required artifact file: {artifact}")

    manifest_artifacts = manifest.get("artifacts", [])
    if isinstance(manifest_artifacts, list):
        for artifact in manifest_artifacts:
            if not isinstance(artifact, dict):
                errors.append("artifact entries must be objects")
                continue
            artifact_path = artifact.get("path")
            if not artifact_path:
                errors.append("artifact entry missing path")
                continue
            if not (pack_dir / str(artifact_path)).exists():
                errors.append(f"manifest artifact path does not exist: {artifact_path}")
    else:
        errors.append("artifacts must be an array")

    blocking_questions = manifest.get("blocking_questions", [])
    human_waivers = manifest.get("human_waivers", [])
    if blocking_questions and not human_waivers:
        errors.append("blocking_questions present without human_waivers")

    status = "fail" if errors else "pass"
    return {"status": status, "errors": errors, "warnings": warnings}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "status": "fail",
                    "errors": ["usage: validate_package_manifest.py <task-pack-dir>"],
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
