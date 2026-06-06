# Rich Note v1 Manual Acceptance Report

## Report Info

- **File**: `reports/personal-notes/rich-note/04-rich-note-v1-manual-acceptance.md`
- **Date**: 2026-06-06
- **Branch**: `codex/personal-notes-strategy-docs`
- **Baseline**: `4790b23` feat(web): support image blocks in rich notes

## Commits Under Test

| # | Commit | Message |
|---|--------|---------|
| 1 | `3341770` | feat(web): add rich note block helpers |
| 2 | `31c0ad2` | feat(web): add lightweight rich note editor |
| 3 | `4790b23` | feat(web): support image blocks in rich notes |

## Test Procedure

### Test 1: New Markdown Note

- [ ] New note created successfully
- [ ] Standard Markdown editing works

### Test 2: Image Paste in Markdown Note

- [ ] Pasted image inserts as `![pasted image](url)`
- [ ] No unexpected behavior

### Test 3: New Rich Note

- [ ] Rich note mode can be toggled
- [ ] Rich note editor initializes correctly

### Test 4: Chinese Input

- [ ] Long Chinese sentences type without lag
- [ ] IME composition not truncated

### Test 5: Plain Text Paste

- [ ] Plain text does not trigger image upload
- [ ] Text inserted as expected

### Test 6: Non-Image File Paste

- [ ] Non-image files do not create image blocks
- [ ] Behavior is consistent

### Test 7: Image Paste in Rich Note

- [ ] Pasted image generates image block
- [ ] Empty paragraph appears below image block

### Test 8: Special Characters

- [ ] Double quotes, backslashes, `code` render correctly after save/reopen

### Test 9: Block Restoration

- [ ] Blocks recover when switching notes and returning

### Test 10: Git Status Clean

- [ ] `git status --short` shows no `data/`, `runtime/`, `public/uploads/` staged

## Result Summary

| Test | Result |
|------|--------|
| 1 | _pending_ |
| 2 | _pending_ |
| 3 | _pending_ |
| 4 | _pending_ |
| 5 | _pending_ |
| 6 | _pending_ |
| 7 | _pending_ |
| 8 | _pending_ |
| 9 | _pending_ |
| 10 | _pending_ |

**Overall**: _pending manual verification_

## Known Issues / UX Follow-up

| # | Issue | Severity | Status |
|---|-------|----------|--------|
| _ | _to be recorded from manual testing_ | _low/med/high_ | _open_ |

## Notes

- Functional commits are complete. This report is documentation only.
- UX improvements should be tracked separately.
- Do not mix bug fixes into this commit.

## Conclusion

This report documents the manual acceptance test results for Rich Note v1.
All functional commits (`3341770`, `31c0ad2`, `4790b23`) form the test baseline.

After manual testing completes:
- Fill in the test result table
- Record any known issues
- Submit this report as a documentation-only commit
