# FengVoice Architecture

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
5. Asset index records are appended to untime/asset-index/note-images.jsonl\.
