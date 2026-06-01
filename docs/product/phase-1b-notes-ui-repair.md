# Phase 1B Repair: Notes usability

## Fixed

- The new-note action now creates an optimistic local draft immediately.
- The draft appears in the list, becomes selected, and focuses the title field.
- A background POST replaces the local draft id with the server id when the API succeeds.
- API failures preserve editable local drafts and show a visible error.
- API calls are centralized in `apps/web/src/api.ts`.
- Save state, connection state, manual save, 800 ms autosave, `Ctrl+S`, and dismissible errors are visible.

## Themes

The sidebar theme control supports comfortable dark, warm gray, and light modes. The choice is stored in `localStorage` and restored after refresh.

## API base URL

The browser reads `VITE_API_BASE_URL`, defaulting to `http://localhost:8000`. Do not expose EverCore tokens or backend secrets through `VITE_` variables.

## Start

```powershell
cd services/api
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload --port 8000

cd apps/web
npm run dev -- --host 0.0.0.0 --port 3000
```

## Test

```powershell
cd apps/web
npm run build

cd ..\..\services\api
.\.venv\Scripts\python.exe -m py_compile main.py
curl.exe http://localhost:8000/health

cd ..\..
.\scripts\ops\verify_notes_ui.ps1
```

The UI verification script uses the locally installed Chrome DevTools Protocol without adding frontend dependencies. It covers online note creation, focus, autosave, refresh persistence, Chinese search, theme persistence, offline draft retention and recovery, and mobile horizontal overflow.

## Known limitations

- Offline drafts remain in the current browser session only.
- Conflict resolution across multiple browser tabs is deferred.
- Rich text, pinning, and trash are deferred.
- Docker Compose was not revalidated locally because Docker CLI is not installed on the current Windows environment.

## Next

- Add lightweight draft persistence in browser storage.
- Add categories and trash after daily-use feedback.
