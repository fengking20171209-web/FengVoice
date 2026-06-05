import importlib.util
import json
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("asset_search", "services/api/asset_search.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def make_record(image_id: str, **kwargs) -> dict:
    rec = {
        "image_id": image_id,
        "public_url": f"/uploads/notes/{image_id}.png",
        "sha256": "a" * 64,
        "mime_type": "image/png",
        "size_bytes": 1000,
        "source": "note_paste",
    }
    rec.update(kwargs)
    return rec


def write_index(path: Path, records: list[dict]):
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")


def test_index_not_found():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        idx = tmp / "nonexistent.jsonl"
        records, warnings = mod.read_asset_index(idx)
        assert records == [], f"Expected empty, got {records}"
        assert len(warnings) >= 1
        assert "not found" in warnings[0].lower()
    print("Index not found: PASS")


def test_empty_index():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        idx = tmp / "index.jsonl"
        idx.write_text("", encoding="utf-8")
        records, warnings = mod.read_asset_index(idx)
        assert records == []
        assert warnings == []
    print("Empty index: PASS")


def test_list_records():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        idx = tmp / "index.jsonl"
        write_index(idx, [make_record("img_a"), make_record("img_b")])
        result = mod.list_assets(index_path=idx)
        assert result["count"] == 2
        assert len(result["items"]) == 2
    print("List records: PASS")


def test_find_by_image_id():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        idx = tmp / "index.jsonl"
        write_index(idx, [make_record("img_a"), make_record("img_b")])
        records, _ = mod.read_asset_index(idx)
        found = mod.find_asset_by_image_id(records, "img_a")
        assert found is not None
        assert found["image_id"] == "img_a"
        not_found = mod.find_asset_by_image_id(records, "img_z")
        assert not_found is None
    print("Find by image_id: PASS")


def test_filter_sha256():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        idx = tmp / "index.jsonl"
        write_index(idx, [
            make_record("img_a", sha256="aaa"),
            make_record("img_b", sha256="bbb"),
        ])
        records, _ = mod.read_asset_index(idx)
        filtered = mod.filter_asset_records(records, sha256="aaa")
        assert len(filtered) == 1
        assert filtered[0]["image_id"] == "img_a"
    print("Filter sha256: PASS")


def test_filter_source():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        idx = tmp / "index.jsonl"
        write_index(idx, [
            make_record("img_a", source="note_paste"),
            make_record("img_b", source="import"),
        ])
        records, _ = mod.read_asset_index(idx)
        filtered = mod.filter_asset_records(records, source="import")
        assert len(filtered) == 1
        assert filtered[0]["image_id"] == "img_b"
    print("Filter source: PASS")


def test_filter_mime():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        idx = tmp / "index.jsonl"
        write_index(idx, [
            make_record("img_a", mime_type="image/png"),
            make_record("img_b", mime_type="image/jpeg"),
        ])
        records, _ = mod.read_asset_index(idx)
        filtered = mod.filter_asset_records(records, mime_type="image/jpeg")
        assert len(filtered) == 1
        assert filtered[0]["mime_type"] == "image/jpeg"
    print("Filter mime_type: PASS")


def test_filter_size():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        idx = tmp / "index.jsonl"
        write_index(idx, [
            make_record("img_a", size_bytes=100),
            make_record("img_b", size_bytes=500),
            make_record("img_c", size_bytes=1000),
        ])
        records, _ = mod.read_asset_index(idx)
        filtered = mod.filter_asset_records(records, min_size=200, max_size=800)
        assert len(filtered) == 1
        assert filtered[0]["image_id"] == "img_b"
    print("Filter size: PASS")


def test_malformed_jsonl():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        idx = tmp / "index.jsonl"
        idx.write_text("not valid json\n{\"image_id\": \"img_a\"}\nbad line\n", encoding="utf-8")
        records, warnings = mod.read_asset_index(idx)
        assert len(records) == 1  # Only the valid line
        assert len(warnings) >= 1
    print("Malformed JSONL: PASS")


def test_limit():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        idx = tmp / "index.jsonl"
        write_index(idx, [make_record(f"img_{i}") for i in range(10)])
        result = mod.list_assets(index_path=idx, limit=3)
        assert result["count"] == 10
        assert len(result["items"]) == 3
    print("Limit: PASS")


print("Running all asset API tests...")
test_index_not_found()
test_empty_index()
test_list_records()
test_find_by_image_id()
test_filter_sha256()
test_filter_source()
test_filter_mime()
test_filter_size()
test_malformed_jsonl()
test_limit()
print()
print("ALL TESTS PASSED")
