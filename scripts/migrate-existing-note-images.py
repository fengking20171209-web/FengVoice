import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_UPLOADS = ROOT / "public" / "uploads" / "notes"
DEFAULT_INDEX = ROOT / "runtime" / "asset-index" / "note-images.jsonl"
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
EXTENSION_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}
REQUIRED_FIELDS = ("image_id", "public_url", "sha256", "mime_type", "size_bytes", "source")


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def load_index(index: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    malformed_lines: list[str] = []
    if not index.exists():
        return records, malformed_lines
    with index.open("r", encoding="utf-8") as f:
        for line_number, raw_line in enumerate(f, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                malformed_lines.append(f"line {line_number}: invalid JSON")
                continue
            if not isinstance(parsed, dict):
                malformed_lines.append(f"line {line_number}: non-object record")
                continue
            records.append(parsed)
    return records, malformed_lines


def scan_uploads(uploads_dir: Path) -> list[tuple[Path, str, str]]:
    results: list[tuple[Path, str, str]] = []
    if not uploads_dir.exists():
        return results
    for entry in sorted(uploads_dir.iterdir()):
        if not entry.is_file():
            continue
        ext = entry.suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            continue
        file_hash = sha256_of(entry)
        mime = EXTENSION_MIME.get(ext, "image/png")
        results.append((entry, file_hash, mime))
    return results


def run_dry_run(
    uploads_dir: Path,
    index_path: Path,
) -> dict[str, Any]:
    uploaded_files = scan_uploads(uploads_dir)
    index_records, malformed_lines = load_index(index_path)

    # Build lookup maps from index
    sha256_in_index: set[str] = set()
    image_id_in_index: set[str] = set()
    public_urls_in_index: set[str] = set()
    for rec in index_records:
        s = rec.get("sha256")
        if s:
            sha256_in_index.add(s)
        iid = rec.get("image_id")
        if iid:
            image_id_in_index.add(iid)
        url = rec.get("public_url", "")
        if url:
            public_urls_in_index.add(url)

    # Check for missing records
    missing_records: list[dict[str, Any]] = []
    for path, file_hash, mime in uploaded_files:
        if file_hash not in sha256_in_index:
            missing_records.append({
                "filename": path.name,
                "path": display_path(path),
                "sha256": file_hash,
                "mime_type": mime,
            })

    # Check duplicate sha256 in index
    sha256_counts: dict[str, int] = {}
    for rec in index_records:
        s = rec.get("sha256", "")
        if s:
            sha256_counts[s] = sha256_counts.get(s, 0) + 1
    duplicate_sha256 = sum(1 for c in sha256_counts.values() if c > 1)

    # Check duplicate image_id in index
    id_counts: dict[str, int] = {}
    for rec in index_records:
        iid = rec.get("image_id", "")
        if iid:
            id_counts[iid] = id_counts.get(iid, 0) + 1
    duplicate_image_id = sum(1 for c in id_counts.values() if c > 1)

    # Check broken public_url records
    broken_urls = 0
    for rec in index_records:
        url = rec.get("public_url", "")
        if url and not url.startswith("/uploads/"):
            broken_urls += 1
        else:
            # Extract relative path and check file existence
            relative = url.removeprefix("/uploads/")
            target = ROOT / "public" / "uploads" / relative
            if not target.exists():
                broken_urls += 1

    # Determine result
    has_issues = (
        len(missing_records) > 0
        or duplicate_sha256 > 0
        or duplicate_image_id > 0
        or broken_urls > 0
        or len(malformed_lines) > 0
    )
    result_status = "PASS" if not has_issues else "WARN"

    return {
        "uploads": display_path(uploads_dir),
        "index": display_path(index_path),
        "uploaded_files_scanned": len(uploaded_files),
        "existing_index_records": len(index_records),
        "missing_index_records": len(missing_records),
        "missing_record_details": missing_records,
        "duplicate_sha256": duplicate_sha256,
        "duplicate_image_id": duplicate_image_id,
        "broken_public_url_records": broken_urls,
        "malformed_index_lines": len(malformed_lines),
        "malformed_line_details": malformed_lines,
        "result": result_status,
        "modified": False,
    }


def print_text_report(result: dict[str, Any]) -> None:
    print("Image Migration Dry Run")
    print()
    print(f"Uploads: {result['uploads']}")
    print(f"Index: {result['index']}")
    print()
    print(f"Uploaded files scanned: {result['uploaded_files_scanned']}")
    print(f"Existing index records: {result['existing_index_records']}")
    print(f"Missing index records: {result['missing_index_records']}")
    if result["missing_index_records"] > 0 and result.get("missing_record_details"):
        for detail in result["missing_record_details"]:
            print(f"  - {detail['filename']} (sha256: {detail['sha256'][:12]}...)")
    print(f"Duplicate sha256 in index: {result['duplicate_sha256']}")
    print(f"Duplicate image_id in index: {result['duplicate_image_id']}")
    print(f"Broken public_url records: {result['broken_public_url_records']}")
    print(f"Malformed index lines: {result['malformed_index_lines']}")
    if result["malformed_index_lines"] > 0 and result.get("malformed_line_details"):
        for detail in result["malformed_line_details"]:
            print(f"  - {detail}")
    print()
    print(f"Result: {result['result']}")
    print("No files were modified.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dry-run migration tool for existing uploaded note images."
    )
    parser.add_argument(
        "--uploads",
        type=Path,
        default=DEFAULT_UPLOADS,
        help=f"Path to uploaded images directory. Defaults to {display_path(DEFAULT_UPLOADS)}.",
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help=f"Path to note-images.jsonl. Defaults to {display_path(DEFAULT_INDEX)}.",
    )
    parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Explicit dry-run mode. Default: enabled.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        default=False,
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.apply:
        print("Error: --apply is not implemented yet. This release only supports dry-run.")
        return 1

    result = run_dry_run(uploads_dir=args.uploads, index_path=args.index)
    result["modified"] = False

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_text_report(result)

    return 0 if result["result"] == "PASS" else 0  # dry-run never fails


if __name__ == "__main__":
    raise SystemExit(main())
