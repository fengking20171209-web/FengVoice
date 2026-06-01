# Maintainer Workflow

## Branch Strategy

- \main\ -- stable, reviewed changes only
- \codex/*\ -- feature branches (bot-assisted development)
- Feature branches are squash-merged into \main\ to keep history clean

## Development Loop

1. Create a feature branch from \main\.
2. Make changes, test locally.
3. Push and open a pull request.
4. Ensure CI passes (lint, build, smoke test).
5. Squash-merge into \main\.
6. Tag significant milestones with \*\ tags.

## Local Testing

`powershell
# API tests
cd services/api
.venv\Scripts\Activate.ps1
pytest

# Web build
cd apps/web
npm run build

# Smoke test
Start-Process http://localhost:8000/health
Start-Process http://localhost:3000
`

## Release Process

1. Update \CHANGELOG.md\ with changes since last release.
2. Bump version in \services/api/main.py\ (FastAPI \ersion\ arg).
3. Commit: \chore: bump to v0.x.y\.
4. Tag: \git tag v0.x.y\.
5. Push: \git push origin main --tags\.

## CI

GitHub Actions workflow runs on every push and PR:
- Python lint (uff\ or \py_compile\)
- Web build (pm run build\)
- Smoke test (startup check)
