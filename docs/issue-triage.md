# Issue Triage

This document defines the labels and handling rules for FengVoice issues. Use it
to keep the issue tracker useful for contributors, reviewers, and maintainers.

## Label Definitions

| Label | Use When |
|---|---|
| `bug` | Existing behavior is broken or produces an incorrect result. |
| `enhancement` | A small improvement to existing behavior or developer workflow. |
| `documentation` | README, docs, examples, screenshots, or release notes need work. |
| `security` | The issue involves upload safety, data exposure, secrets, dependency risk, or unsafe defaults. |
| `good first issue` | The issue is scoped, low-risk, and has enough context for a new contributor. |
| `roadmap` | The issue tracks planning for a future phase or milestone. |
| `needs reproduction` | A bug report lacks enough steps, environment details, or logs. |
| `priority-p0` | Blocks releases, corrupts data, or creates a serious security concern. |
| `priority-p1` | Important for the next release or affects a main workflow. |
| `priority-p2` | Useful but not urgent; can wait for a later maintenance window. |

## Triage Rules

- Every issue should have at least one type label: `bug`, `enhancement`,
  `documentation`, `security`, or `roadmap`.
- Bugs should include reproduction steps, expected behavior, actual behavior,
  environment, and logs or screenshots when relevant.
- Security issues should be kept focused on risk, impact, and mitigation. Avoid
  posting exploit details beyond what is needed to reproduce safely.
- Roadmap issues should include goal, scope, non-goals, acceptance criteria, and
  known risks.
- Add `needs reproduction` when the issue cannot be acted on yet.
- Add one priority label when the issue is accepted into active planning.

## Weekly Maintenance Loop

1. Review new issues and assign labels.
2. Ask for reproduction details on incomplete bug reports.
3. Move small, well-scoped documentation or test tasks to `good first issue`.
4. Close duplicates with a link to the canonical issue.
5. Update `MAINTAINER_LOG.md` with meaningful triage decisions.
