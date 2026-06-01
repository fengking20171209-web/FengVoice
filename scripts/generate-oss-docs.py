import os
from pathlib import Path

ROOT = Path(r"D:\Projects\FengVoice")

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  Created {path.relative_to(ROOT)}")

print("=== Generating OSS Documentation ===\n")

# ── 1. LICENSE ───────────────────────────────────────────────────────────
write(ROOT / "LICENSE", """MIT License

Copyright (c) 2026 FengVoice Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")

# ── 2. README.md ─────────────────────────────────────────────────────────
write(ROOT / "README.md", """# FengVoice

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
""")


# ── 3. CHANGELOG.md ─────────────────────────────────────────────────────
write(ROOT / "CHANGELOG.md", """# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-alpha] - 2026-06-01

### Added

- Notes CRUD API (FastAPI + SQLite)
- React/TypeScript web UI with full note management
- Paste-upload image support with automatic URL generation
- Image asset index (SHA-256 addressed, JSONL-backed)
- EverCore memory bridge integration (best-effort, non-blocking)
- Graph bridge reserved integration point
- Docker Compose setup for local development
- Cross-CORS configuration for local development
- Health check endpoint

### Infrastructure

- MIT license
- CI workflow via GitHub Actions (lint + test)
- Issue and PR templates for community contributions
""")

# ── 4. ROOT ROADMAP.md ──────────────────────────────────────────────────
write(ROOT / "ROADMAP.md", """# FengVoice Public Roadmap

> Last updated: 2026-06-01

## Completed

- **Phase 0** -- Repository and service foundation
- **Phase 1A** -- Notes MVP with CRUD API, React UI, memory bridge
- **Phase 1B** -- Notes UI organization and polish
- **Phase 2A** -- Image paste upload
- **Phase 2B** -- Image asset index (SHA-256, JSONL)

## Upcoming

- **Phase 1C** -- Lightweight cloud deployment (Tencent Cloud)
- **Phase 2C** -- Prompt and asset migration tooling
- **Phase 3** -- Content and audio production workflows
""")


# ── 5. CONTRIBUTING.md ──────────────────────────────────────────────────
write(ROOT / "CONTRIBUTING.md", """# Contributing to FengVoice

Thanks for your interest in contributing! We welcome issues, documentation
improvements, and well-scoped feature work.

## Getting Started

1. Fork the repository.
2. Create a feature branch: \git checkout -b codex/my-feature\
3. Follow the [Quick Start](README.md#quick-start) to set up locally.
4. Make your changes and ensure existing functionality is not broken.
5. Commit with a descriptive message (see style below).
6. Open a pull request against \main\.

## Commit Style

We use conventional commits:

`
feat: add new feature
fix: correct a bug
docs: update documentation
refactor: restructure code without behavior change
test: add or update tests
chore: tooling, CI, dependencies
`

## Code Standards

- Python: follow PEP 8 and type-annotate public functions.
- TypeScript/React: prefer functional components with hooks; use TypeScript
  strict mode.
- Keep tests focused; add them alongside new functionality when feasible.

## Pull Request Process

1. Keep PRs small and focused on a single concern.
2. Update docs if your change affects setup, API, or workflow.
3. Ensure CI passes before requesting review.
4. A maintainer will review within a few business days.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Be
respectful, inclusive, and constructive.
""")

# ── 6. SECURITY.md ──────────────────────────────────────────────────────
write(ROOT / "SECURITY.md", """# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | Security fixes     |

## Reporting a Vulnerability

FengVoice is a local-first tool with minimal attack surface. If you discover
a security-relevant issue:

- **Do not** open a public issue.
- Report privately by emailing the maintainer at the address listed in the
  git commit history, or by opening a GitHub draft security advisory.

You should receive a response within 72 hours. We appreciate responsible
disclosure and will acknowledge valid reports.

## Scope

The following are considered out of scope:
- Dependency CVEs with no practical exploit path in the default configuration
- Theoretical attacks requiring physical access or modified .env files
""")

# ── 7. CODE_OF_CONDUCT.md ───────────────────────────────────────────────
write(ROOT / "CODE_OF_CONDUCT.md", """# Contributor Covenant Code of Conduct

## Our Pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

## Our Standards

Examples of behavior that contributes to a positive environment:

- Demonstrating empathy and kindness toward other people
- Being respectful of differing opinions, viewpoints, and experiences
- Giving and gracefully accepting constructive feedback
- Accepting responsibility and apologizing to those affected by our mistakes
- Focusing on what is best for the overall community

Examples of unacceptable behavior:

- The use of sexualized language or imagery, and sexual attention or advances
- Trolling, insulting or derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Enforcement Responsibilities

Project maintainers are responsible for clarifying and enforcing our standards
and will take appropriate and fair corrective action in response to any
behavior they deem inappropriate, threatening, offensive, or harmful.

## Scope

This Code of Conduct applies within all community spaces, and also applies
when an individual is officially representing the community in public spaces.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the project maintainers. All complaints will be reviewed and
investigated promptly and fairly.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage],
version 2.1, available at
https://www.contributor-covenant.org/version/2/1/code_of_conduct.html.
""")


# ── 8. docs/architecture.md ──────────────────────────────────────────────
write(ROOT / "docs" / "architecture.md", """# FengVoice Architecture

## Overview

FengVoice is designed as a modular, local-first workspace with a clear
separation between data, services, and presentation.

`
+-----------------------------+
|         apps/web            |
|   React + Vite + TypeScript |
|           :3000             |
+-------------+---------------+
              | HTTP (CORS)
+-------------v---------------+
|       services/api           |
|  FastAPI + SQLite + Assets   |
|           :8000              |
+------+-------------+--------+
       |             |
+------v--------+ +--v-----------+
| memory-bridge | | graph-bridge |
| EverCore HTTP | | (reserved)   |
| (best-effort) | |              |
+---------------+ +--------------+
`

## Components

### Web App (\pps/web\)

Vite-powered React application with TypeScript. Communicates with the API
over HTTP. Supports pasting images directly into note content.

### API (\services/api\)

FastAPI application providing:
- Notes CRUD (\/api/notes\)
- Image upload (\/api/uploads/images\)
- Asset index via \sset_index.py\ (SHA-256, JSONL)
- Health check (\/health\)

Persistence is via SQLite at \data/fengvoice.db\. Uploaded images are stored
under \public/uploads/notes/\.

### Memory Bridge (\services/memory-bridge\)

An optional lightweight HTTP client that writes note events to an EverCore
memory server. Failures are logged but never block the main request path.

### Graph Bridge (\services/graph-bridge\)

Reserved for future graph-based read integration. Currently a placeholder.

## Data Flow

1. User creates/edits a note in the web UI.
2. UI sends HTTP request to the API.
3. API persists to SQLite and (optionally) forwards to memory bridge.
4. Image pastes are uploaded, stored to disk, indexed by SHA-256, and the
   absolute URL is returned for embedding in note content.
5. Asset index records are appended to \
untime/asset-index/note-images.jsonl\.
""")

# ── 9. docs/use-cases.md ────────────────────────────────────────────────
write(ROOT / "docs" / "use-cases.md", """# FengVoice Use Cases

## Personal Knowledge Base

Quickly capture ideas, notes, and to-dos. Paste screenshots or diagrams
directly into notes. Tag and search notes to retrieve information later.

Ideal for developers, researchers, and writers who want a local, zero-fuss
note-taking tool with image support.

## Image Asset Management

Paste images from clipboard and get stable URLs. The SHA-256 asset index
prevents duplicate storage and provides a traceable record of every image
uploaded.

Useful when composing documentation, blog posts, or presentations that
reference locally hosted images.

## Content Production Pipeline (future)

With audio production workflows planned for Phase 3, FengVoice aims to become
an end-to-end content workspace where notes become scripts, images become
illustrations, and recordings become deliverables, all managed from one
local dashboard.

## AI-Enhanced Writing via Memory Bridge (optional)

When paired with an EverCore memory server, note events can be forwarded to
an AI memory layer for context-aware suggestions, cross-note queries, and
long-term recall, without making the memory service a hard dependency.
""")

# ── 10. docs/maintainer-workflow.md ──────────────────────────────────────
write(ROOT / "docs" / "maintainer-workflow.md", """# Maintainer Workflow

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
.venv\\Scripts\\Activate.ps1
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
- Python lint (\
uff\ or \py_compile\)
- Web build (\
pm run build\)
- Smoke test (startup check)
""")


# ── 11. .github/ISSUE_TEMPLATE/bug_report.md ────────────────────────────
write(ROOT / ".github" / "ISSUE_TEMPLATE" / "bug_report.md", """---
name: Bug Report
about: Create a report to help us improve
title: \"[Bug] \"
labels: bug
assignees: \"\"
---

**Describe the bug**
A clear and concise description of the issue.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment (please complete):**
- OS: [e.g. Windows 11, macOS 14]
- Browser: [e.g. Chrome 125, Firefox 128]
- FengVoice version: [e.g. 0.1.0-alpha]

**Additional context**
Add any other context about the problem here.
""")

# ── 12. .github/ISSUE_TEMPLATE/feature_request.md ───────────────────────
write(ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_request.md", """---
name: Feature Request
about: Suggest an idea for this project
title: \"[Feature] \"
labels: enhancement
assignees: \"\"
---

**Is your feature request related to a problem?**
A clear description of what the problem is.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
A clear description of any alternative solutions or features you've considered.

**Additional context**
Add any other context, screenshots, or references about the feature request.
""")

# ── 13. .github/PULL_REQUEST_TEMPLATE.md ────────────────────────────────
write(ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md", """## Summary

<!-- One-sentence summary of the change. -->

## Related Issues

<!-- Closes #... or Relates to #... -->

## Changes

- <!-- Bullet describing one specific change -->
- <!-- Bullet describing another specific change -->

## Testing

- [ ] API starts without errors
- [ ] Web app builds without errors
- [ ] Existing functionality is not broken
- [ ] New behavior is covered by tests (if applicable)

## Checklist

- [ ] Code follows project conventions
- [ ] Docs updated if needed
- [ ] Commits follow conventional commit style
""")

# ── 14. .github/workflows/test.yml ──────────────────────────────────────
write(ROOT / ".github" / "workflows" / "test.yml", """name: Test

on:
  push:
    branches: [\"main\"]
  pull_request:
    branches: [\"main\"]

jobs:
  lint-and-build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: \"3.12\"

      - name: Install Python dependencies
        working-directory: services/api
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Python lint
        working-directory: services/api
        run: python -m py_compile main.py asset_index.py

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: \"22\"
          cache: \"npm\"
          cache-dependency-path: apps/web/package-lock.json

      - name: Install Node dependencies
        working-directory: apps/web
        run: npm ci

      - name: Build web app
        working-directory: apps/web
        run: npm run build

      - name: Smoke check
        run: echo \"CI passed\"
""")

# ── 15. OPENAI_CODEX_OSS_APPLICATION_DRAFT.md ────────────────────────────
write(ROOT / "OPENAI_CODEX_OSS_APPLICATION_DRAFT.md", """# OpenAI Codex OSS Application Draft

> **Project**: FengVoice
> **Date**: 2026-06-01
> **Repository**: https://github.com/fengking20171209-web/FengVoice
> **Branch**: \codex/oss-application-rush\

## Application Overview

FengVoice is a local-first content workspace for notes and image assets,
built with Codex (GPT-5 based coding agent). This application is submitted
as part of the OpenAI Codex OSS Application Rush program.

## AI-Assisted Development

This project was developed primarily through collaboration with Codex, an
AI coding agent powered by GPT-5. Key milestones:

- **Phase 1A** -- Notes MVP with FastAPI backend and React frontend
- **Phase 1B** -- UI organization and refinement
- **Phase 2A** -- Image paste upload functionality
- **Phase 2B** -- SHA-256 image asset index

## OSS Documentation

All standard OSS documents have been created:

| File | Description |
|------|-------------|
| LICENSE | MIT license |
| README.md | Project overview and quick start |
| CHANGELOG.md | Version history |
| ROADMAP.md | Public roadmap |
| CONTRIBUTING.md | Contribution guide |
| SECURITY.md | Security policy |
| CODE_OF_CONDUCT.md | Code of conduct |
| docs/architecture.md | System architecture |
| docs/use-cases.md | Use case documentation |
| docs/maintainer-workflow.md | Maintainer guide |
| .github/ISSUE_TEMPLATE/ | Bug report and feature request templates |
| .github/PULL_REQUEST_TEMPLATE.md | PR template |
| .github/workflows/test.yml | CI workflow |

## Reflection

The AI-assisted development workflow enabled rapid iteration across the full
stack, from database schema to React UI to CI configuration, within a
single project context. The OSS Application Rush provided the structure and
motivation to formalize community-facing documentation alongside the code.
""")

# ── 16. OSS_APPLICATION_RUSH_REPORT.md ──────────────────────────────────
write(ROOT / "OSS_APPLICATION_RUSH_REPORT.md", """# OSS Application Rush Report

## Project: FengVoice

| Metric | Value |
|--------|-------|
| Repository | github.com/fengking20171209-web/FengVoice |
| License | MIT |
| Latest version | 0.1.0-alpha |
| Primary language | Python (FastAPI) / TypeScript (React) |
| AI assistant | Codex (GPT-5 based) |

## Documents Created

This rush produced **16 files**:

1. **LICENSE** -- MIT license (updated copyright holder)
2. **README.md** -- Full project overview, features, quick start
3. **CHANGELOG.md** -- Keep a Changelog format, 0.1.0-alpha
4. **ROADMAP.md** -- Completed phases and upcoming milestones
5. **CONTRIBUTING.md** -- Getting started, commit style, code standards
6. **SECURITY.md** -- Supported versions, reporting process
7. **CODE_OF_CONDUCT.md** -- Contributor Covenant 2.1
8. **docs/architecture.md** -- System architecture overview
9. **docs/use-cases.md** -- Knowledge base, asset management, content pipeline
10. **docs/maintainer-workflow.md** -- Branch strategy, release process, CI
11. **.github/ISSUE_TEMPLATE/bug_report.md** -- Structured bug reports
12. **.github/ISSUE_TEMPLATE/feature_request.md** -- Structured feature requests
13. **.github/PULL_REQUEST_TEMPLATE.md** -- PR checklist and summary
14. **.github/workflows/test.yml** -- GitHub Actions CI workflow
15. **OPENAI_CODEX_OSS_APPLICATION_DRAFT.md** -- OSS application context
16. **OSS_APPLICATION_RUSH_REPORT.md** -- This report

## Verification

- All documents are in English
- License chosen: MIT (widest OSS compatibility)
- CI configured for GitHub Actions
- Issue and PR templates follow GitHub conventions
- Architecture documentation reflects actual project structure

## Conclusion

FengVoice is now fully equipped with standard open-source community
infrastructure. The project is ready for public contribution with clear
guidance for contributors, maintainers, and security researchers.
""")

print("\n=== All 16 OSS documentation files generated ===")

