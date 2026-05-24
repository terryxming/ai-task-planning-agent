#!/usr/bin/env python3
"""Render artifact-index.md from package-manifest.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def load_manifest(pack_dir: Path) -> dict[str, Any]:
    with (pack_dir / "package-manifest.json").open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("package-manifest.json must contain a JSON object")
    return data


def render_index(manifest: dict[str, Any]) -> str:
    release_recommendation = manifest.get("release_recommendation", "block")
    lines = [
        "# Artifact Index",
        "",
        f"Release recommendation: `{release_recommendation}`",
        "",
        "| Path | Type | Purpose |",
        "|---|---|---|",
    ]

    for artifact in manifest.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        path = artifact.get("path", "")
        artifact_type = artifact.get("type", "")
        purpose = artifact.get("purpose", "")
        lines.append(f"| `{path}` | {artifact_type} | {purpose} |")

    lines.append("")
    return "\n".join(lines)


def render(task_pack_dir: str | Path) -> dict[str, Any]:
    pack_dir = Path(task_pack_dir)
    manifest = load_manifest(pack_dir)
    output_path = pack_dir / "artifact-index.md"
    output_path.write_text(render_index(manifest), encoding="utf-8")
    return {"status": "pass", "artifact_index": str(output_path)}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "status": "fail",
                    "artifact_index": None,
                    "errors": ["usage: render_artifact_index.py <task-pack-dir>"],
                },
                indent=2,
            )
        )
        return 2

    try:
        result = render(argv[1])
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(
            json.dumps(
                {"status": "fail", "artifact_index": None, "errors": [str(exc)]},
                indent=2,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
