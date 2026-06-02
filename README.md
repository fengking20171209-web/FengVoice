# FengVoice

FengVoice is an early-stage, local-first platform for organizing AI-generated
content and note-linked image assets.

The current alpha release focuses on a practical creator workflow:

- paste images directly into notes
- upload pasted images through the local API
- create an append-only JSONL asset index
- return stable image IDs for future search, tagging, and retrieval

## Features

- **Notes CRUD** -- create, read, update, delete notes with tags and status
- **Image paste upload** -- paste images directly into notes, served as
  absolute URLs
- **Image asset index** -- SHA-256 content-addressed index (JSONL) for
  deduplication and traceability
- **Memory bridge** (optional) -- best-effort EverCore memory integration
  without blocking note operations

## Quick Start

FengVoice currently runs as a local `v0.1.x-alpha` workspace with two
independent services:

- API service: `services/api`
- Web app: `apps/web`

### 1. Start the API

Run the API from the `services/api` directory:

```powershell
cd services/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

The API health endpoint is:

```text
http://127.0.0.1:8000/health
```

### 2. Start the Web App

Run the web app from the `apps/web` directory:

```powershell
cd apps/web
npm.cmd install
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

### 3. Open the App

```text
http://127.0.0.1:5173/
```

### 4. Run Verification Checks

Use these checks after local setup or documentation/CI changes:

```powershell
cd apps/web
npm.cmd run build
npm.cmd run test:image-paste

cd ../..
node scripts/verify-image-asset-index.js
```

### 5. Runtime Files

Uploaded note images and local asset indexes are runtime files. They should
stay out of Git:

- `runtime/`
- `public/uploads/`

For common setup issues, see
[Local development troubleshooting](docs/troubleshooting.md).

### Docker Compose

```powershell
docker compose up --build
```

## Documentation

- [Architecture](docs/architecture.md)
- [Use Cases](docs/use-cases.md)
- [Maintainer Workflow](docs/maintainer-workflow.md)
- [Local development troubleshooting](docs/troubleshooting.md)
- [Product Roadmap](docs/product/roadmap.md)
- [Project Vision](docs/product/vision.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT -- see [LICENSE](LICENSE).
