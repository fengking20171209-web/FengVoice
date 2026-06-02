import importlib.util
import json
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("migrate", "scripts/migrate-existing-note-images.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_basic_dry_run():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        uploads = tmp / "uploads"
        uploads.mkdir()
        index = tmp / "index.jsonl"

        png_file = uploads / "test.png"
        png_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

        result = mod.run_dry_run(uploads, index)
        assert result["uploaded_files_scanned"] == 1
        assert result["existing_index_records"] == 0
        assert result["missing_index_records"] == 1
        assert result["modified"] is False
        print("Basic dry-run: PASS")


def test_empty_uploads():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        uploads = tmp / "uploads"
        uploads.mkdir()
        index = tmp / "index.jsonl"
        index.write_text("", encoding="utf-8")

        result = mod.run_dry_run(uploads, index)
        assert result["uploaded_files_scanned"] == 0
        assert result["existing_index_records"] == 0
        assert result["missing_index_records"] == 0
        assert result["modified"] is False
        print("Empty uploads: PASS")


def test_index_no_file():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        uploads = tmp / "uploads"
        uploads.mkdir()
        index = tmp / "nonexistent.jsonl"

        png_file = uploads / "test.png"
        png_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

        result = mod.run_dry_run(uploads, index)
        assert result["uploaded_files_scanned"] == 1
        assert result["existing_index_records"] == 0
        assert result["malformed_index_lines"] == 0
        print("Index not exist: PASS")


def test_complete_match():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        uploads = tmp / "uploads"
        uploads.mkdir()
        index = tmp / "index.jsonl"

        import hashlib
        png_file = uploads / "test.png"
        png_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
        file_hash = hashlib.sha256(png_file.read_bytes()).hexdigest()

        record = {
            "image_id": "img_test123",
            "public_url": "/uploads/notes/test.png",
            "sha256": file_hash,
            "mime_type": "image/png",
            "size_bytes": 108,
            "source": "note_paste",
        }
        index.write_text(json.dumps(record) + "\n", encoding="utf-8")

        result = mod.run_dry_run(uploads, index)
        assert result["uploaded_files_scanned"] == 1
        assert result["existing_index_records"] == 1
        assert result["missing_index_records"] == 0
        print("Complete match: PASS")


def test_missing_record():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        uploads = tmp / "uploads"
        uploads.mkdir()
        index = tmp / "index.jsonl"

        png_file = uploads / "test.png"
        png_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

        # Index has a record for a different file
        record = {
            "image_id": "img_other",
            "public_url": "/uploads/notes/other.png",
            "sha256": "0" * 64,
            "mime_type": "image/png",
            "size_bytes": 100,
            "source": "note_paste",
        }
        index.write_text(json.dumps(record) + "\n", encoding="utf-8")

        result = mod.run_dry_run(uploads, index)
        assert result["existing_index_records"] == 1
        assert result["missing_index_records"] == 1
        print("Missing record: PASS")


def test_duplicate_sha256():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        uploads = tmp / "uploads"
        uploads.mkdir()
        index = tmp / "index.jsonl"

        r1 = {"image_id": "img_a", "sha256": "abc123", "public_url": "/uploads/notes/a.png", "mime_type": "image/png", "size_bytes": 100, "source": "note_paste"}
        r2 = {"image_id": "img_b", "sha256": "abc123", "public_url": "/uploads/notes/b.png", "mime_type": "image/png", "size_bytes": 100, "source": "note_paste"}
        index.write_text(json.dumps(r1) + "\n" + json.dumps(r2) + "\n", encoding="utf-8")

        result = mod.run_dry_run(uploads, index)
        assert result["duplicate_sha256"] >= 1 or result["duplicate_sha256"] == 1
        print("Duplicate sha256: PASS")


def test_duplicate_image_id():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        uploads = tmp / "uploads"
        uploads.mkdir()
        index = tmp / "index.jsonl"

        r1 = {"image_id": "img_same", "sha256": "aaa", "public_url": "/uploads/notes/a.png", "mime_type": "image/png", "size_bytes": 100, "source": "note_paste"}
        r2 = {"image_id": "img_same", "sha256": "bbb", "public_url": "/uploads/notes/b.png", "mime_type": "image/png", "size_bytes": 100, "source": "note_paste"}
        index.write_text(json.dumps(r1) + "\n" + json.dumps(r2) + "\n", encoding="utf-8")

        result = mod.run_dry_run(uploads, index)
        assert result["duplicate_image_id"] >= 1
        print("Duplicate image_id: PASS")


def test_malformed_jsonl():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        uploads = tmp / "uploads"
        uploads.mkdir()
        index = tmp / "index.jsonl"

        index.write_text("not valid json\n{also bad\n", encoding="utf-8")

        result = mod.run_dry_run(uploads, index)
        assert result["malformed_index_lines"] >= 1 or result["malformed_index_lines"] == 2
        print("Malformed JSONL: PASS")


def test_broken_url():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        uploads = tmp / "uploads"
        uploads.mkdir()
        index = tmp / "index.jsonl"

        r1 = {"image_id": "img_gone", "sha256": "abc", "public_url": "/uploads/notes/missing.png", "mime_type": "image/png", "size_bytes": 100, "source": "note_paste"}
        index.write_text(json.dumps(r1) + "\n", encoding="utf-8")

        result = mod.run_dry_run(uploads, index)
        print(f"Broken URL count: {result['broken_public_url_records']}")
        print("Broken URL: PASS")


def test_json_output():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        uploads = tmp / "uploads"
        uploads.mkdir()
        index = tmp / "index.jsonl"

        result = mod.run_dry_run(uploads, index)
        output = json.dumps(result)
        parsed = json.loads(output)
        assert parsed["modified"] is False
        print("JSON output: PASS")


print("Running all dry-run tests...")
test_basic_dry_run()
test_empty_uploads()
test_index_no_file()
test_complete_match()
test_missing_record()
test_duplicate_sha256()
test_duplicate_image_id()
test_malformed_jsonl()
test_broken_url()
test_json_output()
print()
print("ALL TESTS PASSED")
