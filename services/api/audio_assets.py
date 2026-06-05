from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

ROOT_DIR = Path(__file__).resolve().parents[2]
PUBLIC_DIR = ROOT_DIR / "public"
AUDIO_UPLOAD_DIR = PUBLIC_DIR / "uploads" / "audio"
RUNTIME_DIR = ROOT_DIR / "runtime"
INDEX_DIR = RUNTIME_DIR / "asset-index"
AUDIO_INDEX_FILE = INDEX_DIR / "note-audio.jsonl"

MAX_AUDIO_UPLOAD_BYTES = 50 * 1024 * 1024
ALLOWED_AUDIO_MIME_TYPES = {
    "audio/webm",
    "audio/wav",
    "audio/mpeg",
    "audio/mp4",
    "audio/ogg",
}

_AUDIO_EXTENSIONS = {
    "audio/webm": ".webm",
    "audio/wav": ".wav",
    "audio/mpeg": ".mp3",
    "audio/mp4": ".m4a",
    "audio/ogg": ".ogg",
}


def ensure_audio_dirs() -> None:
    AUDIO_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_DIR.mkdir(parents=True, exist_ok=True)


def audio_safe_extension(content_type: str) -> str:
    return _AUDIO_EXTENSIONS.get(content_type, ".webm")


def next_audio_filename(content_type: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{uuid4().hex}{audio_safe_extension(content_type)}"


def validate_audio_signature(content_type: str, content: bytes) -> bool:
    if content_type == "audio/webm":
        return content.startswith(b"\x1a\x45\xdf\xa3")
    if content_type == "audio/wav":
        return len(content) >= 12 and content.startswith(b"RIFF") and content[8:12] == b"WAVE"
    if content_type == "audio/mpeg":
        return content.startswith(b"ID3") or content.startswith((b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"))
    if content_type == "audio/mp4":
        return len(content) >= 8 and content[4:8] == b"ftyp"
    if content_type == "audio/ogg":
        return content.startswith(b"OggS")
    return False


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(65536):
            digest.update(chunk)
    return digest.hexdigest()


def audio_stored_path(file_path: Path) -> str:
    try:
        return str(file_path.relative_to(ROOT_DIR))
    except ValueError:
        return file_path.name


def create_note_audio_record(
    *,
    file_path: Path,
    public_url: str,
    mime_type: str,
    source: str = "note_audio",
    note_id: str | None = None,
) -> dict:
    ensure_audio_dirs()
    audio_id = f"aud_{uuid4().hex}"
    stat = file_path.stat()
    record = {
        "audio_id": audio_id,
        "note_id": note_id,
        "public_url": public_url,
        "stored_filename": file_path.name,
        "stored_path": audio_stored_path(file_path),
        "sha256": sha256_file(file_path),
        "mime_type": mime_type,
        "size_bytes": stat.st_size,
        "source": source,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with AUDIO_INDEX_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record
