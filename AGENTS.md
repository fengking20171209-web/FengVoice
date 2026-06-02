# AGENTS.md

## Project

FengVoice is an early-stage local-first platform for organizing AI-generated content and note-linked image assets.

Current public alpha releases:

- 0.1.0-alpha: note image paste upload and JSONL asset index
- 0.1.1-alpha: maintainer workflow documentation and OSS review readiness
- 0.2.0-alpha: image asset lookup and validation workflow

## Current maintainer goal

Keep FengVoice moving as a truthful, maintainable open-source project.

Prefer small, reviewable PRs linked to GitHub Issues and milestones.

## Operating loop

Use this loop for all work:

1. Read the related GitHub Issue.
2. Create a focused branch from main.
3. Make the smallest useful change.
4. Run validation.
5. Create a PR with a clear summary.
6. Wait for CI.
7. Squash merge only after green checks.
8. Update release notes or maintainer logs when appropriate.

## Branch naming

Use:

- codex/docs-* for documentation
- codex/security-* for security work
- codex/asset-* for asset workflow features
- codex/fix-* for bug fixes
- codex/roadmap-* for planning and roadmap changes

## Commit style

Use Conventional Commits:

- docs: ...
- eat: ...
- ix: ...
- 	est: ...
- chore: ...

## Validation commands

For web build:

  powershell
cd D:\Projects\FengVoice\apps\web
npm.cmd run build
  

For image paste upload test:

  powershell
cd D:\Projects\FengVoice\apps\web
npm.cmd run test:image-paste
  

For asset index validation:

  powershell
cd D:\Projects\FengVoice
python scripts/verify-image-asset-index-validation.py
python scripts/verify-find-image-asset.py
node scripts/verify-image-asset-index.js
  

Run only the relevant checks for the task, but always explain what was and was not run.

## Files and directories to avoid

Do not modify or commit:

* untime/
* public/uploads/
* local OpenAI application files
* local browser automation scripts
* credentials
* tokens
* API keys

Never commit:

* OPENAI_CODEX_OSS_FORM_FIELDS.json
* OPENAI_CODEX_OSS_FORM_FIELDS_READY.md
* OPENAI_CODEX_OSS_SUBMIT_LOG.md
* OPENAI_CODEX_OSS_FILL_RESULT.md
* GITHUB_RELEASE_*.md
* local application draft files unless explicitly requested

## Core logic safety

Do not modify these files unless the issue explicitly requires it:

* services/api/main.py
* services/api/asset_index.py
* pps/web core runtime code

When modifying upload behavior, preserve:

* image paste upload behavior
* Markdown image insertion
* stable image_id
* JSONL asset index append behavior
* existing validation scripts

## Git safety

Do not run:

* git reset
* git rebase
* git push --force
* destructive branch deletion
* destructive tag deletion

If git-remote-https.exe crashes or Git locks appear:

1. Stop.
2. Inspect processes.
3. Check .git/*.lock.
4. Report state.
5. Do not retry push in a loop.

See docs/agent/git-recovery.md.

## Current next actions

Before starting new work, read:

* docs/agent/project-state.md
* docs/agent/next-actions.md
* the relevant GitHub Issue
