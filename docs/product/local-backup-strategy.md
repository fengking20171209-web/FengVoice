# FengVoice Local Backup Strategy

## Why Backup Is P0

A personal notes system becomes valuable only after it contains real decisions, prompts, screenshots, audio, and learning notes. Once FengVoice is used daily, data loss becomes more damaging than a missing feature.

Backup must be treated as a P0 design concern before heavy personal use.

## Content to Back Up

| Content | Path | Why |
| --- | --- | --- |
| SQLite database | `data/fengvoice.db` | Main note data. |
| Asset index | `runtime/asset-index/` | JSONL metadata for image assets. |
| Uploaded files | `public/uploads/` | Pasted images and future local media files. |
| Vault notes | `vault/` | Local knowledge/project notes when present. |
| Product templates | `docs/product/templates/` | Personal note and prompt templates. |

## Current Stage: Design Only

This document does not execute backup, write scripts, delete old files, or connect to sync services.

Any future backup implementation should be handled as a separate, reviewable task.

## Recommended Local Backup Targets

Use at least one local or synced target outside the repo working tree:

- Another path on the D drive, for example:

```text
D:\FengVoiceBackups\
```

- OneDrive synchronized directory.
- Baidu Netdisk synchronized directory.

The backup target should not be inside `D:\Projects\FengVoice` to avoid accidental Git staging.

## Backup Package Naming

Use timestamped zip archives:

```text
fengvoice_backup_YYYYMMDD-HHMMSS.zip
```

Example:

```text
fengvoice_backup_20260606-213000.zip
```

## Recommended Backup Manifest

A future backup package should include a manifest such as:

```json
{
  "created_at": "2026-06-06T21:30:00+08:00",
  "source": "D:/Projects/FengVoice",
  "included": [
    "data/fengvoice.db",
    "runtime/asset-index/",
    "public/uploads/",
    "vault/",
    "docs/product/templates/"
  ],
  "notes": "Local personal-notes backup. No secrets intentionally included."
}
```

## Future One-Click Export Plan

A future script may:

1. Stop or warn about active writers.
2. Copy the SQLite DB.
3. Copy asset index JSONL files.
4. Copy uploads and templates.
5. Create a zip archive with timestamp.
6. Write a manifest.
7. Print the backup path and size.

## Safety Rules

- Do not automatically delete old backups.
- Do not include `.env`, API keys, tokens, credentials, or browser profiles.
- Do not push backup packages to Git.
- Do not assume OneDrive or Baidu Netdisk is available.
- Do not overwrite a previous backup with the same name.
- Do not perform cloud sync inside the first backup script.
