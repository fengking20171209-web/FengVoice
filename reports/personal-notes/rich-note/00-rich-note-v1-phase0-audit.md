# Rich Image Note v1 Phase 0 Audit

## Result

WARN — implementation should be split before editing `App.tsx`.

This audit inspected the current web structure for the lightweight rich image note feature. No business code was changed.

## Current Web Files

```text
apps/web/src/App.tsx          571 lines
apps/web/src/api.ts            96 lines
apps/web/src/audioRecord.ts    75 lines
apps/web/src/imagePaste.ts     39 lines
apps/web/src/main.tsx
apps/web/src/styles.css       132 lines
apps/web/src/vite-env.d.ts
```

## Relevant Existing Behavior

### API client

`apps/web/src/api.ts` defines:

- `Note`
- `NoteDraft`
- `uploadNoteImage(file)`
- `createNote(draft)`
- `updateNote(id, draft)`

No backend API change is needed for v1 because rich note JSON can be stored in the existing `content` string.

### Image paste helpers

`apps/web/src/imagePaste.ts` already provides:

- `firstImageFromClipboard(items)`
- `markdownImage(url, alt)`
- `insertMarkdownAtSelection(content, markdown, start, end)`

These are Markdown-specific today. Rich note v1 should reuse `firstImageFromClipboard`, but should not reuse `insertMarkdownAtSelection` for `rich_note` image blocks.

### App coupling

`apps/web/src/App.tsx` currently owns:

- note list state;
- selected note state;
- `draft` state;
- autosave;
- new note creation;
- note selection;
- Markdown textarea rendering;
- image paste upload;
- audio recording integration;
- delete flow;
- layout rendering.

Important lines / responsibilities found:

- `emptyDraft()` defaults `note_type` to `general`.
- `toDraft(note)` maps note content directly into textarea content.
- `contentRef` is a single textarea ref.
- `handleContentPaste()` uploads an image and inserts Markdown.
- the note type selector currently contains `general`, `content`, `prompt`, `idea`, `task`.
- the main editor always renders a single `<textarea>` for `draft.content`.

## Risk Assessment

Directly implementing rich note behavior inside `App.tsx` would touch several coupled areas at once:

- note type selector;
- content rendering;
- paste handling;
- autosave state;
- draft serialization;
- focus behavior;
- styles.

That is risky because Markdown notes must not regress.

## Recommended File Split Before Feature Work

Create focused frontend files:

```text
apps/web/src/richNote.ts
apps/web/src/RichNoteEditor.tsx
```

Optional later:

```text
apps/web/src/richNoteValidation.ts
```

### `richNote.ts`

Responsibilities:

- define `RichNoteContent`, `RichNoteBlock`, `ParagraphBlock`, `ImageBlock`;
- `createEmptyRichNote()`;
- `parseRichNoteContent(raw: string)`;
- `serializeRichNoteContent(content: RichNoteContent)`;
- `appendImageBlock(...)` or `insertImageBlockAfter(...)`;
- guarantee empty-block fallback.

Must preserve paragraph text exactly, including internal `\n`.

### `RichNoteEditor.tsx`

Responsibilities:

- render paragraph blocks as textareas;
- render image blocks as actual images;
- handle rich note image paste by calling `uploadNoteImage` and inserting an image block;
- create a blank paragraph block after a pasted image;
- surface invalid JSON fallback without discarding original content.

### `App.tsx` minimal integration

Keep `App.tsx` changes narrow:

- add `rich_note` option to note type selector;
- if `draft.note_type === "rich_note"`, render `RichNoteEditor`;
- otherwise keep current Markdown textarea and current `handleContentPaste()` behavior;
- update `draft.content` from serialized rich note content.

## Required go9 Constraints

Implementation must include these constraints:

1. Paragraph internal newlines must be preserved.
2. Empty blocks must fall back to `createEmptyRichNote()` with one blank paragraph.
3. Orphan uploaded images are a known v1 limitation; do not delete uploads.
4. Invalid rich JSON must show a friendly fallback text view and must not overwrite original content automatically.
5. Markdown notes must continue inserting Markdown image syntax.

Friendly fallback message:

```text
检测到此笔记内容不是图文 Block JSON。为避免丢失内容，已切换到安全文本视图。如需体验图文 Block 模式，请新建“图文笔记”。
```

## Suggested Commit Split

1. `feat(web): add rich note block helpers`
2. `feat(web): add lightweight rich note editor`
3. `feat(web): support image blocks in rich notes`

## Validation Requirements

Add validation evidence for:

- paragraph multiline save/load;
- empty blocks fallback;
- invalid JSON fallback;
- orphan upload limitation documented;
- ordinary Markdown image paste still inserts `![pasted image](url)`;
- no backend API or DB schema change;
- no committed runtime uploads.

## Stop Point

Stop after this audit before implementation.

Reason: `App.tsx` is large enough that rich note work should be split into helper/component tasks rather than implemented as one large edit.
