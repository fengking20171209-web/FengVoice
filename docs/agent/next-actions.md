# Next Actions

## P0

### Record the v0.3.1-alpha release state

Goal: Keep the agent context aligned with the published GitHub mainline audio
release.

Success criteria:
- document `v0.3.1-alpha` as the latest GitHub mainline release
- preserve `v0.3.0-alpha` as the historical Gitee-side audio experiment tag
- keep the update documentation-only
- do not commit `_local/`, `runtime/`, `public/uploads/`, `OPENAI*`, `vault/`,
  or `.git_old/`

### Keep the mainline coherent

Goal: Treat `origin/main` after `v0.3.1-alpha` as the clean alpha baseline.

Success criteria:
- avoid merging or cherry-picking broad Gitee mainline work
- avoid moving or deleting historical tags
- keep release follow-up PRs small and reviewable
- run focused validation before any behavior-changing PR

### Avoid using the parked dirty API branch directly

Goal: Protect the old read-only asset API WIP until it can be restarted safely.

Success criteria:
- keep `codex/api-image-asset-readonly` parked
- do not rebase or merge that dirty branch into the new mainline
- reuse only saved patch ideas that still fit the current codebase
- restart read-only asset API work from clean `origin/main`

## P1

### Prepare Tencent Cloud deployment

Goal: Turn the v0.3.1-alpha mainline into a deployable alpha baseline.

Success criteria:
- confirm Docker and runtime configuration assumptions
- document deployment commands and rollback notes
- keep credentials, tokens, runtime data, and uploads out of Git
- verify API and web build from the selected release baseline

### Refresh deployment runbook and Docker readiness

Goal: Make deployment steps reproducible before publishing wider usage notes.

Success criteria:
- document environment variables and local-first storage assumptions
- verify service startup path
- note what is intentionally not production-ready
- keep early-stage alpha limitations visible

### Restart read-only image/audio asset API

Goal: Resume asset API work from the clean v0.3.1-alpha mainline.

Success criteria:
- create a new branch from clean `origin/main`
- implement only the smallest read-only API surface needed next
- preserve image paste upload, image JSONL append, audio JSONL append, and
  existing validation scripts
- add focused API validation

## P2

### Capture real screenshots for audio and image workflow demos

Goal: Add browser evidence once the deployable alpha baseline is stable.

Success criteria:
- capture note image paste workflow
- capture audio recording and uploaded audio link insertion
- capture validation output
- avoid committing `runtime/` or `public/uploads/`

### Polish audio note documentation

Goal: Explain the intentionally minimal audio workflow without overstating
production readiness.

Success criteria:
- describe backend upload behavior
- describe separate audio JSONL index
- document current browser recording limitations
- document that transcript and advanced audio library features are future work

### Plan transcript and AI asset library work

Goal: Keep future audio intelligence work separate from the alpha release.

Success criteria:
- define transcript scope separately
- define AI asset library scope separately
- avoid mixing deployment, transcript, and asset browser work into one PR
