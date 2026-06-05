from __future__ import annotations

import importlib
import json
import os
import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "api"))

os.environ["FENGVOICE_DB_PATH"] = str(Path(tempfile.gettempdir()) / "fengvoice-audio-upload-test.db")

main = importlib.import_module("main")
audio_assets = importlib.import_module("audio_assets")
asset_index = importlib.import_module("asset_index")


def patch_audio_paths(tmp: Path) -> None:
    audio_uploads = tmp / "public" / "uploads" / "audio"
    audio_index = tmp / "runtime" / "asset-index" / "note-audio.jsonl"
    image_index = tmp / "runtime" / "asset-index" / "note-images.jsonl"

    audio_uploads.mkdir(parents=True, exist_ok=True)
    image_index.parent.mkdir(parents=True, exist_ok=True)
    image_index.write_text("", encoding="utf-8")

    main.AUDIO_UPLOAD_DIR = audio_uploads
    audio_assets.AUDIO_UPLOAD_DIR = audio_uploads
    audio_assets.AUDIO_INDEX_FILE = audio_index
    asset_index.INDEX_FILE = image_index


def upload(client: TestClient, content: bytes, mime_type: str, filename: str = "recording.webm"):
    return client.post(
        "/api/notes/audio",
        files={"file": (filename, content, mime_type)},
    )


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main_test() -> int:
    with tempfile.TemporaryDirectory(prefix="fengvoice-audio-upload-") as tmp_name:
        tmp = Path(tmp_name)
        patch_audio_paths(tmp)
        client = TestClient(main.app)

        webm = b"\x1a\x45\xdf\xa3" + b"\0" * 100
        response = upload(client, webm, "audio/webm")
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["audio_id"].startswith("aud_")
        assert body["public_url"].startswith("http://testserver/uploads/audio/")
        assert body["mime_type"] == "audio/webm"
        assert body["size_bytes"] == len(webm)
        assert len(body["sha256"]) == 64

        wav = b"RIFF" + (b"\0" * 4) + b"WAVE" + (b"\0" * 32)
        response = upload(client, wav, "audio/wav", "clip.wav")
        assert response.status_code == 200, response.text
        assert response.json()["mime_type"] == "audio/wav"

        response = upload(client, b"not-audio", "text/plain", "bad.txt")
        assert response.status_code == 400

        response = upload(client, b"", "audio/webm")
        assert response.status_code == 400

        audio_records = read_jsonl(audio_assets.AUDIO_INDEX_FILE)
        assert len(audio_records) == 2
        assert audio_records[0]["audio_id"] == body["audio_id"]
        assert audio_records[0]["source"] == "note_audio"
        assert audio_records[0]["public_url"] == body["public_url"]

        image_records = read_jsonl(asset_index.INDEX_FILE)
        assert image_records == []

    print("audio upload verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_test())
