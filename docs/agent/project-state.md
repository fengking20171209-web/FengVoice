# FengVoice Project State

## Current status

FengVoice is an early-stage alpha OSS project.

Current HEAD: 59eeb94 feat: add metadata filters for image asset lookup

## Releases

| Release | Description |
|---------|-------------|
| v0.1.0-alpha | note image paste upload and JSONL asset index |
| v0.1.1-alpha | maintainer workflow and OSS review readiness |
| v0.2.0-alpha | image asset lookup and validation workflow |

## Completed workflow

- image paste upload
- JSONL asset indexing
- asset index validation CLI
- asset lookup by image_id
- asset lookup by sha256
- metadata filters (source, mime_type, size_bytes)
- upload endpoint security review
- troubleshooting docs
- README quick start improvements

## Current milestone

v0.2.0-alpha

## Open issues to prioritize

1. Issue #19 security: add magic bytes validation for uploaded images
2. Issue #10 feature: add migration tool for existing uploaded images
3. Issue #4 docs: add screenshots for image paste workflow
4. Issue #12 roadmap: plan v0.2.0 local asset workflow
5. Issue #7 maintenance: add release checklist for alpha versions

## Closed issues

Issues #13, #11, #9, #8, #6, #5 are closed.

## Known limitations

- Magic bytes validation is not implemented yet.
- MIME consistency still needs review.
- Local Git on Windows has shown HTTPS / lock instability.
- Project remains early-stage alpha.

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
