# Image Asset Workflow Demo

This demo shows the current local-first image asset workflow in FengVoice, from pasting an image into a note to validating and managing the image asset index.

## Workflow

1. Create or open a note
2. Paste an image into the note editor
3. Upload the image through the local API
4. Insert Markdown image URL into the note
5. Append image metadata to the JSONL asset index
6. Validate the asset index
7. Look up image records by `image_id` or `sha256`
8. Filter image records by metadata (`source`, `mime_type`, `size_bytes`)
9. Run migration dry-run for existing uploaded images

## Prerequisites

- Python 3.12+
- Node.js 22+
- FengVoice API and web app running locally

## Step-by-step demo

### 1. Start services

Start the API and web app:

```powershell
# Terminal 1: API server
cd D:\Projects\FengVoice\services\api
python -m uvicorn main:app --reload --port 8777

# Terminal 2: Web app
cd D:\Projects\FengVoice\apps\web
npm run dev
```

### 2. Create a note

```powershell
curl -X POST http://localhost:8777/api/notes \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Demo note\", \"content\": \"\", \"note_type\": \"general\", \"tags\": [\"demo\"], \"status\": \"active\"}"
```

Expected response (truncated):

```json
{
  "id": "uuid-here",
  "title": "Demo note",
  "content": "",
  "created_at": "2026-...",
  "updated_at": "2026-..."
}
```

### 3. Paste an image into the note

In the web app, open the note and paste an image (e.g. Win+Shift+S screenshot, Ctrl+V). The web app will:

1. Detect the paste event
2. Upload the image to `POST /api/uploads/images`
3. Insert a Markdown image URL at the cursor position

The resulting Markdown content looks like:

```markdown
![pasted image](/uploads/notes/20260602-123456-abcdef123456.png)
```

### 4. Confirm the uploaded image URL

The uploaded image is accessible at the public URL. Use the URL from the previous step:

```powershell
curl -I http://localhost:8777/uploads/notes/20260602-123456-abcdef123456.png
```

Expected HTTP response: `200 OK` with an `image/png` content type.

### 5. Inspect the JSONL asset index

Each upload appends a JSONL record to the image asset index:

```powershell
cat runtime/asset-index/note-images.jsonl
```

Each line is a JSON record like:

```json
{
  "image_id": "img_a1b2c3d4e5f6",
  "original_filename": "20260602-123456-abcdef123456.png",
  "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "mime_type": "image/png",
  "size_bytes": 154320,
  "source": "note_paste",
  "created_at": "2026-...",
  "public_url": "/uploads/notes/20260602-123456-abcdef123456.png"
}
```

### 6. Validate the asset index

```powershell
python scripts/validate-image-asset-index.py
```

Expected output (clean index):

```
Image Asset Index Validation

Index: runtime/asset-index/note-images.jsonl
Total lines: 1
Valid records: 1
Invalid records: 0
Duplicate image_id: 0
Duplicate sha256: 0

Result: PASS
```

With JSON output:

```powershell
python scripts/validate-image-asset-index.py --json
```

```json
{
  "index": "runtime/asset-index/note-images.jsonl",
  "total_lines": 1,
  "valid_records": 1,
  "invalid_records": 0,
  "duplicate_image_id": 0,
  "duplicate_sha256": 0,
  "result": "PASS"
}
```

### 7. Look up an image asset

By `image_id`:

```powershell
python scripts/find-image-asset.py --image-id img_a1b2c3d4e5f6
```

```
Records found: 1
image_id: img_a1b2c3d4e5f6
sha256: e3b0c44...
mime_type: image/png
size_bytes: 154320
source: note_paste
```

By `sha256`:

```powershell
python scripts/find-image-asset.py --sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

With JSON output:

```powershell
python scripts/find-image-asset.py --image-id img_a1b2c3d4e5f6 --json
```

### 8. Filter image assets

By source:

```powershell
python scripts/find-image-asset.py --source note_paste
```

By MIME type:

```powershell
python scripts/find-image-asset.py --mime-type image/png --json
```

By file size range:

```powershell
python scripts/find-image-asset.py --min-size 100 --max-size 500000
```

### 9. Run migration dry-run

After uploading images over time, check for index consistency:

```powershell
python scripts/migrate-existing-note-images.py
```

Expected output for a consistent index:

```
Image Migration Dry Run

Uploads: public/uploads/notes
Index: runtime/asset-index/note-images.jsonl

Uploaded files scanned: 5
Existing index records: 5
Missing index records: 0
Duplicate sha256 in index: 0
Duplicate image_id in index: 0
Broken public_url records: 0
Malformed index lines: 0

Result: PASS
No files were modified.
```

With JSON output:

```powershell
python scripts/migrate-existing-note-images.py --json
```

## Validation commands

Run all verification scripts to confirm the project is healthy:

```powershell
cd D:\Projects\FengVoice

python scripts/verify-image-migration-dry-run.py
python scripts/verify-upload-security-constraints.py
python scripts/verify-image-asset-index-validation.py
python scripts/verify-find-image-asset.py

cd D:\Projects\FengVoice\apps\web
npm.cmd run build
npm.cmd run test:image-paste

cd D:\Projects\FengVoice
node scripts/verify-image-asset-index.js
node scripts/verify-image-paste-upload.js
```

## Current limitations

- Screenshots for this demo will be added in a follow-up update
- Magic bytes validation was added in v0.2.1-alpha but the security verification script on this branch does not yet check for it
- The project is in early alpha and is not production-ready

## Related releases

| Release | Description |
|---------|-------------|
| v0.1.0-alpha | Note image paste upload and JSONL asset index |
| v0.1.1-alpha | Maintainer workflow and OSS review readiness |
| v0.2.0-alpha | Asset index validation, lookup, and metadata filters |
| v0.2.1-alpha | Upload security hardening with magic bytes validation |
| v0.2.2-alpha | Image asset migration dry-run |


## Screenshots

The current demo is command-output based.

The following screenshots should be added when a local browser session is available. See the [screenshot checklist](assets/demo/README.md) for capture instructions.

| Screenshot | Purpose |
|------------|---------|
| 01-note-editor.png | Show the note editor with a blank or existing note |
| 02-pasted-image-markdown.png | Show pasted image Markdown URL in the editor |
| 03-uploaded-image-url.png | Confirm the uploaded image is accessible at its public URL |
| 04-jsonl-index.png | Show a JSONL asset index record |
| 05-validate-cli.png | Show validate-image-asset-index.py output |
| 06-lookup-filter-cli.png | Show find-image-asset.py lookup and filter output |
| 07-migration-dry-run.png | Show migrate-existing-note-images.py output |

