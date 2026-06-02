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

### API

`powershell
cd services/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
`

### Web

```powershell
cd apps/web
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

Open http://localhost:3000. The API health endpoint is http://localhost:8000/health.

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
