# Demo Screenshot Checklist

This directory will contain screenshots for the image asset workflow demo document.

## How to capture

1. Start the FengVoice API and web app locally.
2. Open a browser to the web app.
3. Use your operating system screenshot tool (e.g. Win+Shift+S, Cmd+Shift+4).

## Required screenshots

| File | Purpose |
|------|---------|
| `01-note-editor.png` | The note editor interface with a new or existing note |
| `02-pasted-image-markdown.png` | Note content after pasting an image (Markdown URL visible) |
| `03-uploaded-image-url.png` | The uploaded image accessible at its public URL |
| `04-jsonl-index.png` | The JSONL asset index file showing a record |
| `05-validate-cli.png` | Output of `python scripts/validate-image-asset-index.py` |
| `06-lookup-filter-cli.png` | Output of `python scripts/find-image-asset.py --image-id ...` |
| `07-migration-dry-run.png` | Output of `python scripts/migrate-existing-note-images.py` |

## Guidelines

- Capture the full terminal or browser view for context.
- Do not include personal information, credentials, or tokens in screenshots.
- Use the same demo content described in docs/demo-image-asset-workflow.md.
- Place each screenshot in this directory and reference it from the demo document using relative paths.

## Completion criteria

All 7 screenshots are captured, verified, and referenced from docs/demo-image-asset-workflow.md.
