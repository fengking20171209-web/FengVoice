# FengVoice Local Notes Acceptance Plan

## Purpose

This plan verifies that FengVoice can serve as a local-first personal notes workspace before more cloud, public showcase, or integration work continues.

## Safety Boundary

- Do not commit `runtime/`.
- Do not commit `public/uploads/`.
- Do not read `.env`, API keys, tokens, or credentials.
- Do not connect to Tencent Cloud, COS, MCP, or remote production systems.
- Record evidence in docs or reports only.

## Acceptance Checklist

### 1. API Startup

Command:

```powershell
cd D:\Projects\FengVoice\services\api
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Expected:

- API starts without traceback.
- `http://127.0.0.1:8000/health` responds.

### 2. Web Startup

Command:

```powershell
cd D:\Projects\FengVoice\apps\web
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

Expected:

- Web app starts.
- `http://127.0.0.1:5173/` loads.

### 3. Create First Local Note

Create a note titled:

```text
PN-1 AI 长任务复盘试用
```

Expected:

- Note appears in the note list.
- Content can be edited.

### 4. Autosave / Save Behavior

Enter several paragraphs and wait for the existing save flow.

Expected:

- Refreshing the page does not lose the note.
- Any save failure is visible or recorded as a PN-5 issue.

### 5. Search

Search for a unique phrase from the note.

Expected:

- The note is returned.
- Search behavior is fast enough for daily use.

### 6. Tags

Apply or record tags from the approved personal-notes whitelist:

```text
workflow, notes, decision, prompt, research, review, audio, image, general
```

Expected:

- Tags remain associated with the note.
- Tag behavior is documented if the current UI lacks a complete flow.

### 7. Pin

Mark a note as pinned if supported by the current UI/API.

Expected:

- Pinned note remains easy to find.
- If pinning is missing or broken, record it as a PN-5 candidate.

### 8. Trash / Recovery

Move a test note to trash and recover it if supported.

Expected:

- Trash operation does not delete unrelated notes.
- Recovery status is documented.

### 9. Prompt Template

Use `docs/product/templates/ai-long-task-review-template.md` as the manual static template.

Expected:

- The template can be copied into a note.
- Dynamic placeholders are not required in this phase.

### 10. Image Paste

Paste a small screenshot into a note.

Expected:

- Markdown image URL is inserted.
- Uploaded file is stored under local uploads.
- No uploaded file is committed.

### 11. Audio Recording / Upload

If the current app supports audio, record or upload a short local test clip.

Expected:

- Audio status is documented honestly.
- If unsupported, record as a future PN-3/PN-5 item.

### 12. Asset Index

Run the relevant asset validation after image testing:

```powershell
cd D:\Projects\FengVoice
python scripts/verify-image-asset-index-validation.py
python scripts/verify-find-image-asset.py
node scripts/verify-image-asset-index.js
```

Expected:

- Asset index validation passes, or failures are recorded with exact command output.

### 13. Notebook Mode Entry Point

Select one completed AI long-task review note.

Expected:

- The note can be summarized as a `gbrain-candidate` draft.
- No production GBrain write occurs automatically.

### 14. Local Backup / Export Check

Review the local backup strategy before heavy daily use.

Expected:

- Required backup sources are known: SQLite DB, runtime asset index, uploads, vault, and templates.
- No automatic deletion of old backups is introduced.

## PN-0 Exit Criteria

PASS when API and web start, one note can be created and recovered after reload, and local safety boundaries are preserved.

WARN when optional flows such as pinning, trash, audio, or Notebook Mode are incomplete but documented.

FAIL when note data is lost, runtime/upload files are committed, secrets are read, or remote systems are contacted.
