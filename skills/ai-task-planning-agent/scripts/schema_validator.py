"""Small JSON Schema subset validator for the repository's local schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


def load_schema(schema_name: str) -> dict[str, Any]:
    with (SCHEMA_DIR / schema_name).open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    if not isinstance(schema, dict):
        raise ValueError(f"{schema_name} must contain a JSON object")
    return schema


def validate_schema(data: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")

    if expected_type and not type_matches(data, expected_type):
        errors.append(f"schema: {path} type expected {expected_type}")
        return errors

    if "enum" in schema and data not in schema["enum"]:
        errors.append(f"schema: {path} enum expected one of {schema['enum']}")

    if isinstance(data, str) and "minLength" in schema and len(data) < schema["minLength"]:
        errors.append(f"schema: {path} minLength expected at least {schema['minLength']}")

    if isinstance(data, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(data) < min_items:
            errors.append(f"schema: {path} minItems expected at least {min_items}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(data):
                errors.extend(validate_schema(item, item_schema, f"{path}[{index}]"))

    if isinstance(data, dict):
        for field in schema.get("required", []):
            if field not in data:
                errors.append(f"schema: {path}.{field} missing required field")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for field, field_schema in properties.items():
                if field in data and isinstance(field_schema, dict):
                    errors.extend(validate_schema(data[field], field_schema, f"{path}.{field}"))

    return errors


def type_matches(data: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(data, dict)
    if expected_type == "array":
        return isinstance(data, list)
    if expected_type == "string":
        return isinstance(data, str)
    if expected_type == "boolean":
        return isinstance(data, bool)
    if expected_type == "number":
        return isinstance(data, (int, float)) and not isinstance(data, bool)
    if expected_type == "integer":
        return isinstance(data, int) and not isinstance(data, bool)
    return True
