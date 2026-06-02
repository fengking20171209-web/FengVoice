# Upload Endpoint Security Review

## Scope

This review covers the current note image upload endpoint and related local
asset handling in FengVoice. It focuses on upload size, MIME validation,
filename handling, runtime file safety, public URL exposure, JSONL asset index
write safety, and verification coverage.

Reviewed files:

- `services/api/main.py`
- `services/api/asset_index.py`
- `.gitignore`
- `scripts/verify-image-paste-upload.js`
- `scripts/verify-image-asset-index.js`
- `scripts/verify-upload-security-constraints.py`

## Current Behavior

The upload endpoint accepts note image uploads through
`POST /api/uploads/images`. Uploaded files are stored under
`public/uploads/notes/`, served through the local `/uploads` static mount, and
recorded in the JSONL image asset index under `runtime/asset-index/`.

The endpoint currently:

- rejects non-`image/*` content types
- enforces a `5MB` upload size limit while streaming file chunks
- generates stored filenames with timestamp plus UUID content
- removes oversized or empty upload files
- returns a public URL and stable `image_id`
- appends an asset index record containing `sha256`, `source`, and runtime path

## Findings

| Area | Status | Risk | Recommendation |
|---|---|---|---|
| Upload size limit | PASS | Large uploads are capped at `5MB`. | Keep the current limit documented and covered by tests. |
| MIME type validation | WARN | The endpoint checks `file.content_type.startswith("image/")`, which depends on client-provided metadata. | Add magic bytes validation in a future PR before broadening upload workflows. |
| Filename handling | PASS | Stored filenames are generated with timestamp and UUID content instead of trusting user filenames. | Keep user-provided names out of final storage paths. |
| Runtime file safety | PASS | `.gitignore` excludes both `runtime/` and `public/uploads/`. | Continue treating uploaded files and local indexes as runtime data. |
| Public URL exposure | PASS | Returned URLs are constrained to `/uploads/notes/<generated-file>`. | Keep upload paths constrained to the notes upload directory. |
| JSONL index write safety | PASS | Asset index records are append-only and include `sha256`, `image_id`, and `source`. | Use the validation CLI to inspect malformed or duplicate records. |
| Asset index MIME recording | WARN | `asset_index.py` currently records `mime_type` as `image/png` regardless of uploaded content type. | Track the actual upload content type in a future metadata PR. |
| CI / test coverage | PASS | Upload and asset index verification scripts exist, and this PR adds a lightweight security constraint check. | Keep CI running the verification scripts on every PR. |

## Verified Safeguards

- `.gitignore` excludes `runtime/`.
- `.gitignore` excludes `public/uploads/`.
- The upload endpoint defines `MAX_UPLOAD_BYTES`.
- Oversized uploads are rejected with `413`.
- Non-image uploads are rejected with `400`.
- Stored filenames use generated values and do not rely on raw user filenames.
- Uploaded files are constrained to `NOTE_UPLOAD_DIR`.
- Public URLs are generated under `/uploads/notes/`.
- Empty or oversized uploads are removed.
- Upload responses include `image_id`.
- JSONL records include `sha256`.
- JSONL records are appended to the asset index.
- JSONL records include `source="note_paste"`.

## Known Limitations

- MIME validation does not inspect magic bytes yet.
- The asset index currently stores a fixed `image/png` MIME value instead of the
  actual upload content type.
- The upload endpoint is intended for local alpha use and does not yet include
  production-grade malware scanning, per-user quotas, authentication, or
  retention policies.

## Follow-up Issues

Recommended follow-up issues:

- Add magic bytes validation for uploaded image files.
- Store actual uploaded MIME type in JSONL asset index records.
- Add tests for supported image extensions and unsupported image-like metadata.
- Document local upload retention and cleanup expectations.

## Validation Commands

```powershell
cd D:\Projects\FengVoice

python scripts/verify-upload-security-constraints.py
python scripts/verify-image-asset-index-validation.py
python scripts/validate-image-asset-index.py --json

cd D:\Projects\FengVoice\apps\web
npm.cmd run build
npm.cmd run test:image-paste

cd D:\Projects\FengVoice
node scripts/verify-image-asset-index.js
```
