from __future__ import annotations

import json
import logging
import os
import sqlite3
import sys
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

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

app = FastAPI(title="FengVoice API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
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


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "fengvoice-api"}


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
