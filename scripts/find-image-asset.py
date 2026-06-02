import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "runtime" / "asset-index" / "note-images.jsonl"


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def warning(line: int, message: str) -> dict[str, Any]:
    return {"line": line, "message": message}


def load_records(index: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    with index.open("r", encoding="utf-8") as index_file:
        for line_number, raw_line in enumerate(index_file, start=1):
            line = raw_line.strip()
            if not line:
                warnings.append(warning(line_number, "blank line skipped"))
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError as exc:
                warnings.append(warning(line_number, f"invalid JSON skipped: {exc.msg}"))
                continue
            if not isinstance(parsed, dict):
                warnings.append(warning(line_number, "non-object JSON record skipped"))
                continue
            parsed["_line_number"] = line_number
            records.append(parsed)

    return records, warnings


def find_matches(
    records: list[dict[str, Any]],
    image_id: str | None,
    sha256: str | None,
    source: str | None,
    mime_type: str | None,
    min_size: int | None,
    max_size: int | None,
    warnings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    matches = records
    if image_id:
        matches = [record for record in matches if record.get("image_id") == image_id]
    if sha256:
        matches = [record for record in matches if record.get("sha256") == sha256]
    if source:
        matches = [record for record in matches if record.get("source") == source]
    if mime_type:
        matches = [record for record in matches if record.get("mime_type") == mime_type]
    if min_size is not None:
        matches = filter_by_size(matches, min_size, None, warnings)
    if max_size is not None:
        matches = filter_by_size(matches, None, max_size, warnings)
    return matches


def filter_by_size(
    records: list[dict[str, Any]],
    min_size: int | None,
    max_size: int | None,
    warnings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for record in records:
        size = record.get("size_bytes")
        if not isinstance(size, int) or isinstance(size, bool):
            warnings.append(warning(int(record.get("_line_number", 0)), "missing size_bytes for size filter"))
            continue
        if min_size is not None and size < min_size:
            continue
        if max_size is not None and size > max_size:
            continue
        filtered.append(record)
    return filtered


def public_record(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key != "_line_number"}


def duplicate_warnings(records: list[dict[str, Any]], matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    image_ids = [record.get("image_id") for record in records if isinstance(record.get("image_id"), str)]
    sha_values = [record.get("sha256") for record in records if isinstance(record.get("sha256"), str)]
    duplicate_image_ids = {value for value, count in Counter(image_ids).items() if count > 1}
    duplicate_sha_values = {value for value, count in Counter(sha_values).items() if count > 1}

    matched_image_ids = {record.get("image_id") for record in matches}
    matched_sha_values = {record.get("sha256") for record in matches}

    for image_id in sorted(duplicate_image_ids & matched_image_ids):
        warnings.append(warning(0, f"duplicate image_id found: {image_id}"))
    for sha256 in sorted(duplicate_sha_values & matched_sha_values):
        warnings.append(warning(0, f"duplicate sha256 found: {sha256}"))

    return warnings


def lookup(
    index: Path,
    image_id: str | None,
    sha256: str | None,
    source: str | None,
    mime_type: str | None,
    min_size: int | None,
    max_size: int | None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "index": display_path(index),
        "query": {
            "image_id": image_id,
            "sha256": sha256,
            "source": source,
            "mime_type": mime_type,
            "min_size": min_size,
            "max_size": max_size,
        },
        "result": "NOT_FOUND",
        "matches": [],
        "warnings": [],
    }

    if not index.exists():
        result["result"] = "ERROR"
        result["warnings"].append(warning(0, "index file does not exist"))
        return result

    records, warnings = load_records(index)
    matches = find_matches(records, image_id, sha256, source, mime_type, min_size, max_size, warnings)
    warnings.extend(duplicate_warnings(records, matches))

    result["matches"] = [public_record(match) for match in matches]
    result["warnings"] = warnings
    if matches:
        result["result"] = "FOUND"
    return result


def print_text(result: dict[str, Any]) -> None:
    print("Image Asset Lookup")
    print()
    print(f"Index: {result['index']}")
    query = result["query"]
    if query.get("image_id"):
        print(f"image_id: {query['image_id']}")
    if query.get("sha256"):
        print(f"sha256: {query['sha256']}")
    if query.get("source"):
        print(f"source: {query['source']}")
    if query.get("mime_type"):
        print(f"mime_type: {query['mime_type']}")
    if query.get("min_size") is not None:
        print(f"min_size: {query['min_size']}")
    if query.get("max_size") is not None:
        print(f"max_size: {query['max_size']}")
    print(f"Matches: {len(result['matches'])}")

    if result["matches"]:
        print()
        for idx, match in enumerate(result["matches"], start=1):
            print(f"Match {idx}:")
            print(f"  image_id: {match.get('image_id', '')}")
            print(f"  sha256: {match.get('sha256', '')}")
            print(f"  public_url: {match.get('public_url', '')}")
            print(f"  mime_type: {match.get('mime_type', '')}")
            print(f"  size_bytes: {match.get('size_bytes', '')}")

    if result["warnings"]:
        print()
        print("Warnings:")
        for item in result["warnings"]:
            location = "file" if item["line"] == 0 else f"line {item['line']}"
            print(f"- {location}: {item['message']}")

    print()
    print(f"Result: {result['result']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Find records in the FengVoice image asset JSONL index.")
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help="Path to note-images.jsonl. Defaults to runtime/asset-index/note-images.jsonl.",
    )
    parser.add_argument("--image-id", help="Find records with this image_id.")
    parser.add_argument("--sha256", help="Find records with this sha256.")
    parser.add_argument("--source", help="Filter records by source.")
    parser.add_argument("--mime-type", help="Filter records by mime_type.")
    parser.add_argument("--min-size", type=int, help="Filter records with size_bytes greater than or equal to this value.")
    parser.add_argument("--max-size", type=int, help="Filter records with size_bytes less than or equal to this value.")
    parser.add_argument("--json", action="store_true", help="Print lookup result as JSON.")
    args = parser.parse_args()
    if args.min_size is not None and args.min_size < 0:
        parser.error("--min-size must be non-negative")
    if args.max_size is not None and args.max_size < 0:
        parser.error("--max-size must be non-negative")
    if args.min_size is not None and args.max_size is not None and args.min_size > args.max_size:
        parser.error("--min-size cannot be greater than --max-size")
    if not any(
        value is not None
        for value in (args.image_id, args.sha256, args.source, args.mime_type, args.min_size, args.max_size)
    ):
        parser.error("at least one lookup or filter option is required")
    return args


def main() -> int:
    args = parse_args()
    result = lookup(args.index, args.image_id, args.sha256, args.source, args.mime_type, args.min_size, args.max_size)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_text(result)
    return 0 if result["result"] == "FOUND" else 1


if __name__ == "__main__":
    raise SystemExit(main())
