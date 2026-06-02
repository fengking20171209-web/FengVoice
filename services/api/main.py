from __future__ import annotations

import json
import hashlib
import hashlib
import logging
import os
import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, Request, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from asset_index import create_note_image_record
from asset_index import create_note_image_record

MEMORY_BRIDGE_DIR = Path(__file__).resolve().parents[1] / "memory-bridge"
sys.path.insert(0, str(MEMORY_BRIDGE_DIR))
from memory_client import write_note_memory  # noqa: E402

logger = logging.getLogger("fengvoice.api")
logging.basicConfig(level=logging.INFO)

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")
DB_PATH = Path(os.getenv("FENGVOICE_DB_PATH", str(ROOT_DIR / "data" / "fengvoice.db")))
if not DB_PATH.is_absolute():
    DB_PATH = ROOT_DIR / DB_PATH
PUBLIC_DIR = ROOT_DIR / "public"
NOTE_UPLOAD_DIR = PUBLIC_DIR / "uploads" / "notes"
MAX_UPLOAD_BYTES = 5 * 1024 * 1024
NOTE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="FengVoice API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/uploads", StaticFiles(directory=PUBLIC_DIR / "uploads"), name="uploads")


class NoteInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = ""
    note_type: str = Field(default="general", max_length=50)
    tags: list[str] = Field(default_factory=list)
    status: str = Field(default="active", max_length=50)


class Note(NoteInput):
    id: str
    created_at: str
    updated_at: str


class ImageUploadResponse(BaseModel):
    url: str
    alt: str
    image_id: str
    image_id: str


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    NOTE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    with closing(connect()) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                note_type TEXT NOT NULL,
                tags TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        connection.commit()


def to_note(row: sqlite3.Row) -> Note:
    values = dict(row)
    values["tags"] = json.loads(values["tags"])
    return Note(**values)


def record_memory(note: Note, event_type: str) -> None:
    try:
        write_note_memory(note.model_dump(), event_type)
    except Exception as exc:  # Notes remain usable while EverCore is offline.
        logger.warning("EverCore memory write skipped: %s", exc)


def safe_extension(filename: str, content_type: str) -> str:
    extension = Path(filename or "").suffix.lower()
    allowed = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    if extension in allowed:
        return extension
    return {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/gif": ".gif",
        "image/webp": ".webp",
    }.get(content_type, ".png")

# Magic bytes signatures for supported image formats
_MAGIC_PNG = b"""\x89PNG\r\n\x1a\n"""
_MAGIC_JPEG = b"""\xff\xd8\xff"""
_MAGIC_WEBP_RIFF = b"RIFF"
_MAGIC_WEBP_HEADER = b"WEBP"


def detect_image_format(data: bytes) -> str | None:
    if len(data) < 4:
        return None
    if data[:8] == _MAGIC_PNG:
        return "image/png"
    if data[:3] == _MAGIC_JPEG:
        return "image/jpeg"
    if data[:4] == _MAGIC_WEBP_RIFF and len(data) >= 12 and data[8:12] == _MAGIC_WEBP_HEADER:
        return "image/webp"
    return None


def validate_upload_magic_bytes(content_type: str, data: bytes) -> str:
    detected = detect_image_format(data)
    if detected is None:
        raise HTTPException(status_code=400, detail="Uploaded file content does not match PNG, JPEG, or WebP image format")
    if detected != content_type:
        raise HTTPException(status_code=400, detail=f"Declared MIME type '{content_type}' does not match detected image format '{detected}'")
    return detected





def absolute_upload_url(request: Request, relative_path: str) -> str:
    return str(request.url_for("uploads", path=relative_path.removeprefix("/uploads/")))


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "fengvoice-api"}


@app.post("/api/uploads/images", response_model=ImageUploadResponse)
async def upload_note_image(request: Request, file: UploadFile = File(...)) -> ImageUploadResponse:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are allowed")

    first_chunk = await file.read(1024 * 1024)
    if not first_chunk:
        raise HTTPException(status_code=400, detail="Uploaded image is empty")

    detected_mime = validate_upload_magic_bytes(file.content_type, first_chunk)

    extension = safe_extension(file.filename or "", detected_mime)
    filename = f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid4().hex}{extension}"
    target = NOTE_UPLOAD_DIR / filename

    size = len(first_chunk)
    try:
        with target.open("wb") as output:
            output.write(first_chunk)
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_UPLOAD_BYTES:
                    output.close()
                    target.unlink(missing_ok=True)
                    raise HTTPException(status_code=413, detail="Image upload is limited to 5MB")
                output.write(chunk)
    finally:
        await file.close()

    if size == 0:
        target.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="Uploaded image is empty")

    relative_url = f"/uploads/notes/{filename}"
    public_url = absolute_upload_url(request, relative_url)
    record = create_note_image_record(
        file_path=target,
        public_url=public_url,
        alt="pasted image",
        source="note_paste",
        mime_type=detected_mime,
    )
    return ImageUploadResponse(url=public_url, alt="pasted image", image_id=record["image_id"])


@app.get("/api/notes", response_model=list[Note])
def list_notes(search: str = "") -> list[Note]:
    query = "SELECT * FROM notes"
    params: tuple[Any, ...] = ()
    if search:
        query += " WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?"
        term = f"%{search}%"
        params = (term, term, term)
    query += " ORDER BY updated_at DESC"
    with closing(connect()) as connection:
        return [to_note(row) for row in connection.execute(query, params).fetchall()]


@app.post("/api/notes", response_model=Note, status_code=201)
def create_note(payload: NoteInput) -> Note:
    timestamp = now_iso()
    note = Note(id=str(uuid4()), created_at=timestamp, updated_at=timestamp, **payload.model_dump())
    with closing(connect()) as connection:
        connection.execute(
            "INSERT INTO notes VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (note.id, note.title, note.content, note.note_type, json.dumps(note.tags), note.status, note.created_at, note.updated_at),
        )
        connection.commit()
    record_memory(note, "note_created")
    return note


@app.get("/api/notes/{note_id}", response_model=Note)
def get_note(note_id: str) -> Note:
    with closing(connect()) as connection:
        row = connection.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Note not found")
    return to_note(row)


@app.put("/api/notes/{note_id}", response_model=Note)
def update_note(note_id: str, payload: NoteInput) -> Note:
    existing = get_note(note_id)
    note = Note(id=existing.id, created_at=existing.created_at, updated_at=now_iso(), **payload.model_dump())
    with closing(connect()) as connection:
        connection.execute(
            """
            UPDATE notes SET title = ?, content = ?, note_type = ?, tags = ?, status = ?, updated_at = ?
            WHERE id = ?
            """,
            (note.title, note.content, note.note_type, json.dumps(note.tags), note.status, note.updated_at, note.id),
        )
        connection.commit()
    record_memory(note, "note_updated")
    return note


@app.delete("/api/notes/{note_id}", status_code=204)
def delete_note(note_id: str) -> Response:
    with closing(connect()) as connection:
        cursor = connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        connection.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return Response(status_code=204)
