# v0.2.x Roadmap: Local Asset Workflow

This roadmap describes the local-first asset management work completed across the v0.2.x alpha cycle.

## Goal

Make pasted image assets easier to find, validate, and migrate while preserving the current local-first workflow.

## Completed

### Asset Search by image_id (v0.2.0-alpha)

- Script: scripts/find-image-asset.py with --image-id flag
- Returns stored URL, MIME type, size, sha256, and creation metadata
- Existing upload response preserved

### Sha256 Lookup (v0.2.0-alpha)

- Search by --sha256 in find-image-asset.py
- Duplicate sha256 detection in validate-image-asset-index.py

### Metadata Filters (v0.2.0-alpha)

- Filters for source, mime_type, and size_bytes
- Read-only; does not modify index records

### Image Index Validation CLI (v0.2.0-alpha)

- Script: scripts/validate-image-asset-index.py
- Checks JSONL syntax, required fields, duplicate image_id, duplicate sha256
- Actionable error output without modifying files

### Upload Security Review (v0.2.0-alpha)

- Security constraint verification script (verify-upload-security-constraints.py)
- documented in docs/security-upload-review.md

### Magic Bytes Validation (v0.2.1-alpha)

- Server-side content verification for PNG, JPEG, and WebP
- MIME mismatch rejection with clear error messages
- Real MIME type recorded in JSONL asset index

### Migration Dry-Run (v0.2.2-alpha)

- Script: scripts/migrate-existing-note-images.py
- Dry-run only; no file writes
- Reports missing records, duplicate sha256, duplicate image_id, broken URLs, malformed lines

### Demo Documentation (merged post-v0.2.2)

- docs/demo-image-asset-workflow.md
- Command-output style demo for the full asset workflow

## Current limitations

- Screenshots are pending
- Migration --apply mode is not implemented
- No web UI asset browser
- Search is CLI-first
- Runtime is local-only

## Current asset workflow

Paste arrow Upload arrow Index arrow Validate arrow Lookup arrow Filter arrow Migration dry-run

## Completed sub-tasks

- image paste upload
- stable image_id generation
- JSONL image asset index
- asset index validation CLI
- image lookup by image_id and sha256
- metadata filters
- upload endpoint security review
- magic bytes validation
- migration dry-run
- demo documentation
- Codex operating instructions

## v0.3.0-alpha direction

The next milestone targets a local image asset browser and search surface in the web UI.

See ROADMAP.md for details.
