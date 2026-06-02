# PR Review Checklist

Use this checklist for every FengVoice pull request. The goal is to make review
decisions explicit and repeatable, especially while the project is still in
alpha.

## 1. Code Scope Review

- Confirm the PR has one clear purpose.
- Confirm unrelated refactors are not mixed into feature or bug-fix work.
- Confirm generated, runtime, or uploaded files are not included unless the PR
  is specifically about repository fixtures.

## 2. API Compatibility

- Check whether request paths, response fields, status codes, or error details
  changed.
- If an API response changed, require documentation and a changelog note.
- For alpha-breaking changes, require an explicit migration or rollback note.

## 3. Data Format Compatibility

- Check whether persisted notes, SQLite data, JSONL asset index records, or
  image metadata changed shape.
- Preserve backward compatibility where practical.
- If compatibility is intentionally broken, document the impact and the manual
  recovery path.

## 4. CI and Test Requirement

- Require CI to pass before merge.
- Require local verification for the touched area:
  - Web: `npm.cmd run build` from `apps/web`
  - Image paste: `npm.cmd run test:image-paste` from `apps/web`
  - Asset index: `node scripts/verify-image-asset-index.js` from the repo root
- Add or update tests when behavior changes.

## 5. Documentation Requirement

- Update README, roadmap, demo docs, or product docs when user-visible behavior
  changes.
- Update release notes for changes that affect installation, usage, APIs, or
  data formats.

## 6. Security Review

- Review upload endpoints for file type, file size, path traversal, and public
  URL exposure risks.
- Check whether new inputs are validated before use.
- Avoid logging secrets, local paths containing private data, or uploaded file
  contents.

## 7. Runtime File Safety

- Do not commit files from `runtime/`.
- Do not commit files from `public/uploads/`.
- Confirm `.gitignore` still protects generated local data.

## 8. Release Note Requirement

- For release-bound PRs, include:
  - version target
  - user-visible changes
  - known limitations
  - rollback note
  - validation commands and results
