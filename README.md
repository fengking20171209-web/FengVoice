# FengVoice

FengVoice is an incremental content and voice production workspace. Phase 1A provides a lightweight Notes MVP and an optional EverCore memory write bridge.

## Quick start

### API

```powershell
cd services/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Web

```powershell
cd apps/web
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

Open `http://localhost:3000`. The API health endpoint is `http://localhost:8000/health`.

### Docker Compose

```powershell
docker compose up --build
```

See [docs/product/phase-1a-notes-mvp.md](docs/product/phase-1a-notes-mvp.md) for API details and curl examples.

