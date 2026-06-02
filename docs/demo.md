# FengVoice Alpha Demo

This demo explains the current `v0.1.0-alpha` workflow for local-first notes and
image asset indexing.

## Demo Goal

Show that FengVoice can capture a note, accept a pasted image, return a public
image URL for Markdown, and record a stable `image_id` in a JSONL asset index.

## Prerequisites

- API dependencies installed for `services/api`
- Web dependencies installed for `apps/web`
- Local API running on `http://localhost:8000`
- Local web app running on `http://localhost:3000`

## Steps

1. Open the web app.
2. Create or select a note.
3. Paste an image into the note editor.
4. Confirm the editor inserts Markdown similar to:

```markdown
![pasted image](http://localhost:8000/uploads/notes/example.png)
```

5. Confirm the upload API response includes:

```json
{
  "url": "http://localhost:8000/uploads/notes/example.png",
  "alt": "pasted image",
  "image_id": "img_..."
}
```

6. Confirm the JSONL asset index receives a record under:

```text
runtime/asset-index/note-images.jsonl
```

## What This Demonstrates

- A creator can paste an image while writing a note.
- FengVoice stores the image as a local uploaded asset.
- The note receives a Markdown image URL.
- The backend assigns a stable `image_id`.
- The asset index can become the foundation for future search, migration, and
  metadata workflows.

## Current Alpha Limitations

- Asset search by `image_id` is planned but not implemented yet.
- Metadata filters are planned for `v0.2.0`.
- Uploaded files and runtime indexes are local development data and should not
  be committed to git.
