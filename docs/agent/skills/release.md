# Skill: Release

## When to use

When a set of closed Issues and merged PRs warrants a new alpha release.

## Trigger conditions

- At least one new capability has been merged to main.
- CI passes on main.
- The release notes cover all included work.
- The tag follows the existing naming convention.

## Steps

1. Confirm main is up to date:

git checkout main
git pull origin main

2. Review the merged commits:

git log --oneline -10
git tag --list "v0.*"

3. Choose the next version number following semantic versioning for alphas.
4. Create release notes file: GITHUB_RELEASE_V<version>.md
5. Create the tag and GitHub Release:

git tag -a v<version> -m "v<version>: <short description>"
git push origin v<version>
gh release create v<version> --repo fengking20171209-web/FengVoice --title "v<version> - <title>" --notes-file GITHUB_RELEASE_V<version>.md

6. Verify the release on GitHub.
7. Close the associated milestone if the release completes it.
8. Update docs/agent/project-state.md with the new release.
9. Update docs/agent/next-actions.md.

## Do not

- Include unmerged work in release notes.
- Modify runtime behavior during a release-only PR.
- Commit OpenAI application or form files in the release branch.
