# Changelog

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
