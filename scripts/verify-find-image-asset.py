import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "find-image-asset.py"


def run_lookup(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def write_jsonl(path: Path, records: list[dict] | list[str]) -> None:
    lines = []
    for record in records:
        if isinstance(record, str):
            lines.append(record)
        else:
            lines.append(json.dumps(record))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def record(image_id: str, sha256: str, **overrides: object) -> dict:
    item = {
        "image_id": image_id,
        "public_url": f"http://testserver/uploads/notes/{image_id}.png",
        "sha256": sha256,
        "mime_type": "image/png",
        "size_bytes": 8,
        "source": "note_paste",
    }
    item.update(overrides)
    return item


def parse_json(result: subprocess.CompletedProcess[str]) -> dict:
    assert result.returncode in (0, 1), result.stderr
    return json.loads(result.stdout)


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        temp_dir = Path(tmp)
        index = temp_dir / "note-images.jsonl"
        write_jsonl(
            index,
            [
                record("img_001", "a" * 64),
                record("img_002", "b" * 64),
            ],
        )

        by_image_id = run_lookup("--index", str(index), "--image-id", "img_001", "--json")
        payload = parse_json(by_image_id)
        assert by_image_id.returncode == 0, payload
        assert payload["result"] == "FOUND", payload
        assert payload["matches"][0]["image_id"] == "img_001", payload

        by_sha = run_lookup("--index", str(index), "--sha256", "b" * 64, "--json")
        payload = parse_json(by_sha)
        assert by_sha.returncode == 0, payload
        assert payload["result"] == "FOUND", payload
        assert payload["matches"][0]["image_id"] == "img_002", payload

        filtered_index = temp_dir / "filtered.jsonl"
        missing_size = record("img_missing_size", "f" * 64)
        del missing_size["size_bytes"]
        write_jsonl(
            filtered_index,
            [
                record("img_png_small", "1" * 64, mime_type="image/png", size_bytes=10, source="note_paste"),
                record("img_webp_large", "2" * 64, mime_type="image/webp", size_bytes=600, source="note_paste"),
                record("img_manual", "3" * 64, mime_type="image/png", size_bytes=300, source="manual_upload"),
                missing_size,
            ],
        )

        payload = parse_json(run_lookup("--index", str(filtered_index), "--source", "note_paste", "--json"))
        assert payload["result"] == "FOUND", payload
        assert {match["image_id"] for match in payload["matches"]} == {
            "img_png_small",
            "img_webp_large",
            "img_missing_size",
        }, payload

        payload = parse_json(run_lookup("--index", str(filtered_index), "--mime-type", "image/png", "--json"))
        assert payload["result"] == "FOUND", payload
        assert {match["image_id"] for match in payload["matches"]} == {
            "img_png_small",
            "img_manual",
            "img_missing_size",
        }, payload

        payload = parse_json(run_lookup("--index", str(filtered_index), "--min-size", "100", "--json"))
        assert payload["result"] == "FOUND", payload
        assert {match["image_id"] for match in payload["matches"]} == {
            "img_webp_large",
            "img_manual",
        }, payload
        assert payload["warnings"], payload
        assert "missing size_bytes" in payload["warnings"][0]["message"], payload

        payload = parse_json(run_lookup("--index", str(filtered_index), "--max-size", "100", "--json"))
        assert payload["result"] == "FOUND", payload
        assert [match["image_id"] for match in payload["matches"]] == ["img_png_small"], payload

        payload = parse_json(
            run_lookup(
                "--index",
                str(filtered_index),
                "--source",
                "note_paste",
                "--mime-type",
                "image/webp",
                "--min-size",
                "500",
                "--max-size",
                "700",
                "--json",
            )
        )
        assert payload["result"] == "FOUND", payload
        assert [match["image_id"] for match in payload["matches"]] == ["img_webp_large"], payload

        no_filter_match = run_lookup("--index", str(filtered_index), "--source", "unknown", "--json")
        payload = parse_json(no_filter_match)
        assert no_filter_match.returncode == 1, payload
        assert payload["result"] == "NOT_FOUND", payload

        not_found = run_lookup("--index", str(index), "--image-id", "img_missing", "--json")
        payload = parse_json(not_found)
        assert not_found.returncode == 1, payload
        assert payload["result"] == "NOT_FOUND", payload
        assert payload["matches"] == [], payload

        malformed = temp_dir / "malformed.jsonl"
        write_jsonl(malformed, [record("img_good", "c" * 64), '{"image_id":'])
        payload = parse_json(run_lookup("--index", str(malformed), "--image-id", "img_good", "--json"))
        assert payload["result"] == "FOUND", payload
        assert payload["warnings"], payload
        assert "invalid JSON" in payload["warnings"][0]["message"], payload

        duplicate = temp_dir / "duplicate.jsonl"
        write_jsonl(
            duplicate,
            [
                record("img_dup", "d" * 64),
                record("img_dup", "e" * 64),
            ],
        )
        payload = parse_json(run_lookup("--index", str(duplicate), "--image-id", "img_dup", "--json"))
        assert payload["result"] == "FOUND", payload
        assert len(payload["matches"]) == 2, payload
        assert payload["warnings"], payload
        assert "duplicate image_id" in payload["warnings"][0]["message"], payload

        missing = temp_dir / "missing.jsonl"
        missing_result = run_lookup("--index", str(missing), "--image-id", "img_001", "--json")
        payload = parse_json(missing_result)
        assert missing_result.returncode == 1, payload
        assert payload["result"] == "ERROR", payload
        assert "index file does not exist" in payload["warnings"][0]["message"], payload

        text_result = run_lookup("--index", str(index), "--image-id", "img_001")
        assert text_result.returncode == 0, text_result.stderr
        assert "Image Asset Lookup" in text_result.stdout, text_result.stdout
        assert "Result: FOUND" in text_result.stdout, text_result.stdout
        assert "img_001" in text_result.stdout, text_result.stdout

    print("image asset lookup CLI verification passed")


if __name__ == "__main__":
    main()
