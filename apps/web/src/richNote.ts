export type ParagraphBlock = {
  type: "paragraph";
  text: string;
};

export type ImageBlock = {
  type: "image";
  url: string;
  alt: string;
  image_id: string;
};

export type RichNoteBlock = ParagraphBlock | ImageBlock;

export type RichNoteContentV1 = {
  version: 1;
  blocks: RichNoteBlock[];
};

const EMPTY_PARAGRAPH: ParagraphBlock = { type: "paragraph", text: "" };

export function createEmptyRichNote(): RichNoteContentV1 {
  return { version: 1, blocks: [{ ...EMPTY_PARAGRAPH }] };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function sniffRichNoteJson(content: string): boolean {
  const candidate = content.trimStart();
  return candidate.startsWith("{") && candidate.includes('"blocks"');
}

function normalizeParagraphText(value: unknown): string {
  if (typeof value === "string") return value;
  if (value === null || value === undefined) return "";
  return String(value);
}

function normalizeParagraphBlock(block: Record<string, unknown>): ParagraphBlock | null {
  if (block.type !== "paragraph") return null;
  return {
    type: "paragraph",
    text: normalizeParagraphText(block.text),
  };
}

function normalizeImageBlock(block: Record<string, unknown>): ImageBlock | null {
  if (block.type !== "image") return null;
  if (typeof block.url !== "string" || block.url.length === 0) return null;
  if (typeof block.image_id !== "string" || block.image_id.length === 0) return null;
  return {
    type: "image",
    url: block.url,
    alt: typeof block.alt === "string" ? block.alt : "pasted image",
    image_id: block.image_id,
  };
}

function normalizeBlock(block: unknown): RichNoteBlock | null {
  if (!isRecord(block)) return null;
  return normalizeParagraphBlock(block) ?? normalizeImageBlock(block);
}

export function ensureValidRichNote(value: unknown): RichNoteContentV1 {
  if (!isRecord(value) || value.version !== 1 || !Array.isArray(value.blocks)) {
    return createEmptyRichNote();
  }

  const blocks = value.blocks
    .map((block) => normalizeBlock(block))
    .filter((block): block is RichNoteBlock => block !== null);

  if (blocks.length === 0) return createEmptyRichNote();

  // Hard constraint 10: if last block is image, append trailing empty paragraph
  const lastBlock = blocks[blocks.length - 1];
  if (lastBlock.type === "image") {
    return { version: 1, blocks: [...blocks, { ...EMPTY_PARAGRAPH }] };
  }

  return { version: 1, blocks };
}

export function parseRichNoteContent(content: string): RichNoteContentV1 | null {
  if (!sniffRichNoteJson(content)) return null;

  try {
    return ensureValidRichNote(JSON.parse(content));
  } catch {
    return null;
  }
}

export function serializeRichNoteContent(value: RichNoteContentV1): string {
  return JSON.stringify(ensureValidRichNote(value));
}

export function appendImageBlock(
  value: RichNoteContentV1,
  image: { url: string; alt?: string; image_id: string },
): RichNoteContentV1 {
  const current = ensureValidRichNote(value);
  const imageBlock: ImageBlock = {
    type: "image",
    url: image.url,
    alt: typeof image.alt === "string" ? image.alt : "pasted image",
    image_id: image.image_id,
  };

  return {
    version: 1,
    blocks: [...current.blocks, imageBlock, { ...EMPTY_PARAGRAPH }],
  };
}
