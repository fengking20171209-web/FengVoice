from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("fengvoice.asset_search")

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_INDEX = ROOT_DIR / "runtime" / "asset-index" / "note-images.jsonl"

REQUIRED_FIELDS = ("image_id", "public_url", "sha256", "mime_type", "size_bytes", "source")


def read_asset_index(index_path: Path | None = None) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    warnings: list[str] = []
    path = index_path or DEFAULT_INDEX

    if not path.exists():
        warnings.append(f"Asset index not found: {path}")
        return records, warnings

    with path.open("r", encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                warnings.append(f"Line {line_number}: invalid JSON ({exc.msg})")
                continue
            if not isinstance(parsed, dict):
                warnings.append(f"Line {line_number}: non-object record")
                continue
            records.append(parsed)

    return records, warnings


def _safe_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def filter_asset_records(
    records: list[dict[str, Any]],
    image_id: str | None = None,
    sha256: str | None = None,
    source: str | None = None,
    mime_type: str | None = None,
    min_size: int | None = None,
    max_size: int | None = None,
) -> list[dict[str, Any]]:
    filtered = records

    if image_id:
        filtered = [r for r in filtered if r.get("image_id") == image_id]
    if sha256:
        filtered = [r for r in filtered if r.get("sha256") == sha256]
    if source:
        filtered = [r for r in filtered if r.get("source") == source]
    if mime_type:
        filtered = [r for r in filtered if r.get("mime_type") == mime_type]
    if min_size is not None:
        filtered = [r for r in filtered if (_safe_int(r.get("size_bytes")) or 0) >= min_size]
    if max_size is not None:
        filtered = [r for r in filtered if (_safe_int(r.get("size_bytes")) or 0) <= max_size]

    return filtered


def find_asset_by_image_id(
    records: list[dict[str, Any]],
    image_id: str,
) -> dict[str, Any] | None:
    for record in records:
        if record.get("image_id") == image_id:
            return record
    return None


def list_assets(
    index_path: Path | None = None,
    image_id: str | None = None,
    sha256: str | None = None,
    source: str | None = None,
    mime_type: str | None = None,
    min_size: int | None = None,
    max_size: int | None = None,
    limit: int = 100,
) -> dict[str, Any]:
    records, warnings = read_asset_index(index_path)
    filtered = filter_asset_records(
        records,
        image_id=image_id,
        sha256=sha256,
        source=source,
        mime_type=mime_type,
        min_size=min_size,
        max_size=max_size,
    )
    return {
        "items": filtered[:limit],
        "count": len(filtered),
        "warnings": warnings,
    }
