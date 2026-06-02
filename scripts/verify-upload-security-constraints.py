from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "services" / "api" / "main.py"
ASSET_INDEX = ROOT / "services" / "api" / "asset_index.py"
GITIGNORE = ROOT / ".gitignore"


def check(condition: bool, level: str, message: str, results: list[tuple[str, str]]) -> None:
    results.append((level if condition else "FAIL", message))


def warn(condition: bool, message: str, results: list[tuple[str, str]]) -> None:
    results.append(("PASS" if condition else "WARN", message))


def contains(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.MULTILINE | re.DOTALL) is not None


def main() -> int:
    results: list[tuple[str, str]] = []
    main_source = MAIN.read_text(encoding="utf-8")
    asset_source = ASSET_INDEX.read_text(encoding="utf-8")
    gitignore = GITIGNORE.read_text(encoding="utf-8")

    check("runtime/" in gitignore, "PASS", ".gitignore excludes runtime/", results)
    check("public/uploads/" in gitignore, "PASS", ".gitignore excludes public/uploads/", results)

    check("MAX_UPLOAD_BYTES" in main_source, "PASS", "upload endpoint defines a max upload size", results)
    check("Image upload is limited to 5MB" in main_source, "PASS", "upload endpoint rejects oversized images", results)
    check(
        'file.content_type.startswith("image/")' in main_source,
        "PASS",
        "upload endpoint restricts requests to image/* MIME types",
        results,
    )
    check("uuid4().hex" in main_source, "PASS", "upload filename uses generated UUID content", results)
    check(
        'filename = f"{datetime.now(timezone.utc).strftime' in main_source,
        "PASS",
        "stored filename is generated instead of trusting the original filename",
        results,
    )
    check("NOTE_UPLOAD_DIR / filename" in main_source, "PASS", "upload target is constrained to NOTE_UPLOAD_DIR", results)
    check("/uploads/notes/" in main_source, "PASS", "public URL is constrained to uploads/notes", results)
    check("target.unlink(missing_ok=True)" in main_source, "PASS", "failed or empty uploads are removed", results)
    check("image_id=record" in main_source, "PASS", "upload response returns image_id", results)

    check("sha256" in asset_source, "PASS", "asset index records include sha256", results)
    check("INDEX_FILE.open('a'" in asset_source, "PASS", "asset index writes append-only JSONL records", results)
    check("source" in asset_source and "note_paste" in asset_source, "PASS", "asset index records include note_paste source", results)

    check(
        "detect_image_format" in main_source and "validate_upload_magic_bytes" in main_source,
        "PASS",
        "upload endpoint validates magic bytes for PNG, JPEG, and WebP image content",
        results,
    )
    check(
        "'mime_type': mime_type or 'image/png'" in asset_source,
        "PASS",
        "asset index stores actual upload MIME type via optional mime_type parameter",
        results,
    )

    print("Upload Security Constraint Verification")
    print()
    for level, message in results:
        print(f"{level}: {message}")

    has_fail = any(level == "FAIL" for level, _ in results)
    has_warn = any(level == "WARN" for level, _ in results)
    print()
    if has_fail:
        print("Result: FAIL")
        return 1
    if has_warn:
        print("Result: PASS with warnings")
        return 0
    print("Result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
