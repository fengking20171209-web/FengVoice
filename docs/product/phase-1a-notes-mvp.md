# Phase 1A: Notes MVP

## Implemented

- FastAPI health endpoint
- SQLite-backed Notes CRUD API
- Vite React TypeScript web interface
- Notes list, create, edit, delete, and local search
- Best-effort EverCore memory writes after note creation and update
- Lightweight Docker Compose services for API and web

## Start locally

API:

```powershell
cd services/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Web:

```powershell
cd apps/web
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

Docker:

```powershell
docker compose up --build
```

## API

- `GET /health`
- `GET /api/notes`
- `POST /api/notes`
- `GET /api/notes/{id}`
- `PUT /api/notes/{id}`
- `DELETE /api/notes/{id}`

## API smoke test

```powershell
curl.exe http://localhost:8000/health
$note = curl.exe -s -X POST http://localhost:8000/api/notes -H "Content-Type: application/json" -d '{\"title\":\"Phase 1A\",\"content\":\"Notes MVP smoke test\",\"note_type\":\"engineering\",\"tags\":[\"mvp\"],\"status\":\"active\"}' | ConvertFrom-Json
curl.exe http://localhost:8000/api/notes
curl.exe -X PUT "http://localhost:8000/api/notes/$($note.id)" -H "Content-Type: application/json" -d '{\"title\":\"Phase 1A updated\",\"content\":\"Notes MVP smoke test updated\",\"note_type\":\"engineering\",\"tags\":[\"mvp\",\"verified\"],\"status\":\"active\"}'
curl.exe -X DELETE "http://localhost:8000/api/notes/$($note.id)"
```

## EverCore strategy

The API reads `EVEROS_BASE_URL`, `EVEROS_MEMORY_PATH`, and optional `EVEROS_API_TOKEN` from the environment. Create and update operations attempt to send a memory event. Any EverCore failure is logged as a warning and does not block the Notes API response.

## Known limitations

- SQLite is intended for the MVP and lightweight test deployment.
- Authentication and permissions are intentionally deferred.
- EverCore memory search is not included yet.
- Search is local in the web interface and basic `LIKE` matching in the API.

## Next

- Notes categories, pinning, trash, and refined tags
- Tencent Cloud test deployment with Nginx and HTTPS
- Selective migration of Prompt Forge and image asset capabilities

