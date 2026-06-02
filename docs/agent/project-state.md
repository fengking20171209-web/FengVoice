# FengVoice Project State

## Current status

FengVoice is an early-stage alpha OSS project.

Current releases: v0.1.0-alpha through v0.2.2-alpha.

## Releases

| Release | Description |
|---------|-------------|
| v0.1.0-alpha | Note image paste upload and JSONL asset index |
| v0.1.1-alpha | Maintainer workflow and OSS review readiness |
| v0.2.0-alpha | Asset index validation, lookup, and metadata filters |
| v0.2.1-alpha | Upload security hardening with magic bytes validation |
| v0.2.2-alpha | Image asset migration dry-run |

## Completed workflow

- Note image paste upload
- Stable image_id generation
- JSONL image asset index with sha256
- Asset index validation CLI
- Image lookup by image_id and sha256
- Metadata filters (source, mime_type, size_bytes)
- Upload endpoint security review
- Magic bytes validation for PNG, JPEG, WebP
- Real MIME type recorded in JSONL asset index
- Migration dry-run CLI for existing images
- Image asset workflow demo document
- Codex operating instructions (AGENTS.md, docs/agent/)
- CI / verification suite

## Open issues

- Issue #12: roadmap polish (in progress)

## Closed issues

All prior issues: #13, #11, #9, #8, #6, #5, #19, #10, #4 are closed.

## Current milestone

v0.2.2-alpha completed. Next: v0.3.0-alpha.

## Known limitations

- Screenshots not yet added to demo document
- Migration --apply mode is not implemented
- No web UI asset browser
- CLI-first search
- Local Git on Windows has shown HTTPS/lock instability
- Project remains early-stage alpha

## Maintainer strategy

Keep changes small and reviewable.

Prefer:
- one issue per PR
- one capability per release
- green CI before merge
- honest known limitations

## Related docs

- AGENTS.md in project root
- docs/agent/next-actions.md
- docs/agent/operating-loop.md
- docs/agent/git-recovery.md
- ROADMAP.md
