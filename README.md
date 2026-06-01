# FengVoice

FengVoice is a lightweight, local-first content workspace for notes and image
assets. It provides a fast note-taking experience with paste-upload image
support, an append-only image asset index, and optional use of AI memory
bridges for enriched context.

Built with a Python/FastAPI backend and a React/TypeScript frontend, FengVoice
runs entirely on your machine with no external dependencies beyond what you
already have installed.

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

`powershell
cd apps/web
npm install
npm run dev -- --host 0.0.0.0 --port 3000
`

Open http://localhost:3000. The API health endpoint is http://localhost:8000/health.

### Docker Compose

`powershell
docker compose up --build
`

## Documentation

- [Architecture](docs/architecture.md)
- [Use Cases](docs/use-cases.md)
- [Maintainer Workflow](docs/maintainer-workflow.md)
- [Product Roadmap](docs/product/roadmap.md)
- [Project Vision](docs/product/vision.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT -- see [LICENSE](LICENSE).
