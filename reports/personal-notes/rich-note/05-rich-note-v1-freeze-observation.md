# Rich Note v1 Freeze Observation Log

## Status

OBSERVING

## Observation Window

- Start:
- End:
- Duration: 1-2 days

## Scope

Frozen feature commits:

- 3341770 feat(web): add rich note block helpers
- 31c0ad2 feat(web): add lightweight rich note editor
- 4790b23 feat(web): support image blocks in rich notes
- 48d25ca docs: add rich note v1 manual acceptance report

## Daily Usage Scenarios

| Date | Scenario | Duration | Result | Notes |
|---|---|---:|---|---|
|  | Listening/course screenshot notes |  | PENDING | |
|  | AI long-task review note |  | PENDING | |
|  | Tax/accounting knowledge note |  | PENDING | |
|  | General markdown note regression |  | PENDING | |

## UX vs Blocker Classification

Use this rule:

- UX: usable but uncomfortable
- Blocker: prevents daily use or risks data loss

| Type | Symptom | Reproduction Steps | Severity | Notes |
|---|---|---|---|---|
| UX / Blocker |  |  | PENDING | |

## Input Method / Chinese IME Check

| Check | Expected | Result | Notes |
|---|---|---|---|
| Long Chinese sentence typing | No truncation, no cursor jump | PENDING | |
| Fast typing under system load | No IME candidate flicker | PENDING | |
| Paragraph switching | Cursor remains predictable | PENDING | |

## Image Paste Check

| Check | Expected | Result | Notes |
|---|---|---|---|
| Single screenshot paste | Image block + empty paragraph | PENDING | |
| Continuous screenshots paste | Can continue typing after images | PENDING | |
| Plain text paste | No upload triggered | PENDING | |
| Non-image file paste | No image block created | PENDING | |

## Text Preservation Check

| Check | Expected | Result | Notes |
|---|---|---|---|
| Newlines | Preserved after save/reopen | PENDING | |
| Leading spaces | Preserved after save/reopen | PENDING | |
| Double quotes | Preserved after save/reopen | PENDING | |
| Backslash | Preserved after save/reopen | PENDING | |
| Inline `code` | Preserved after save/reopen | PENDING | |

## Empty Content / Backspace Check

| Check | Expected | Result | Notes |
|---|---|---|---|
| Delete all text | Editor remains usable | PENDING | |
| Delete after image | Empty paragraph remains | PENDING | |

## Git Status Daily Check

Run before ending each day:

```powershell
cd D:\Projects\FengVoice_Clean
git status --short
```

| Date  | Expected                              | Result  | Notes |
| ----- | ------------------------------------- | ------- | ----- |
| Day 1 | No staged data/runtime/public/uploads | PENDING |       |
| Day 2 | No staged data/runtime/public/uploads | PENDING |       |

## Known Issues

Record only real observed issues.

* None yet.

## V1.1 Candidate Fixes

Do not implement during observation.

| Candidate                | Trigger                            | Priority | Notes |
| ------------------------ | ---------------------------------- | -------- | ----- |
| Auto-grow textarea       | Long paragraph feels cramped       | PENDING  |       |
| Improve post-image focus | Continuous paste feels interrupted | PENDING  |       |
| Polish rich note spacing | Blocks feel visually crowded       | PENDING  |       |

## Final Observation Decision

* [ ] PASS — keep Rich Note v1 as daily-use baseline
* [ ] WARN — usable, create small V1.1 fix task
* [ ] FAIL — fix blocker before daily use

## Next Step After Observation

If PASS:

* continue daily use

If WARN:

* create focused fix task:
  `fix(web): improve rich note editor typing ergonomics`

If FAIL:

* create blocker fix task before new features
