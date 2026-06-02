# Skill: Issue to PR

## When to use

When starting work on a GitHub Issue or implementing a small change.

## Steps

1. Read the GitHub Issue to understand the requirement.
2. Check AGENTS.md for branch naming and validation rules.
3. Read docs/agent/project-state.md and docs/agent/next-actions.md.
4. Create a branch from main:

git checkout main
git pull origin main
git checkout -b codex/<category>-<short-description>

5. Implement the smallest useful change.
6. Run the relevant validation checks (see AGENTS.md Validation commands).
7. Stage and commit:

git add <files>
git commit -m "<type>: <description>"

8. Push and create a PR:

git push origin codex/<branch-name>
gh pr create --title "<type>: <description>" --body "Closes #<issue-number>" --base main

9. Wait for CI.
10. Squash merge after green checks.
11. Update docs/agent/next-actions.md if priorities changed.
