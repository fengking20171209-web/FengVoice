# FengVoice Public Roadmap

> Last updated: 2026-06-05

## Releases

| Release | Description |
|---------|-------------|
| v0.1.0-alpha | Note image paste upload and JSONL asset index |
| v0.1.1-alpha | Maintainer workflow and OSS review readiness |
| v0.2.0-alpha | Asset index validation, lookup, and metadata filters |
| v0.2.1-alpha | Upload security hardening with magic bytes validation |
| v0.2.2-alpha | Image asset migration dry-run |
| v0.3.0-alpha | Historical Gitee-side audio experiment tag |
| v0.3.1-alpha | Audio note capture on the GitHub mainline |

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
- Audio note upload backend API
- Separate audio JSONL index
- Minimal browser audio recording UI
- Uploaded audio link insertion in notes
- Image asset workflow demo document
- Codex operating instructions (AGENTS.md, docs/agent/)
- CI / verification suite for asset index, lookup, paste upload, and security constraints

## Current limitations

- Screenshots are not yet included in the demo document
- Migration --apply mode is not implemented
- No web UI asset browser yet
- Asset search is CLI-first, not web UI
- Audio recording UI is intentionally minimal
- No transcript or advanced audio library workflow yet
- No cloud storage or multi-user support
- Project remains early-stage alpha

## Next milestone: deployable alpha baseline

### Direction

Tencent Cloud deployment preparation and a small read-only asset API restarted
from clean `origin/main`.

### Candidate scope

- Deployment runbook and Docker readiness review
- API and web startup verification from the v0.3.1-alpha baseline
- Read-only image/audio asset API design from a clean branch
- Preserve image paste, audio upload, JSONL append, and existing validation
  workflows
- Keep CLI workflow as fallback for asset lookup

### Candidate non-goals

- No production deployment guarantee
- No cloud storage requirement
- No external user analytics
- No automatic migration writes (--apply reserved for future design)
- No destructive changes to runtime/ or public/uploads/
- No transcript feature in this milestone

## Earlier phases

- Phase 0: Repository and service foundation
- Phase 1A: Notes MVP with CRUD API, React UI, memory bridge
- Phase 1B: Notes UI organization and polish
- Phase 2A: Image paste upload
- Phase 2B: Image asset index (SHA-256, JSONL)
- Phase 2C: Prompt and asset migration tooling (partial)
