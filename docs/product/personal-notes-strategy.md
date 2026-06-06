# FengVoice Personal Notes Strategy

## New Positioning

FengVoice should first become a local-first personal notes and content asset workspace.

The near-term product question is not whether FengVoice is ready for public showcase or cloud deployment. The near-term question is whether the maintainer can open it every day to capture, review, search, and reuse real work notes.

## Why Shift from Application-First to Self-Use-First

The previous OSS/application and deployment work created useful project hygiene: releases, security checks, asset indexing, and maintainer workflows. However, FengVoice needs a daily reason to exist before more public packaging work.

Self-use-first means:

- build around the maintainer's real Pi Agent / Codex / Kimi collaboration loop;
- validate the note, prompt, image, audio, and review flows with real data;
- keep the system local-first and low-risk;
- postpone cloud and community-facing expansion until the local workflow is valuable.

## First Killer Scenario

```text
AI long-task review + prompt-driven notes + course/listening notes
```

FengVoice should become the commander log for AI collaboration:

1. Create a review note after a long AI-agent task.
2. Paste the Pi Agent / Codex / Kimi execution summary.
3. Use a static prompt template to turn the summary into structured review notes.
4. Tag the note with workflow, notes, decision, prompt, review, image, or audio.
5. Attach screenshots or audio when useful.
6. Decide whether the note becomes a GBrain candidate.

## Current P0 Use Cases

### AI Long-Task Execution Review

Record what was asked, which agent executed it, what changed, what passed, what failed, what decisions were made, and what should be done next.

### Prompt-Driven Notes

Use static templates to turn raw AI output or course material into structured notes. Dynamic placeholders can come later after the static workflow proves useful.

### Course and Listening Notes

Capture key points from lectures, videos, audio notes, or live learning sessions. Link audio assets when available, but do not block the note workflow on audio automation.

## Temporarily Paused

The following tracks are valuable but should not drive the next development loop:

- OSS application and open-source showcase polish.
- Public launch packaging.
- Vercel deployment optimization.
- Tencent Cloud deployment optimization.
- COS backup/storage integration.
- MCP adapter work.
- Multi-user system design.
- Complex prompt variable engines.

## Notebook Mode / GBrain Candidate Loop

Notebook Mode should be a cognitive organization layer, not an automatic code or production-memory writer.

Proposed loop:

```text
FengVoice note
  -> Notebook Mode review
  -> structured summary
  -> gbrain-candidate draft
  -> human approval
  -> long-term knowledge only when approved
```

Rules:

- Pi Agent can summarize, classify, and propose candidates.
- Pi Agent should not automatically modify business code.
- Pi Agent should not automatically write production GBrain.
- Human approval is required before long-term knowledge is committed.

## Success Standards

FengVoice succeeds in this phase when it is useful as a daily local note tool:

- The maintainer can open it every day.
- Creating a note is fast enough to use during real work.
- AI long-task summaries can be pasted and structured.
- Tags and search retrieve prior decisions.
- Images and audio can be associated with notes when needed.
- Local data can be backed up or exported safely.
- Notebook Mode can identify GBrain candidates without writing production memory automatically.
