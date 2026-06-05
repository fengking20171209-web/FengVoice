# FengVoice Project State

## Current status

FengVoice is an early-stage alpha OSS project focused on local-first notes and
AI-generated image/audio asset workflows.

Current GitHub mainline release: v0.3.1-alpha.

GitHub `origin/main` should remain the OSS public mainline. Local inspection has
shown that GitHub `origin/main` and Gitee `gitee/main` diverged. The useful
Gitee audio note capture work has now been manually ported into GitHub mainline
through focused PRs instead of merging or cherry-picking the full Gitee
mainline.

## Releases

| Release | Description |
|---------|-------------|
| v0.1.0-alpha | note image paste upload and JSONL asset index |
| v0.1.1-alpha | maintainer workflow and OSS review readiness |
| v0.2.0-alpha | image asset lookup and validation workflow |
| v0.2.1-alpha | upload security hardening with magic bytes validation |
| v0.2.2-alpha | image asset migration dry-run |
| v0.3.0-alpha | historical Gitee-side audio experiment tag; preserved, not moved |
| v0.3.1-alpha | GitHub mainline audio note capture |

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
- v0.3.1-alpha audio note backend API
- separate audio JSONL asset index
- minimal frontend audio recording UI
- manual Gitee audio feature port into GitHub mainline
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
- PR #32 merged: audio note backend API
- PR #33 merged: audio note recording UI
- GitHub Release published: v0.3.1-alpha - Audio note capture

## Current risks

- GitHub `origin/main` and Gitee `gitee/main` have diverged historically.
- GitHub main should remain the OSS public mainline unless the maintainer
  explicitly decides otherwise.
- The old `v0.3.0-alpha` tag points to the Gitee-side audio experiment and
  should remain preserved as historical context.
- GitHub mainline audio note capture is released as `v0.3.1-alpha`.
- The old WIP branch `codex/api-image-asset-readonly` should remain parked.
- `_local/` contains local snapshots / patches and must not be committed.
- Do not directly rebase or merge the parked `codex/api-image-asset-readonly`
  branch. Restart read-only asset API work from clean `origin/main` and reuse
  only the still-relevant WIP patch ideas.
- Local Git on Windows has shown HTTPS / lock instability.

## Current recommendation

1. Record the v0.3.1-alpha release state in a documentation-only PR.
2. Keep the current API WIP parked.
3. Prepare Tencent Cloud deployment from the coherent v0.3.1-alpha mainline.
4. Restart read-only image/audio asset API work from clean `origin/main`.
5. Capture real workflow screenshots after the deployable alpha baseline is
   stable.

## Known limitations

- Migration `--apply` mode is not implemented.
- No web UI asset browser has been implemented yet.
- CLI-first image search remains the stable workflow.
- Audio recording UI is intentionally minimal.
- No transcript or advanced audio library workflow exists yet.
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
