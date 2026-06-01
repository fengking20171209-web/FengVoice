from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

logger = logging.getLogger('fengvoice.asset_index')

ROOT_DIR = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT_DIR / 'runtime'
INDEX_DIR = RUNTIME_DIR / 'asset-index'
INDEX_FILE = INDEX_DIR / 'note-images.jsonl'


def ensure_dirs() -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)


def _next_image_id() -> str:
    return f'img_{uuid4().hex}'


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def create_note_image_record(
    *,
    file_path: Path,
    public_url: str,
    alt: str,
    source: str = 'note_paste',
    note_id: str | None = None,
) -> dict:
    ensure_dirs()
    image_id = _next_image_id()
    stat = file_path.stat()
    record = {
        'image_id': image_id,
        'note_id': note_id,
        'original_filename': file_path.name,
        'stored_filename': file_path.name,
        'stored_path': str(file_path.relative_to(ROOT_DIR)),
        'public_url': public_url,
        'sha256': _sha256(file_path),
        'mime_type': 'image/png',
        'size_bytes': stat.st_size,
        'width': None,
        'height': None,
        'alt': alt,
        'source': source,
        'created_at': datetime.now(timezone.utc).isoformat(),
    }
    with INDEX_FILE.open('a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')
    logger.info('Asset index record created: %s', image_id)
    return record
