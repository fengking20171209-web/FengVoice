# FengVoice Notebook Mode

## Purpose

Notebook Mode is the Pi Agent cognition layer for FengVoice personal notes. It helps organize notes, extract decisions, and propose long-term knowledge candidates.

Notebook Mode is not a business-code modifier, production-memory writer, crawler, or deployment agent.

## Core Rules

- Pi Agent acts as a cognitive organizer only.
- Pi Agent does not automatically modify `apps/web`, `services/api/main.py`, or `services/api/asset_index.py`.
- Pi Agent does not automatically write production GBrain.
- Pi Agent may generate `gbrain-candidate` drafts.
- Human approval is required before candidate knowledge becomes long-term memory.
- Pi Agent should not read `.env`, credentials, tokens, API keys, or private browser automation files.

## FengVoice Note Entry Flow

```text
FengVoice note
  -> user selects or copies note content
  -> Pi Agent Notebook Mode summarizes and classifies
  -> Pi Agent proposes actions or gbrain-candidate draft
  -> user approves, edits, or rejects
```

## AI Long-Task Review Flow

For the first killer scenario, Notebook Mode should process AI long-task review notes as commander logs.

Input note should include:

- task name;
- executing agent;
- task goal;
- input prompt or goal summary;
- execution result: PASS, WARN, or FAIL;
- key outputs;
- problems found;
- useful lessons;
- next actions;
- whether the note should become long-term knowledge.

Notebook Mode output may include:

```markdown
# gbrain-candidate

## Source note

## Candidate summary

## Why this should be remembered

## Suggested tags

## Human decision
- approve / revise / reject
```

## Candidate Criteria

A note is a good GBrain candidate when it records:

- a reusable project rule;
- a repeated workflow;
- a decision that affects future work;
- a reliable prompt pattern;
- a resolved failure mode;
- a safety boundary or validation rule.

A note should remain a normal FengVoice note when it is:

- temporary task chatter;
- incomplete raw output;
- private sensitive content;
- a one-off observation with no future value;
- not yet reviewed by a human.

## Safety Boundary

Notebook Mode must stop and ask for approval before:

- changing business code;
- changing data formats;
- writing production GBrain;
- reading secret-bearing files;
- connecting to cloud systems;
- committing or pushing Git changes;
- deleting notes, uploads, runtime data, or backups.

## Relationship to Personal Notes Roadmap

Notebook Mode starts in PN-1 as a manual review aid and becomes more important in PN-6 when selected notes are turned into candidate long-term knowledge.
