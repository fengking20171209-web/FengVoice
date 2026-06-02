# v0.2.0 Roadmap: Local Asset Workflow

This roadmap describes planned work for `v0.2.0-alpha`. It is intentionally
limited to local-first asset management improvements and does not promise cloud
sync, collaboration, or large media pipelines.

## Goal

Make pasted image assets easier to find, validate, and migrate while preserving
the current local-first workflow.

## Scope

### Asset Search by `image_id`

- Add a way to look up an uploaded image record by its stable `image_id`.
- Return the stored URL, MIME type, size, hash, and creation metadata.
- Keep the existing upload response compatible.

### Metadata Filters

- Add filters for common asset index fields such as MIME type, created date, and
  note association when available.
- Keep filtering read-only for the alpha release.

### Image Index Validation Command

- Add a command that checks JSONL syntax, required fields, duplicate
  `image_id` values, missing files, and hash mismatches.
- Report actionable errors without modifying files by default.

### Migration Script

- Add a script for indexing existing uploaded images that predate the asset
  index.
- Require a dry-run mode before writing records.

### Local-First Asset Workflow Polish

- Improve documentation for runtime data location, git safety, and backup
  expectations.
- Add troubleshooting steps for local upload and asset index failures.

## Non-Goals

- No cloud storage integration in `v0.2.0-alpha`.
- No account system or multi-user permissions.
- No destructive cleanup command for uploaded files.
- No automatic migration without a dry run.

## Acceptance Criteria

- Maintainers can look up an image record by `image_id`.
- Maintainers can validate the JSONL asset index from the command line.
- Existing uploaded images can be previewed in a dry-run migration report.
- README or demo docs explain the asset workflow in terms a new contributor can
  follow.
- CI or local verification covers the new validation command.

## Risks

- JSONL records may reference files that were manually deleted.
- Runtime data paths may differ across developer machines.
- Migration code could accidentally index temporary or unsupported files if the
  input directory is not constrained.
- Future metadata fields should not make existing alpha records unreadable.
