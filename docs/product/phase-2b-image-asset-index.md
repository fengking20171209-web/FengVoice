# Phase 2B Image Asset Index

Phase 2B adds a structured asset index layer on top of Phase 2A's image paste upload capability.

## Background

Phase 2A implemented image paste upload: pasting an image into the notes editor uploads it and inserts
Markdown. However, Phase 2A left no structured record of which images were uploaded, where they came
from, or how to track them across storage layers.

Phase 2B solves this by recording every pasted image as an indexed asset record.

## Current Implementation

### JSONL Index

- Path: `runtime/asset-index/note-images.jsonl`
- Format: One JSON object per line (JSONL, UTF-8)
- Write strategy: append-only

### Index Record Fields

| Field | Type | Description |
|---|---|---|
| image_id | str | Unique identifier, prefixed `img_` |
| note_id | str | nullable, reserved for future note attachment |
| original_filename | str | as-stored filename |
| stored_filename | str | same as stored name |
| stored_path | str | relative path from project root |
| public_url | str | absolute URL for browser access |
| sha256 | str | hex-encoded file hash |
| mime_type | str | detected content type |
| size_bytes | int | file size |
| width | int | nullable, reserved |
| height | int | nullable, reserved |
| alt | str | alt text supplied at upload |
| source | str | source label (default: `note_paste`) |
| created_at | str | ISO 8601 UTC timestamp |

### Upload API Changes

`POST /api/uploads/images` now returns an additional field:

```json
{
  "url": "http://localhost:8000/uploads/notes/xxx.png",
  "alt": "pasted image",
  "image_id": "img_abc123"
}
```

### Frontend Changes

The `UploadedImage` type in `apps/web/src/api.ts` now includes `image_id`.

## Verification

```powershell
cd D:\Projects\FengVoice\apps\web
npm run build
npm test
```

Or run the asset index-specific test:

```powershell
node scripts/verify-image-asset-index.js
```

## Non-goals (Phase 2B)

- No COS / OneDrive / cloud storage integration
- No image management UI
- No OCR or alt-text generation
- No image deduplication via hash

## Future (Phase 2C)

- COS / OneDrive upload sync
- Asset management UI in notes editor
- Image search and retrieval
- Alt-text auto-generation
- Hash-based deduplication
