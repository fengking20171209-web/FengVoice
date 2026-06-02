# v0.3.0 Image Asset Browser Design

## Goal

Add a read-only local image asset browser and search surface in the web UI for FengVoice, building on the existing JSONL-based image asset workflow from v0.2.x.

## Background

The v0.2.x alpha releases established a complete CLI-first asset workflow:

- Paste arrow Upload arrow Index arrow Validate arrow Lookup arrow Filter arrow Migration dry-run

All asset operations are currently command-line only. The next step is to make index browsing and search available in the web UI without changing the existing upload, storage, or indexing behavior.

## Current asset workflow

1. User pastes an image into a note.
2. The web app uploads it to POST /api/uploads/images.
3. The backend stores the file under public/uploads/notes/ and appends a JSONL record to runtime/asset-index/note-images.jsonl.
4. CLI tools can validate, look up, filter, and dry-run migration against the index.
5. There is no web UI for browsing or searching indexed assets.

## Proposed user experience

### Asset browser page

A new page at /assets that displays a table or grid of indexed images. Each entry shows:

- Thumbnail (if feasible) or file type icon
- image_id
- MIME type
- File size
- Source (note_paste, etc.)
- Upload date
- Public URL (clickable)
- sha256 (truncated)

### Search and filter panel

A sidebar or top panel with:

- Text search by image_id or sha256
- MIME type dropdown filter
- Source filter
- Size range (min / max)
- Sort by date, size, or name

### Asset detail panel

Clicking a row opens a detail view with:

- Full public URL (copyable)
- Full sha256
- Upload timestamp
- All metadata fields from the JSONL record
- Link back to the note if note_id is recorded

## Data source options

### Option A: read JSONL via backend API

Add a read-only API endpoint that parses the JSONL index file and returns records.

Pros: single source of truth, live data, no duplication.

Cons: requires new API endpoint, needs to handle large indexes with pagination.

### Option B: generate static JSON from CLI

The existing find-image-asset.py CLI can produce JSON output. A scheduled or on-demand script would write a static JSON snapshot for the frontend to fetch.

Pros: no API change, frontend can fetch static JSON.

Cons: stale data, extra build step, does not scale well.

### Option C: CLI-first only, no web UI yet

Keep the current CLI-only workflow and defer the web UI to a later milestone.

Pros: no frontend work.

Cons: limits accessibility of the asset workflow.

### Recommended approach

**Option A** (backed by a light read-only API) is recommended for v0.3.0-alpha. It keeps the JSONL as the source of truth, avoids duplication, and provides a clean interface for the frontend.

## Search fields

- image_id (exact match)
- sha256 (exact match)
- source (exact match or partial)
- mime_type (exact match or dropdown)
- size_bytes (range: min/max)
- created_at (date range, if indexed)
- public_url (partial match, for finding broken URLs)

## API design draft

### GET /api/assets/images

Query parameters:

- image_id (optional)
- sha256 (optional)
- source (optional)
- mime_type (optional)
- min_size (optional)
- max_size (optional)
- limit (default: 50)
- offset (default: 0)

Response:

```json
{
  "records": [
    {
      "image_id": "img_abc123",
      "public_url": "/uploads/notes/20260602-...",
      "sha256": "e3b0c44...",
      "mime_type": "image/png",
      "size_bytes": 154320,
      "source": "note_paste",
      "created_at": "2026-06-02T..."
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### GET /api/assets/images/{image_id}

Response:

```json
{
  "image_id": "img_abc123",
  "public_url": "/uploads/notes/20260602-...",
  "sha256": "e3b0c44...",
  "mime_type": "image/png",
  "size_bytes": 154320,
  "source": "note_paste",
  "created_at": "2026-06-02T..."
}
```

### Implementation notes

- Read from the existing JSONL file at runtime/asset-index/note-images.jsonl.
- No writes to the index or runtime directory.
- Pagination uses limit/offset over the parsed in-memory records.
- The existing find-image-asset.py logic can be reused for filtering.

## Frontend design draft

### Route

- /assets

### Component structure

- AssetBrowserPage (top-level page component)
- SearchFilters (MIME dropdown, source dropdown, size inputs, text search)
- AssetTable (paginated table of records)
- AssetDetailPanel (slide-over or modal with full record)

### Data flow

1. On mount, fetch GET /api/assets/images with default sorting.
2. When filters change, re-fetch with filter parameters.
3. Clicking a row selects the record and opens the detail panel.
4. Detail panel fetches GET /api/assets/images/{image_id} for the full record.

### State

- records: list of asset records
- total: total matching count
- filters: current search/filter state
- selectedId: currently selected image_id for the detail panel
- isLoading: loading indicator

## Acceptance criteria

- /assets page loads and displays indexed images.
- Search by image_id returns matching records.
- Filter by MIME type works.
- Filter by size range works.
- Detail view shows full record metadata.
- Pagination works for indexes with more records than the page limit.
- CLI tools (validate, find, migration) still work unchanged.
- Existing upload and paste behavior is preserved.
- No runtime files are modified by the browser or API.

## Non-goals

- No cloud storage integration.
- No user accounts or permissions.
- No asset deletion from the UI.
- No batch operations.
- No image editing, cropping, or transformation.
- No automatic migration writes.
- No production deployment guarantee.
- No analytics or tracking.

## Risks

- Large JSONL files may cause slow initial load on the API. Mitigation: add limit/offset pagination and consider streaming reads for very large indexes.
- The JSONL file may contain malformed lines. The API should skip malformed records gracefully with a warning log.
- Runtime index paths differ across machines. The API should resolve paths relative to the project root or use a configurable path.
- Future metadata fields should not break existing readers. The JSONL records are append-only and forward-compatible by design.

## Implementation phases

### Phase 1: read-only API endpoint

- Add GET /api/assets/images and GET /api/assets/images/{image_id} to the backend.
- Reuse filtering logic from find-image-asset.py.
- Add basic pagination.
- No frontend changes yet.
- Add API tests.

### Phase 2: browser UI

- Add /assets route to the web app.
- Build the asset browser page with a table view.
- Implement search and filter controls.
- Wire up pagination.

### Phase 3: detail view

- Add slide-over or modal for the selected record.
- Show full record metadata.
- Add a copyable public URL link.

### Phase 4: screenshot and demo polish

- Capture screenshots of the new UI.
- Update docs/demo-image-asset-workflow.md with screenshots.
- Update docs/assets/demo/README.md checklist.
