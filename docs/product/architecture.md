# FengVoice Architecture

Phase 1A runs as two lightweight services:

- `apps/web`: Vite React TypeScript web interface
- `services/api`: FastAPI service with SQLite persistence
- `services/memory-bridge`: best-effort EverCore HTTP writer
- `services/graph-bridge`: reserved graph read integration

