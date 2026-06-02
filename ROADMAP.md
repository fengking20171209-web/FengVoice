# FengVoice Public Roadmap

> Last updated: 2026-06-02

## Releases

| Release | Description |
|---------|-------------|
| v0.1.0-alpha | Note image paste upload and JSONL asset index |
| v0.1.1-alpha | Maintainer workflow and OSS review readiness |
| v0.2.0-alpha | Asset index validation, lookup, and metadata filters |
| v0.2.1-alpha | Upload security hardening with magic bytes validation |
| v0.2.2-alpha | Image asset migration dry-run |

## Completed capabilities

- Note image paste upload
- Stable image_id generation
- JSONL image asset index with sha256
- Asset index validation CLI (validate-image-asset-index.py)
- Image lookup by image_id and sha256 (find-image-asset.py)
- Metadata filters by source, mime_type, size_bytes
- Upload endpoint security review
- Magic bytes validation for PNG, JPEG, WebP
- Migration dry-run for existing uploaded images (migrate-existing-note-images.py)
- Image asset workflow demo document
- Codex operating instructions (AGENTS.md, docs/agent/)
- CI / verification suite for asset index, lookup, paste upload, and security constraints

## Current limitations

- Screenshots are not yet included in the demo document
- Migration --apply mode is not implemented
- No web UI asset browser yet
- Asset search is CLI-first, not web UI
- No cloud storage or multi-user support
- Project remains early-stage alpha

## Next milestone: v0.3.0-alpha

### Direction

Local image asset browser and search surface.

### Candidate scope

- Web UI for browsing indexed uploaded images
- Search by image_id
- Search and filter by metadata
- Display public URL, MIME type, size, and sha256
- Link image records back to notes (if note_id support is added)
- Keep CLI workflow as fallback

### Candidate non-goals

- No production deployment guarantee
- No cloud storage requirement
- No external user analytics
- No automatic migration writes (--apply reserved for future design)
- No destructive changes to runtime/ or public/uploads/

## Earlier phases

- Phase 0: Repository and service foundation
- Phase 1A: Notes MVP with CRUD API, React UI, memory bridge
- Phase 1B: Notes UI organization and polish
- Phase 2A: Image paste upload
- Phase 2B: Image asset index (SHA-256, JSONL)
- Phase 2C: Prompt and asset migration tooling (partial)
