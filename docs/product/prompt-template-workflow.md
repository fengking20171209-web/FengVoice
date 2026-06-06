# FengVoice Prompt Template Workflow

## Role in Personal Notes

Prompt templates help turn raw work output into reusable personal notes. In the personal-notes-first phase, templates are not a feature showcase. They are a practical way to make repeated note types fast and consistent.

Primary template uses:

- AI long-task execution review.
- Prompt-driven decision notes.
- Course and listening-note summaries.
- Community command or resource triage from manually selected URLs.

## Current Stage: Static Templates Only

The current phase should use simple Markdown templates stored in docs or copied manually into notes.

Rules:

- No complex variable engine.
- No automatic remote fetching.
- No background crawler.
- No production GBrain write.
- Human decides what source material enters a note.

## Later: Dynamic Placeholders

Dynamic placeholders may be useful after the static workflow proves valuable.

Possible future placeholders:

```text
{{task_name}}
{{agent_name}}
{{date}}
{{result_status}}
{{source_url}}
{{tags}}
{{gbrain_candidate}}
```

This should not be implemented until PN-1 and PN-4 show repeated real use.

## Example: Community Command Collection Filter

Use this when the user manually provides a URL or copied text. Do not crawl broad communities automatically.

```markdown
# Community Resource Filter

## Source
- URL or copied source:

## Why this source matters

## Useful commands / prompts / patterns

## Noise to ignore

## Security or trust concerns

## Should FengVoice keep this?
- no / candidate

## Tags
- research
- prompt
- review
```

## Example: AI Long-Task Review Organizer

```markdown
Turn the following AI-agent execution summary into a FengVoice commander-log note.

Rules:
- Keep factual outputs separate from opinions.
- Mark result as PASS, WARN, or FAIL.
- Extract next actions as checkable bullets.
- Identify whether any item should become a GBrain candidate.
- Use only these tags: workflow, notes, decision, prompt, research, review, audio, image, general.

Input:
<<< paste execution summary here >>>
```

## Not Doing

- No complex variable engine.
- No MCP adapter.
- No browser automation for resource harvesting.
- No automatic publishing.
- No hidden background writes to long-term memory.
