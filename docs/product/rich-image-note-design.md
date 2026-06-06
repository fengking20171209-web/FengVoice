# Rich Image Note Design

## Goal

Add a lightweight rich image note mode so FengVoice can support OneNote-style mixed text and images:

```text
text
image
text under the image
another image
more notes
```

The first version should be small and practical. It should make pasted images visible inside the note flow while preserving the existing plain-text / Markdown note behavior.

## Non-Goals

Do not build a full rich-text editor in the first version.

Out of scope for v1:

- drag-and-drop block reorder;
- image resizing;
- columns or canvas layout;
- tables;
- handwriting or drawing;
- complex rich text formatting;
- collaborative editing;
- cloud storage or COS integration;
- API asset format changes unless explicitly planned.

## New Note Mode

Use a distinct note type for rich image notes:

```text
note_type = rich_note
```

Display name:

```text
图文笔记
```

Existing note types continue to behave as text / Markdown notes.

## Data Model

Keep the existing note API shape for the first version. Store the rich note body as JSON inside the existing `content` string field.

Example `content` value:

```json
{
  "version": 1,
  "blocks": [
    {
      "type": "paragraph",
      "text": "这里是图片上方的说明。"
    },
    {
      "type": "image",
      "url": "http://localhost:8000/uploads/notes/example.png",
      "alt": "pasted image",
      "image_id": "img_example"
    },
    {
      "type": "paragraph",
      "text": "这里是图片下方的补充笔记。"
    }
  ]
}
```

This avoids a database schema change in the first version.

## Block Types for v1

### Paragraph Block

```ts
type ParagraphBlock = {
  type: "paragraph";
  text: string;
};
```

Purpose:

- write normal text;
- continue writing below an image;
- keep the editing experience simple.

### Image Block

```ts
type ImageBlock = {
  type: "image";
  url: string;
  alt: string;
  image_id: string;
};
```

Purpose:

- display pasted image inline;
- keep existing upload and asset index behavior;
- preserve stable `image_id` returned by the API.

## Editing Flow

For a `rich_note`:

1. The editor renders a vertical list of blocks.
2. Paragraph blocks render as textareas or simple text inputs.
3. Image blocks render as actual images.
4. When the user pastes an image while editing a rich note:
   - upload the image through the existing image upload API;
   - append or insert an image block at the current position;
   - create a blank paragraph block after the image;
   - focus that paragraph so the user can immediately write notes under the image.

## Compatibility

Plain notes remain unchanged.

- Existing Markdown notes continue to store plain text in `content`.
- Existing image paste behavior for Markdown notes should continue inserting:

```markdown
![pasted image](http://localhost:8000/uploads/notes/example.png)
```

Rich notes use JSON content only when `note_type === "rich_note"`.

If a `rich_note` contains invalid JSON, the UI should fail safely by showing a text fallback and a warning rather than losing content.

## API Impact

First version should avoid API changes.

Use existing endpoints:

- `POST /api/uploads/images`
- `POST /api/notes`
- `PUT /api/notes/{id}`
- `GET /api/notes`

Preserve existing invariants:

- image paste upload behavior;
- stable `image_id`;
- Markdown image insertion for non-rich notes;
- JSONL asset index append behavior;
- existing upload validation.

## UI Scope for v1

Minimum usable UI:

- note type selector includes `图文笔记` / `rich_note`;
- rich note editor displays paragraph and image blocks in one vertical flow;
- image blocks display the actual image;
- paragraph below image is editable;
- save writes JSON content to the existing note `content` field;
- switching away and back reloads the same blocks.

## Validation Plan

Manual validation:

1. Create a new `图文笔记`.
2. Type text in the first paragraph.
3. Paste an image.
4. Confirm image is displayed inline.
5. Type text under the image.
6. Save the note.
7. Reload notes.
8. Confirm text and image blocks are still present.
9. Confirm `runtime/asset-index/` receives an image record.
10. Confirm `public/uploads/` receives the uploaded file but remains ignored by Git.

Automated or script validation later:

- rich note JSON parser accepts valid v1 blocks;
- invalid rich note content falls back safely;
- Markdown notes still insert image Markdown;
- rich notes insert image blocks.

## Risks

| Risk | Mitigation |
| --- | --- |
| JSON content may be hard to edit manually | Keep fallback text view and avoid schema changes in v1. |
| Rich note editor may grow complex | Limit v1 to paragraph + image blocks only. |
| Existing Markdown flow may regress | Keep Markdown notes on existing path and add focused tests. |
| Images may upload but not render | Validate image URL with browser and API health checks. |

## Recommended Implementation Order

1. Add small rich-note block parser/serializer helpers in the web app.
2. Add a lightweight rich-note editor component.
3. Route `note_type === "rich_note"` to the rich editor.
4. Wire image paste in rich notes to create image blocks.
5. Add focused validation and manual test notes.

## Decision

Proceed with a lightweight rich image note mode using `note_type = rich_note` and JSON blocks stored in the existing `content` field.

Do not change the database schema or API in v1.
