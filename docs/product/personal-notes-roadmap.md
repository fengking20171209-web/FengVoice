# FengVoice Personal Notes Roadmap

## PN-0: Local Startup Acceptance

**Goal:** Prove FengVoice starts locally and can be used without cloud services.

**Input:** Current repo, local Python/Node environment, existing API and web app instructions.

**Output:** A short acceptance record showing API, web, and core note flow status.

**Acceptance Standards:**

- API starts on `127.0.0.1:8000`.
- Web app starts on `127.0.0.1:5173`.
- Health endpoint responds.
- The web UI loads.
- No runtime/upload/generated files are committed.

**Not Doing:**

- No Docker.
- No SSH.
- No Tencent Cloud.
- No Vercel deployment.
- No schema migration.

## PN-1: AI Long-Task Review Note Loop

**Goal:** Make the first killer scenario usable: AI long-task review, prompt-driven structuring, and tags.

**Input:** One real Pi Agent / Codex / Kimi long-task summary and the AI long-task review template.

**Output:** One structured commander-log note with tags and next actions.

**Acceptance Standards:**

- A note can record task name, agent, goal, result, outputs, problems, lessons, and next steps.
- Tags include only approved labels such as `workflow`, `notes`, `decision`, `prompt`, `review`, `image`, `audio`, or `general`.
- The note can be found later by search or tag.
- The note can be marked as `no` or `candidate` for long-term knowledge.

**Not Doing:**

- No dynamic prompt variable engine.
- No automatic GBrain writes.
- No new code unless a focused issue is approved later.

## PN-2: Core Notes Function Loop

**Goal:** Verify the ordinary note operations that make daily use practical.

**Input:** Several short real notes, including work decisions and course notes.

**Output:** A small local notebook with searchable and tagged notes.

**Acceptance Standards:**

- Create, edit, save, search, tag, pin, and recover/trash flows are checked.
- Known missing behavior is recorded as PN-5 fix candidates.
- The user can continue using the app despite non-blocking defects.

**Not Doing:**

- No multi-user collaboration.
- No cloud sync.
- No database schema changes without a separate issue.

## PN-3: Image and Audio Asset Loop

**Goal:** Validate that visual and audio context can support notes.

**Input:** One screenshot/image paste and one audio recording or upload sample when available.

**Output:** Notes with linked image/audio assets and an asset-index validation record.

**Acceptance Standards:**

- Image paste works and returns a usable Markdown URL.
- Image asset index records are appended and validated.
- Audio recording/upload status is documented honestly.
- Missing audio behavior becomes a scoped follow-up, not a blocker for notes.

**Not Doing:**

- No COS integration.
- No public media CDN.
- No bulk migration unless explicitly planned.

## PN-4: Real Small-Sample Notes

**Goal:** Use FengVoice with real data for several days.

**Input:** Three days of AI task reviews, prompt notes, decisions, and learning notes.

**Output:** A small sample corpus that exposes real usability issues.

**Acceptance Standards:**

- At least five meaningful personal notes exist locally.
- At least one AI long-task review note is completed.
- At least one prompt template note is completed.
- At least one course/listening note is completed.
- Pain points are ranked by real frequency and severity.

**Not Doing:**

- No polishing for imagined users.
- No broad refactor.
- No public demo obligation.

## PN-5: Experience Repair

**Goal:** Fix only the issues that block daily use.

**Input:** PN-4 pain-point list.

**Output:** Small, reviewable fixes tied to concrete acceptance criteria.

**Acceptance Standards:**

- Each fix has one issue or one clear maintenance note.
- Each fix preserves note, image, and asset-index invariants.
- Relevant validation is run and recorded.

**Not Doing:**

- No speculative feature expansion.
- No unrelated UI redesign.
- No behavior changes without validation.

## PN-6: GBrain Candidate Sedimentation

**Goal:** Turn selected notes into candidate long-term knowledge without automatic production writes.

**Input:** Completed AI task reviews and decision notes.

**Output:** Human-reviewed `gbrain-candidate` summaries.

**Acceptance Standards:**

- Candidate reason is explicit.
- Source note is referenced.
- Human approval is required before long-term knowledge is written.
- Rejected candidates remain useful as normal notes.

**Not Doing:**

- No automatic production GBrain writes.
- No secret extraction.
- No background crawler.
