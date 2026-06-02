# Next Actions

## P0

### Recover local Git health

Reason: Local .git has shown process / lock / permission instability after fetch and tag operations.

Success criteria:
- can checkout main
- can fetch origin
- can fetch tags
- can see v0.2.0-alpha
- can create a new branch cleanly

Status: DONE. New .git directory created after renaming the permission-locked .git_old.

See docs/agent/git-recovery.md for the procedure.

## P1

### Issue #19: magic bytes validation

Goal: Verify uploaded image content by file signature instead of relying only on MIME metadata.

Success criteria:
- detect PNG, JPEG, WebP signatures
- reject mismatched declared MIME and actual content
- preserve paste upload behavior
- add tests

### Issue #10: migration dry-run

Goal: Scan existing uploaded images and generate missing JSONL index records without modifying files by default.

Success criteria:
- dry-run mode
- sha256 calculation
- duplicate detection
- clear output

## P2

### Issue #4: screenshots

Goal: Add visual documentation for note image paste workflow.

### Issue #12: roadmap

Goal: Plan the next milestone's local asset workflow scope and priorities.

### Issue #7: release checklist

Goal: Document the alpha release process so it becomes repeatable.
