import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "validate-image-asset-index.py"


def run_validator(index: Path | None = None, json_output: bool = True) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(CLI)]
    if index is not None:
        command.extend(["--index", str(index)])
    if json_output:
        command.append("--json")
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True)


def write_jsonl(path: Path, records: list[dict] | list[str]) -> None:
    lines = []
    for record in records:
        if isinstance(record, str):
            lines.append(record)
        else:
            lines.append(json.dumps(record))
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def valid_record(**overrides: object) -> dict:
    record = {
        "image_id": "img_001",
        "public_url": "http://testserver/uploads/notes/paste.png",
        "sha256": "a" * 64,
        "mime_type": "image/png",
        "size_bytes": 8,
        "source": "note_paste",
    }
    record.update(overrides)
    return record


def parse_json_result(result: subprocess.CompletedProcess[str]) -> dict:
    assert result.returncode in (0, 1), result.stderr
    return json.loads(result.stdout)


def assert_pass(result: subprocess.CompletedProcess[str]) -> dict:
    payload = parse_json_result(result)
    assert result.returncode == 0, result.stderr or result.stdout
    assert payload["result"] == "PASS", payload
    return payload


def assert_fail(result: subprocess.CompletedProcess[str]) -> dict:
    payload = parse_json_result(result)
    assert result.returncode == 1, result.stdout
    assert payload["result"] == "FAIL", payload
    assert payload["errors"], payload
    return payload


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        temp_dir = Path(tmp)

        valid_index = temp_dir / "valid.jsonl"
        write_jsonl(
            valid_index,
            [
                valid_record(),
                valid_record(image_id="img_002", sha256="b" * 64, size_bytes=9),
            ],
        )
        payload = assert_pass(run_validator(valid_index))
        assert payload["total_lines"] == 2, payload
        assert payload["valid_records"] == 2, payload
        assert payload["invalid_records"] == 0, payload

        missing_field_index = temp_dir / "missing-field.jsonl"
        missing_public_url = valid_record(image_id="img_missing")
        del missing_public_url["public_url"]
        write_jsonl(missing_field_index, [missing_public_url])
        payload = assert_fail(run_validator(missing_field_index))
        assert "missing required field: public_url" in payload["errors"][0]["errors"], payload

        invalid_json_index = temp_dir / "invalid-json.jsonl"
        write_jsonl(invalid_json_index, ['{"image_id": "img_bad"'])
        payload = assert_fail(run_validator(invalid_json_index))
        assert "invalid JSON" in payload["errors"][0]["errors"][0], payload

        duplicate_image_id_index = temp_dir / "duplicate-image-id.jsonl"
        write_jsonl(
            duplicate_image_id_index,
            [
                valid_record(image_id="img_dup", sha256="c" * 64),
                valid_record(image_id="img_dup", sha256="d" * 64),
            ],
        )
        payload = assert_fail(run_validator(duplicate_image_id_index))
        assert payload["duplicate_image_id"] == 1, payload

        duplicate_sha_index = temp_dir / "duplicate-sha.jsonl"
        write_jsonl(
            duplicate_sha_index,
            [
                valid_record(image_id="img_sha_1", sha256="e" * 64),
                valid_record(image_id="img_sha_2", sha256="e" * 64),
            ],
        )
        payload = assert_fail(run_validator(duplicate_sha_index))
        assert payload["duplicate_sha256"] == 1, payload

        invalid_values_index = temp_dir / "invalid-values.jsonl"
        write_jsonl(
            invalid_values_index,
            [
                valid_record(
                    image_id="",
                    sha256="",
                    size_bytes=0,
                    source="manual_upload",
                )
            ],
        )
        payload = assert_fail(run_validator(invalid_values_index))
        line_errors = payload["errors"][0]["errors"]
        assert "image_id must be a non-empty string" in line_errors, payload
        assert "sha256 must be a non-empty string" in line_errors, payload
        assert "size_bytes must be a positive integer" in line_errors, payload
        assert "source must be note_paste" in line_errors, payload

        blank_line_index = temp_dir / "blank-line.jsonl"
        blank_line_index.write_text(json.dumps(valid_record()) + "\n\n", encoding="utf-8")
        payload = assert_fail(run_validator(blank_line_index))
        assert "blank line" in payload["errors"][0]["errors"], payload

        empty_index = temp_dir / "empty.jsonl"
        empty_index.write_text("", encoding="utf-8")
        payload = assert_pass(run_validator(empty_index))
        assert payload["total_lines"] == 0, payload

        missing_index = temp_dir / "missing.jsonl"
        payload = assert_fail(run_validator(missing_index))
        assert payload["total_lines"] == 0, payload
        assert "index file does not exist" in payload["errors"][0]["errors"], payload

        text_result = run_validator(valid_index, json_output=False)
        assert text_result.returncode == 0, text_result.stderr
        assert "Image Asset Index Validation" in text_result.stdout, text_result.stdout
        assert "Result: PASS" in text_result.stdout, text_result.stdout

    print("image asset index validation CLI verification passed")


if __name__ == "__main__":
    main()
