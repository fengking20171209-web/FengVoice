# Next Actions

## P0

### Protect the current worktree and avoid accidental commits

Goal: Keep local WIP, local snapshots, and protected directories out of Git.

Success criteria:
- do not commit `_local/`, `runtime/`, `public/uploads/`, `OPENAI*`, `vault/`,
  or `.git_old/`
- do not include unfinished `services/api/main.py` WIP in documentation commits
- keep the old `codex/api-image-asset-readonly` branch parked until the mainline
  is coherent

### Merge the docs refresh PR

Goal: Land the refreshed project-state and next-actions docs from a clean
branch.

Success criteria:
- only `docs/agent/project-state.md` and `docs/agent/next-actions.md` are
  changed
- Codex workflow documentation verification passes
- PR clearly states this is documentation-only

### Resolve the GitHub/Gitee main divergence plan

Goal: Decide how to integrate Gitee v0.3 audio note capture without overwriting
the GitHub OSS mainline.

Success criteria:
- document GitHub-only work
- document Gitee-only audio work
- keep GitHub `origin/main` as the public OSS authority unless the maintainer
  explicitly chooses otherwise
- avoid `merge gitee/main` and avoid cherry-picking the broad Gitee mainline
  commit wholesale

### Decide how to preserve or park `services/api/main.py` WIP

Goal: Protect the read-only asset API work until it can restart from a clean
mainline.

Success criteria:
- keep the saved API patch available locally
- do not continue API implementation on the old dirty branch
- restart from a clean branch after audio integration planning

## P1

### Manually port Gitee v0.3 audio note capture

Goal: Bring the useful Gitee audio note capture work into GitHub main through
focused PRs.

Success criteria:
- manually port behavior instead of cherry-picking `061942b`
- preserve v0.2.1 upload security hardening
- preserve v0.2.2 migration dry-run work
- preserve image paste upload, Markdown image insertion, stable `image_id`, and
  JSONL asset index append behavior

### Split audio integration if needed

Goal: Keep audio integration reviewable.

Candidate split:
- PR A: audio backend/API integration
- PR B: audio frontend/UI integration

Success criteria:
- backend and frontend changes can be reviewed independently if the combined
  scope is too large
- focused validation is run for each PR

### Restart read-only image asset API

Goal: Resume the read-only image asset API from a clean branch after audio
integration.

Success criteria:
- branch from the selected clean mainline
- apply or rewrite only the protected API WIP that still fits the new base
- add focused API validation

## P2

### Tencent Cloud deployment after mainline coherence

Goal: Resume deployment work only after the public mainline and integration plan
are stable.

Success criteria:
- selected mainline is coherent
- deployment docs match the selected release scope
- no local runtime, upload, credential, or draft files are committed

### v0.3 asset browser implementation

Goal: Implement the designed asset browser after API and mainline work are
stable.

Success criteria:
- design scope is confirmed
- API surface is stable
- frontend branch starts from a clean mainline

### Real screenshots for demo documentation

Goal: Capture real browser evidence for the demo documentation when the app
flow is stable.

Success criteria:
- capture note editor before paste
- capture pasted Markdown image URL
- capture uploaded image URL
- capture JSONL index record
- capture validation output
- capture lookup/filter output
- capture migration dry-run output
- avoid committing `runtime/` or `public/uploads/`

### Add local ignore protection in a separate PR if needed

Goal: Reduce accidental commit risk from local worktree and recovery folders.

Candidate entries:
- `_local/`
- `.git_old/`

Success criteria:
- keep this separate from the docs refresh PR
- verify repository safety after updating ignore rules
