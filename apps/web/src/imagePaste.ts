export type ImageUploadResult = {
  url: string;
  alt?: string;
};

export function toAbsoluteImageUrl(path: string, origin = window.location.origin) {
  if (/^https?:\/\//i.test(path)) return path;
  return new URL(path, origin).toString();
}

export function imageAltText(upload: ImageUploadResult, file?: File) {
  const fallback = file?.name
    ?.replace(/\.[^.]+$/, "")
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
  return upload.alt?.trim() || fallback || "pasted image";
}

export function markdownImage(url: string, alt: string) {
  return `![${alt.replace(/[\[\]\n\r]/g, " ").trim() || "pasted image"}](${url})`;
}

export function insertMarkdownAtSelection(content: string, markdown: string, start?: number | null, end?: number | null) {
  const insertion = `\n\n${markdown}\n\n`;
  if (typeof start !== "number" || typeof end !== "number") {
    return `${content}${insertion}`;
  }
  return `${content.slice(0, start)}${insertion}${content.slice(end)}`;
}

export function firstImageFromClipboard(items: DataTransferItemList) {
  for (const item of Array.from(items)) {
    if (item.kind === "file" && item.type.startsWith("image/")) {
      return item.getAsFile();
    }
  }
  return null;
}
