export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type Note = {
  id: string;
  title: string;
  content: string;
  note_type: string;
  tags: string[];
  status: string;
  created_at: string;
  updated_at: string;
  local?: boolean;
};

export type NoteDraft = Pick<Note, "title" | "content" | "note_type" | "tags" | "status">;

export type UploadedImage = {
  url: string;
  alt: string;
  image_id: string;
};

export type UploadedAudio = {
  audio_id: string;
  public_url: string;
  mime_type: string;
  size_bytes: number;
  sha256: string;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  if (!response.ok) {
    throw new Error(`API ${response.status}: ${response.statusText}`);
  }
  return response.status === 204 ? (undefined as T) : response.json();
}

export function checkHealth() {
  return request<{ status: string; service: string }>("/health");
}

export function listNotes() {
  return request<Note[]>("/api/notes");
}

export function createNote(draft: NoteDraft) {
  return request<Note>("/api/notes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(draft),
  });
}

export function updateNote(id: string, draft: NoteDraft) {
  return request<Note>(`/api/notes/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(draft),
  });
}

export function deleteNote(id: string) {
  return request<void>(`/api/notes/${id}`, { method: "DELETE" });
}

export function uploadNoteImage(file: File) {
  const body = new FormData();
  body.append("file", file);
  return request<UploadedImage>("/api/uploads/images", {
    method: "POST",
    body,
  });
}

export function uploadAudio(blob: Blob) {
  const mimeType = blob.type.split(";")[0] || "audio/webm";
  const extension = mimeType.includes("ogg")
    ? "ogg"
    : mimeType.includes("mp4")
      ? "m4a"
      : mimeType.includes("wav")
        ? "wav"
        : mimeType.includes("mpeg")
          ? "mp3"
          : "webm";
  const file = new File([blob], `recording-${Date.now()}.${extension}`, { type: mimeType });
  const body = new FormData();
  body.append("file", file);
  return request<UploadedAudio>("/api/notes/audio", {
    method: "POST",
    body,
  });
}

