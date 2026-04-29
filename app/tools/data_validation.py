"""CSV validation helpers for experiment data."""

from __future__ import annotations

from typing import Any


REQUIRED_COLUMNS = {"user_id", "group"}


def validate_experiment_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"valid": False, "errors": ["CSV contains no rows."], "warnings": []}
    columns = set(rows[0].keys())
    missing = sorted(REQUIRED_COLUMNS - columns)
    errors = [f"Missing required column: {column}" for column in missing]
    groups = {str(row.get("group", "")).strip().lower() for row in rows}
    warnings: list[str] = []
    if not {"control", "treatment"}.issubset(groups):
        warnings.append("Expected both control and treatment groups.")
    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "columns": sorted(columns),
        "row_count": len(rows),
    }


def infer_metric_columns(rows: list[dict[str, Any]]) -> dict[str, list[str]]:
    if not rows:
        return {"numeric": [], "binary": [], "categorical": []}
    ignored = {"user_id", "group", "segment", "device", "country", "date", "market", "city"}
    numeric: list[str] = []
    binary: list[str] = []
    categorical: list[str] = []
    for column in rows[0].keys():
        if column in ignored:
            continue
        values = [str(row.get(column, "")).strip() for row in rows[:100] if str(row.get(column, "")).strip() != ""]
        if not values:
            continue
        parsed: list[float] = []
        all_numeric = True
        for value in values:
            try:
                parsed.append(float(value))
            except ValueError:
                all_numeric = False
                break
        if not all_numeric:
            categorical.append(column)
            continue
        unique = {value for value in parsed}
        if unique.issubset({0.0, 1.0}):
            binary.append(column)
        else:
            numeric.append(column)
    return {"numeric": numeric, "binary": binary, "categorical": categorical}

