# Operating Loop

## Core principle

Every change follows a repeatable cycle. This keeps work reviewable, mergable, and maintainable.

## The loop

1. Read the related GitHub Issue.
2. Review AGENTS.md, docs/agent/project-state.md, and docs/agent/next-actions.md.
3. Create a focused branch from main.
4. Make the smallest useful change.
5. Run relevant validation checks.
6. Create a PR with a clear summary linked to the Issue.
7. Wait for CI to pass.
8. Squash merge only after green checks.
9. Update release notes or maintainer logs when appropriate.
10. Update docs/agent/next-actions.md if priorities shift.

## When to deviate

- Documentation-only changes may skip CI build validation but should still run a syntax or formatting check.
- Security follow-ups should include the related security review reference.
- Emergency hotfixes still follow the loop but may skip non-blocking validation steps.

## What this avoids

- Large unfocused commits
- PRs without a linked Issue
- Merges without CI
- Branches that drift far from main
- Skipped validation
- Repeated trial-and-error Git operations
