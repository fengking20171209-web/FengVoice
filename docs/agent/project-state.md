# FengVoice Project State

## Current status

FengVoice is an early-stage alpha OSS project focused on local-first notes and
AI-generated image/audio asset workflows.

Current releases: v0.1.0-alpha through v0.2.2-alpha.

GitHub `origin/main` should remain the OSS public mainline. Local inspection has
shown that GitHub `origin/main` and Gitee `gitee/main` have diverged, so v0.3
audio work should be integrated through focused PRs instead of merging or
cherry-picking the full Gitee mainline.

## Releases

| Release | Description |
|---------|-------------|
| v0.1.0-alpha | note image paste upload and JSONL asset index |
| v0.1.1-alpha | maintainer workflow and OSS review readiness |
| v0.2.0-alpha | image asset lookup and validation workflow |
| v0.2.1-alpha | upload security hardening with magic bytes validation |
| v0.2.2-alpha | image asset migration dry-run |

## Completed workflow

- note image paste upload
- stable image_id generation
- JSONL image asset indexing
- asset index validation CLI
- image lookup by `image_id`
- image lookup by `sha256`
- metadata filters by `source`, `mime_type`, and `size_bytes`
- upload endpoint security review
- magic bytes validation for PNG / JPEG / WebP
- migration dry-run for existing uploaded note images
- image asset workflow demo document
- demo screenshot checklist
- roadmap polish
- v0.3 image asset browser design
- Codex operating instructions and agent workflow docs
- CI / verification suite

## Recently completed issues and PRs

- Issue #19 completed: upload security hardening with magic bytes validation
- Issue #10 completed: uploaded image migration dry-run
- Issue #4 completed: image asset workflow demo and screenshot checklist
- Issue #12 completed: local asset workflow roadmap planning
- PR #25 merged: image asset workflow demo
- PR #26 merged: roadmap polish
- PR #27 merged: screenshot checklist
- PR #28 merged into `origin/main`: v0.3 image asset browser design

## Current risks

- GitHub `origin/main` and Gitee `gitee/main` have diverged.
- GitHub main should remain the OSS public mainline unless the maintainer
  explicitly decides otherwise.
- Gitee v0.3 audio note capture should be manually ported, not cherry-picked
  wholesale.
- The old WIP branch `codex/api-image-asset-readonly` should remain parked.
- `_local/` contains local snapshots / patches and must not be committed.
- `services/api/main.py` WIP must be protected until the mainline is coherent.
- Local Git on Windows has shown HTTPS / lock instability.

## Current recommendation

1. Keep the current API WIP parked.
2. Commit this docs refresh in a clean branch.
3. Plan Gitee audio integration as focused PRs.
4. Restart read-only asset API work from a clean mainline after integration.
5. Resume Tencent Cloud deployment only after the mainline is coherent.

## Known limitations

- Migration `--apply` mode is not implemented.
- No web UI asset browser has been implemented yet.
- CLI-first image search remains the stable workflow.
- Project remains early-stage alpha.

## Maintainer strategy

Keep changes small and reviewable.

Prefer:
- one issue per PR
- one capability per release
- green CI before merge
- honest known limitations
- no runtime, upload, credential, or local draft files in commits

## Related docs

- AGENTS.md in project root
- docs/agent/next-actions.md
- docs/agent/operating-loop.md
- docs/agent/git-recovery.md
- docs/agents/codex-workflows.md
- docs/agents/codex-playbook.md
- docs/pr-review-checklist.md
- ROADMAP.md
