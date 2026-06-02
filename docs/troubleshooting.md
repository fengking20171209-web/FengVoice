# Local Development Troubleshooting

## Overview

This guide covers common local development problems for FengVoice contributors.
It focuses on the API service, web app, image paste upload flow, JSONL image
asset index, GitHub Actions, runtime files, and Windows-specific Git issues.

Before debugging a specific problem, confirm the repository is on the expected
branch and that generated local files are not staged:

```powershell
git status --short
```

## API Service Issues

### Port 8000 Is Already in Use

- Symptom: `uvicorn` fails to start, or the health endpoint does not respond as
  expected.
- Cause: another local process is already using port `8000`.
- Fix: stop the existing process or start the API on another port:

```powershell
cd services/api
uvicorn main:app --reload --port 8001
```

If you change the API port, make sure the web app configuration or local API
URL expectations match that port.

### Python Dependency Is Missing

- Symptom: the API or verification script fails with `ModuleNotFoundError`.
- Cause: the local Python environment has not installed the API dependencies.
- Fix: activate the intended virtual environment and install the requirements:

```powershell
cd services/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### FastAPI TestClient Requires httpx

- Symptom: verification fails with a message similar to
  `The starlette.testclient module requires the httpx package to be installed`.
- Cause: Starlette's `TestClient` depends on `httpx`, and a fresh environment
  may not have it installed.
- Fix: install `httpx` in the Python environment used by the verification
  scripts:

```powershell
python -m pip install httpx
```

GitHub Actions also installs `httpx` explicitly before running the image upload
verification scripts.

## Web App Issues

### Port 5173 Is Already in Use

- Symptom: Vite reports that port `5173` is unavailable or starts on a different
  port.
- Cause: another dev server is already running.
- Fix: stop the other process or choose a specific available port:

```powershell
cd apps/web
npm run dev -- --host 0.0.0.0 --port 3000
```

### npm install or npm ci Fails

- Symptom: dependency installation fails in `apps/web`.
- Cause: Node.js version mismatch, corrupted `node_modules`, or stale lockfile
  state.
- Fix: use the web app directory and reinstall dependencies:

```powershell
cd apps/web
npm ci
```

If local state is corrupted, remove `node_modules` from `apps/web` and run
`npm ci` again. Do not commit `node_modules`.

### Vite Dev Server Starts but API Calls Fail

- Symptom: the web app loads, but note or upload API calls fail.
- Cause: the API service is not running, is using a different port, or CORS/API
  URL expectations do not match the local setup.
- Fix: start the API service and confirm the health endpoint:

```powershell
cd services/api
uvicorn main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/health
```

## Image Paste Upload Issues

### Pasted Image Does Not Appear in the Note

- Symptom: pasting an image does not insert Markdown into the note editor.
- Cause: the clipboard item may not be an image, the upload request failed, or
  the API service is not reachable.
- Fix: confirm the API is running, then run the image paste verification:

```powershell
cd apps/web
npm.cmd run test:image-paste
```

### Uploaded Image URL Returns 404

- Symptom: the note contains an image URL, but the browser returns `404`.
- Cause: the uploaded file is not present under the local uploads directory, or
  the API static files mount is not serving the expected path.
- Fix: confirm the API service that handled the upload is still running and that
  local uploaded files have not been deleted. Uploaded files are local runtime
  data and are not committed to git.

## Image Asset Index Issues

### note-images.jsonl Is Not Created

- Symptom: `runtime/asset-index/note-images.jsonl` is missing after an image
  upload.
- Cause: no successful image upload has occurred, or the runtime directory was
  deleted between runs.
- Fix: run the asset index verification:

```powershell
cd D:\Projects\FengVoice
node scripts/verify-image-asset-index.js
```

### Validate the JSONL asset index

- Symptom: maintainers need to check whether
  `runtime/asset-index/note-images.jsonl` contains malformed lines, missing
  fields, invalid values, or duplicate records.
- Cause: the asset index is append-only local runtime data, so manual edits,
  repeated local tests, or interrupted workflows can leave records that need
  review.
- Fix: run the standalone validator:

```powershell
cd D:\Projects\FengVoice
python scripts/validate-image-asset-index.py
```

For machine-readable output:

```powershell
python scripts/validate-image-asset-index.py --json
```

To validate a specific JSONL file:

```powershell
python scripts/validate-image-asset-index.py --index runtime/asset-index/note-images.jsonl
```

### image_id Is Missing from Upload Response

- Symptom: the upload API response includes a URL but no `image_id`.
- Cause: the backend response model or asset index integration is not the
  expected alpha version.
- Fix: confirm the local checkout is up to date and run:

```powershell
cd D:\Projects\FengVoice
python scripts/verify-image-asset-index-validation.py
python scripts/validate-image-asset-index.py --json
node scripts/verify-image-asset-index.js
```

## Runtime Files and Git

### runtime/ or public/uploads/ Appears in git status

- Symptom: generated runtime files or uploaded images appear in `git status`.
- Cause: generated local data was created in a path not covered by `.gitignore`,
  or git status is showing untracked files before ignore rules were updated.
- Fix: do not commit generated files. Confirm `.gitignore` contains:

```text
runtime/
public/uploads/
```

Then check status again:

```powershell
git status --short
```

## GitHub Actions Issues

### CI Fails with Missing httpx

- Symptom: GitHub Actions fails during image paste or asset index verification
  with `ModuleNotFoundError: No module named 'httpx'`.
- Cause: a fresh CI Python environment does not include Starlette TestClient's
  `httpx` dependency unless it is installed.
- Fix: keep the workflow step that installs API requirements and `httpx` before
  running the Node verification scripts.

### CI Fails Because npm Commands Run in the Wrong Directory

- Symptom: `npm` reports that it cannot find `package.json`.
- Cause: the repository root does not contain `package.json`; the web package
  lives in `apps/web`.
- Fix: run web commands from `apps/web`:

```powershell
cd apps/web
npm.cmd run build
npm.cmd run test:image-paste
```

## Windows-Specific Issues

### git-remote-https.exe Crashes

- Symptom: Windows shows an application error for `git-remote-https.exe` during
  a Git push, pull, or fetch over HTTPS.
- Cause: this is usually a Git for Windows HTTPS transport issue, not a
  FengVoice code problem.
- Safe recovery:
  - Close the Windows error dialog.
  - Do not repeatedly retry the same push in a loop.
  - Check whether the remote operation already succeeded:

```powershell
git status --short
git log --oneline -5
gh pr view
```

  - If the problem repeats, upgrade Git for Windows or use SSH if an SSH key is
    already configured:

```powershell
git --version
winget upgrade --id Git.Git -e
```

## Verification Commands

Use these commands after documentation, CI, or upload-related changes:

```powershell
cd D:\Projects\FengVoice\apps\web
npm.cmd run build
npm.cmd run test:image-paste

cd D:\Projects\FengVoice
node scripts/verify-image-asset-index.js
```
