import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "runtime" / "asset-index" / "note-images.jsonl"
REQUIRED_FIELDS = (
    "image_id",
    "public_url",
    "sha256",
    "mime_type",
    "size_bytes",
    "source",
)


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def line_error(line_number: int, errors: list[str]) -> dict[str, Any]:
    return {"line": line_number, "errors": errors}


def validate_record(record: Any, line_number: int) -> tuple[dict[str, Any] | None, list[str]]:
    if not isinstance(record, dict):
        return None, ["record must be a JSON object"]

    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"missing required field: {field}")

    image_id = record.get("image_id")
    if "image_id" in record and (not isinstance(image_id, str) or not image_id.strip()):
        errors.append("image_id must be a non-empty string")

    public_url = record.get("public_url")
    if "public_url" in record and (not isinstance(public_url, str) or not public_url.strip()):
        errors.append("public_url must be a non-empty string")

    sha256 = record.get("sha256")
    if "sha256" in record and (not isinstance(sha256, str) or not sha256.strip()):
        errors.append("sha256 must be a non-empty string")

    mime_type = record.get("mime_type")
    if "mime_type" in record and (not isinstance(mime_type, str) or not mime_type.strip()):
        errors.append("mime_type must be a non-empty string")

    size_bytes = record.get("size_bytes")
    if "size_bytes" in record and (
        not isinstance(size_bytes, int) or isinstance(size_bytes, bool) or size_bytes <= 0
    ):
        errors.append("size_bytes must be a positive integer")

    source = record.get("source")
    if "source" in record and source != "note_paste":
        errors.append("source must be note_paste")

    return record, errors


def validate_index(index_path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "index": display_path(index_path),
        "total_lines": 0,
        "valid_records": 0,
        "invalid_records": 0,
        "duplicate_image_id": 0,
        "duplicate_sha256": 0,
        "result": "PASS",
        "errors": [],
    }

    if not index_path.exists():
        result["result"] = "FAIL"
        result["errors"].append(line_error(0, ["index file does not exist"]))
        return result

    image_ids: list[str] = []
    sha256_values: list[str] = []

    with index_path.open("r", encoding="utf-8") as index_file:
        for line_number, raw_line in enumerate(index_file, start=1):
            result["total_lines"] += 1
            line = raw_line.strip()
            if not line:
                result["invalid_records"] += 1
                result["errors"].append(line_error(line_number, ["blank line"]))
                continue

            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                result["invalid_records"] += 1
                result["errors"].append(line_error(line_number, [f"invalid JSON: {exc.msg}"]))
                continue

            record, errors = validate_record(parsed, line_number)
            if record is not None:
                image_id = record.get("image_id")
                sha256 = record.get("sha256")
                if isinstance(image_id, str) and image_id.strip():
                    image_ids.append(image_id)
                if isinstance(sha256, str) and sha256.strip():
                    sha256_values.append(sha256)

            if errors:
                result["invalid_records"] += 1
                result["errors"].append(line_error(line_number, errors))
            else:
                result["valid_records"] += 1

    duplicate_image_ids = sorted(value for value, count in Counter(image_ids).items() if count > 1)
    duplicate_sha256 = sorted(value for value, count in Counter(sha256_values).items() if count > 1)

    result["duplicate_image_id"] = len(duplicate_image_ids)
    result["duplicate_sha256"] = len(duplicate_sha256)

    for image_id in duplicate_image_ids:
        result["errors"].append(line_error(0, [f"duplicate image_id: {image_id}"]))
    for sha256 in duplicate_sha256:
        result["errors"].append(line_error(0, [f"duplicate sha256: {sha256}"]))

    if result["invalid_records"] or duplicate_image_ids or duplicate_sha256:
        result["result"] = "FAIL"

    return result


def print_text_report(result: dict[str, Any]) -> None:
    print("Image Asset Index Validation")
    print()
    print(f"Index: {result['index']}")
    print(f"Total lines: {result['total_lines']}")
    print(f"Valid records: {result['valid_records']}")
    print(f"Invalid records: {result['invalid_records']}")
    print(f"Duplicate image_id: {result['duplicate_image_id']}")
    print(f"Duplicate sha256: {result['duplicate_sha256']}")
    if result["errors"]:
        print()
        print("Errors:")
        for entry in result["errors"]:
            location = "file" if entry["line"] == 0 else f"line {entry['line']}"
            for error in entry["errors"]:
                print(f"- {location}: {error}")
    print()
    print(f"Result: {result['result']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the FengVoice image asset JSONL index.")
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help="Path to note-images.jsonl. Defaults to runtime/asset-index/note-images.jsonl.",
    )
    parser.add_argument("--json", action="store_true", help="Print validation result as JSON.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate_index(args.index)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_text_report(result)
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
