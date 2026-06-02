# Skill: Security Review

## When to use

When reviewing a security-related Issue, investigating a potential vulnerability, or auditing an endpoint or data flow.

## Steps

1. Identify the scope: which endpoint, file, or data flow is under review.
2. Read the relevant source code and understand the data path.
3. Check for these common issues in a local-first note/image platform:
   - Uploaded file type validation (extension-only vs magic bytes)
   - Path traversal in file serving
   - Unbounded storage (no size cap on uploads)
   - Exposure of internal file paths in responses
   - Lack of content-type verification on served assets
   - Credential or token leakage in logs or error messages
   - Missing authentication checks on write endpoints
4. Document each finding with:
   - Severity (low / medium / high)
   - Location (file and line number)
   - Risk description
   - Recommended fix
5. Create a GitHub Issue for each actionable finding.
6. If the finding is a quick fix, create a PR directly.
7. If the finding needs discussion, link the Issue and tag it with the "security" label.
8. Update docs/agent/project-state.md known limitations if relevant.

## Reference

- OWASP File Upload Cheat Sheet
- Existing review: Issue #8 (upload endpoint security review)
- Follow-up: Issue #19 (magic bytes validation)
