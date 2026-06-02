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
            records.append(parsed)

    return records, warnings


def find_matches(records: list[dict[str, Any]], image_id: str | None, sha256: str | None) -> list[dict[str, Any]]:
    matches = records
    if image_id:
        matches = [record for record in matches if record.get("image_id") == image_id]
    if sha256:
        matches = [record for record in matches if record.get("sha256") == sha256]
    return matches


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


def lookup(index: Path, image_id: str | None, sha256: str | None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "index": display_path(index),
        "query": {"image_id": image_id, "sha256": sha256},
        "result": "NOT_FOUND",
        "matches": [],
        "warnings": [],
    }

    if not index.exists():
        result["result"] = "ERROR"
        result["warnings"].append(warning(0, "index file does not exist"))
        return result

    records, warnings = load_records(index)
    matches = find_matches(records, image_id, sha256)
    warnings.extend(duplicate_warnings(records, matches))

    result["matches"] = matches
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
    parser.add_argument("--json", action="store_true", help="Print lookup result as JSON.")
    args = parser.parse_args()
    if not args.image_id and not args.sha256:
        parser.error("at least one of --image-id or --sha256 is required")
    return args


def main() -> int:
    args = parse_args()
    result = lookup(args.index, args.image_id, args.sha256)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_text(result)
    return 0 if result["result"] == "FOUND" else 1


if __name__ == "__main__":
    raise SystemExit(main())
