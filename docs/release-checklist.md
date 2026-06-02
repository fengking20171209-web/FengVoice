# Release Checklist

Use this checklist for alpha releases such as `v0.1.1-alpha` and `v0.2.0-alpha`.

## Before Tagging

- Confirm the target version and release type.
- Confirm all planned PRs for the release are merged.
- Update `CHANGELOG.md` with user-visible changes.
- Update roadmap or release docs when scope changed.
- Confirm CI is passing on the release commit.

## Local Validation

- Run web build from `apps/web`:

```powershell
npm.cmd run build
```

- Run image paste verification from `apps/web`:

```powershell
npm.cmd run test:image-paste
```

- Run asset index verification from the repository root:

```powershell
node scripts/verify-image-asset-index.js
```

- Perform a manual smoke test when the change touches runtime behavior:
  - start API
  - start web app
  - create a note
  - paste an image
  - confirm Markdown image URL is inserted
  - confirm `image_id` is returned by the upload API

## Release Notes

Include:

- version tag
- summary
- changes
- validation results
- known limitations
- rollback note

## Rollback Note

For alpha releases, rollback usually means checking out the previous tag and
keeping existing local runtime data untouched. If data format changes are
introduced, document whether downgrade is safe before publishing the release.
