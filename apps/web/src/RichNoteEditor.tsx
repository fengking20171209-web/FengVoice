import { useMemo } from "react";
import {
  firstImageFromClipboard,
} from "./imagePaste";
import {
  parseRichNoteContent,
  serializeRichNoteContent,
  createEmptyRichNote,
  RichNoteContentV1,
} from "./richNote";

export type RichNoteEditorProps = {
  content: string;
  onChange: (serializedContent: string) => void;
  onImagePaste?: (file: File) => Promise<void>;
};

const FALLBACK_MESSAGE =
  "检测到此笔记内容不是图文 Block JSON。为避免丢失内容，已切换到安全文本视图。如需体验图文 Block 模式，请新建\u201c图文笔记\u201d。";

/**
 * Controlled rich note editor component.
 *
 * - Accepts raw JSON string content via props.
 * - For valid RichNoteContentV1 JSON, renders paragraph textareas and image
 *   blocks in a vertical list.
 * - For invalid / non-JSON content, shows a safe fallback textarea with the
 *   original raw content.
 * - For empty content, creates a single empty paragraph block.
 *
 * v1 key strategy: `{block.type}-{index}`. No persisted block id in JSON.
 */
export function RichNoteEditor(props: RichNoteEditorProps) {
  const { content, onChange, onImagePaste } = props;

  // Parse content once per string identity change.
  // Returns RichNoteContentV1 for valid / empty content, or null for invalid.
  const richContent = useMemo<RichNoteContentV1 | null>(() => {
    if (!content) return createEmptyRichNote();
    return parseRichNoteContent(content);
  }, [content]);

  // --- Invalid JSON fallback state ---

  if (richContent === null) {
    return (
      <div className="rich-note-editor">
        <div className="rich-note-fallback">
          <p className="rich-note-fallback-message">{FALLBACK_MESSAGE}</p>
          <textarea
            className="rich-note-fallback-textarea"
            value={content}
            onChange={(e) => onChange(e.target.value)}
          />
        </div>
      </div>
    );
  }

  // --- Normal block rendering ---

  const contentValue = richContent;

  function handleParagraphChange(index: number, text: string): void {
    const nextBlocks = contentValue.blocks.map((block, i) => {
      if (i === index && block.type === "paragraph") {
        return { type: "paragraph" as const, text };
      }
      return block;
    });
    onChange(
      serializeRichNoteContent({ version: 1, blocks: nextBlocks }),
    );
  }

  return (
    <div
      className="rich-note-editor"
      onPaste={(event) => {
        if (!onImagePaste) return;
        const imageFile = firstImageFromClipboard(event.clipboardData?.items);
        if (!imageFile) return;
        event.preventDefault();
        void onImagePaste(imageFile);
      }}
    >
      {richContent.blocks.map((block, index) => (
        <div className="rich-note-block" key={`${block.type}-${index}`}>
          {block.type === "paragraph" ? (
            <textarea
              className="rich-note-paragraph"
              value={block.text}
              onChange={(e) => handleParagraphChange(index, e.target.value)}
            />
          ) : (
            <img
              className="rich-note-image"
              src={block.url}
              alt={block.alt}
              onError={(e) => {
                e.currentTarget.style.display = "none";
                const fallback = document.createElement("div");
                fallback.className = "rich-note-image-fallback";
                fallback.textContent = `⚠ Image block: ${block.alt || "pasted image"}`;
                e.currentTarget.parentElement?.replaceChild(fallback, e.currentTarget);
              }}
            />
          )}
        </div>
      ))}
    </div>
  );
}

export default RichNoteEditor;