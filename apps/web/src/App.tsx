import { type ClipboardEvent, useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  CheckCircle2,
  FileText,
  Mic,
  MicOff,
  Plus,
  Save,
  Search,
  Square,
  Trash2,
  Upload,
  Wifi,
  WifiOff,
  X,
} from "lucide-react";
import {
  checkHealth,
  createNote,
  deleteNote as deleteNoteRequest,
  listNotes,
  type Note,
  type NoteDraft,
  updateNote,
  uploadAudio,
  uploadNoteImage,
} from "./api";
import {
  firstImageFromClipboard,
  imageAltText,
  insertMarkdownAtSelection,
  markdownImage,
  toAbsoluteImageUrl,
} from "./imagePaste";
import {
  isAudioRecordingSupported,
  startAudioRecording,
  type AudioRecordingHandle,
} from "./audioRecord";
import { RichNoteEditor } from "./RichNoteEditor";

type SaveState = "idle" | "saving" | "saved" | "error" | "offline";
type Theme = "comfort" | "warm" | "light";
type Toast = { tone: "success" | "error"; message: string };

const emptyDraft = (): NoteDraft => ({
  title: "未命名笔记",
  content: "",
  note_type: "general",
  tags: [],
  status: "active",
});

const toDraft = (note: Note): NoteDraft => ({
  title: note.title,
  content: note.content,
  note_type: note.note_type,
  tags: note.tags,
  status: note.status,
});

const localNote = (): Note => {
  const timestamp = new Date().toISOString();
  return {
    id: `local-${crypto.randomUUID()}`,
    created_at: timestamp,
    updated_at: timestamp,
    local: true,
    ...emptyDraft(),
  };
};

export function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [draft, setDraft] = useState<NoteDraft>(emptyDraft());
  const [query, setQuery] = useState("");
  const [online, setOnline] = useState(false);
  const [dirty, setDirty] = useState(false);
  const [saveState, setSaveState] = useState<SaveState>("idle");
  const [error, setError] = useState("");
  const [toast, setToast] = useState<Toast | null>(null);
  const [theme, setTheme] = useState<Theme>(() => (localStorage.getItem("fengvoice-theme") as Theme) || "comfort");
  const titleRef = useRef<HTMLInputElement>(null);
  const contentRef = useRef<HTMLTextAreaElement>(null);
  const toastTimerRef = useRef<number | null>(null);
  const focusTitleRef = useRef(false);
  const selectedIdRef = useRef<string | null>(null);
  const draftRef = useRef(draft);
  const dirtyRef = useRef(false);
  const persistDraftRef = useRef<() => Promise<boolean>>(async () => true);
  const audioRecordingSupported = isAudioRecordingSupported();
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
  const [audioPreviewUrl, setAudioPreviewUrl] = useState<string | null>(null);
  const [uploadingAudio, setUploadingAudio] = useState(false);
  const recordingHandleRef = useRef<AudioRecordingHandle | null>(null);
  const recordingTimerRef = useRef<number | null>(null);

  useEffect(() => {
    selectedIdRef.current = selectedId;
    if (selectedId && focusTitleRef.current) {
      focusTitleRef.current = false;
      titleRef.current?.select();
    }
  }, [selectedId]);

  useEffect(() => {
    draftRef.current = draft;
  }, [draft]);

  useEffect(() => {
    dirtyRef.current = dirty;
  }, [dirty]);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem("fengvoice-theme", theme);
  }, [theme]);

  useEffect(() => {
    return () => {
      if (toastTimerRef.current) window.clearTimeout(toastTimerRef.current);
    };
  }, []);

  useEffect(() => {
    return () => {
      if (recordingTimerRef.current) window.clearInterval(recordingTimerRef.current);
      if (recordingHandleRef.current) void recordingHandleRef.current.stop().catch(() => undefined);
    };
  }, []);

  useEffect(() => {
    return () => {
      if (audioPreviewUrl) URL.revokeObjectURL(audioPreviewUrl);
    };
  }, [audioPreviewUrl]);

  function showToast(nextToast: Toast) {
    setToast(nextToast);
    if (toastTimerRef.current) window.clearTimeout(toastTimerRef.current);
    toastTimerRef.current = window.setTimeout(() => setToast(null), 2600);
  }

  const loadNotes = useCallback(async () => {
    try {
      const remoteNotes = await listNotes();
      setNotes((current) => [...current.filter((note) => note.local), ...remoteNotes]);
      setOnline(true);
    } catch (cause) {
      console.error("读取笔记失败", cause);
      setOnline(false);
      setError("无法读取服务器笔记，本地草稿仍可编辑。");
    }
  }, []);

  useEffect(() => {
    checkHealth()
      .then(() => setOnline(true))
      .catch((cause) => {
        console.error("API 健康检查失败", cause);
        setOnline(false);
      });
    loadNotes();
  }, [loadNotes]);

  const replaceNote = useCallback((note: Note, previousId = note.id) => {
    setNotes((current) =>
      [note, ...current.filter((item) => item.id !== previousId && item.id !== note.id)]
        .sort((a, b) => b.updated_at.localeCompare(a.updated_at)),
    );
  }, []);

  const persistDraft = useCallback(async (id = selectedIdRef.current, currentDraft = draftRef.current) => {
    if (!id || !dirtyRef.current) return true;
    setSaveState("saving");
    setError("");
    try {
      const saved = id.startsWith("local-")
        ? await createNote(currentDraft)
        : await updateNote(id, currentDraft);
      replaceNote(saved, id);
      setSelectedId((current) => (current === id ? saved.id : current));
      setDirty(false);
      dirtyRef.current = false;
      setOnline(true);
      setSaveState("saved");
      return true;
    } catch (cause) {
      console.error("保存笔记失败", cause);
      setOnline(false);
      setSaveState(id.startsWith("local-") ? "offline" : "error");
      setError(id.startsWith("local-") ? "创建失败，已保留为离线草稿。" : "保存失败，内容仍保留在当前页面。");
      return false;
    }
  }, [replaceNote]);

  useEffect(() => {
    persistDraftRef.current = () => persistDraft();
  }, [persistDraft]);

  useEffect(() => {
    function handleKeydown(event: KeyboardEvent) {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {
        event.preventDefault();
        void persistDraftRef.current();
      }
      if (event.key === "Escape") setError("");
    }
    window.addEventListener("keydown", handleKeydown);
    return () => window.removeEventListener("keydown", handleKeydown);
  }, []);

  useEffect(() => {
    if (!dirty || !selectedId) return;
    const timer = window.setTimeout(() => void persistDraft(), 800);
    return () => window.clearTimeout(timer);
  }, [dirty, draft, persistDraft, selectedId]);

  const visibleNotes = useMemo(() => {
    const term = query.trim().toLowerCase();
    if (!term) return notes;
    return notes.filter((note) =>
      [note.title, note.content, note.note_type, note.tags.join(" ")].some((value) =>
        value.toLowerCase().includes(term),
      ),
    );
  }, [notes, query]);

  function updateDraft(changes: Partial<NoteDraft>) {
    const nextDraft = { ...draftRef.current, ...changes };
    draftRef.current = nextDraft;
    setDraft(nextDraft);
    setDirty(true);
    dirtyRef.current = true;
    setSaveState("idle");
  }

  async function handleContentPaste(event: ClipboardEvent<HTMLTextAreaElement>) {
    const imageFile = firstImageFromClipboard(event.clipboardData.items);
    if (!imageFile) return;

    event.preventDefault();
    const start = event.currentTarget.selectionStart;
    const end = event.currentTarget.selectionEnd;

    try {
      const uploaded = await uploadNoteImage(imageFile);
      const absoluteUrl = toAbsoluteImageUrl(uploaded.url);
      const alt = imageAltText(uploaded, imageFile);
      const markdown = markdownImage(absoluteUrl, alt);
      updateDraft({
        content: insertMarkdownAtSelection(draftRef.current.content, markdown, start, end),
      });
      showToast({ tone: "success", message: "图片上传成功" });
      window.requestAnimationFrame(() => contentRef.current?.focus());
    } catch (cause) {
      console.error("Image paste upload failed", cause);
      showToast({ tone: "error", message: "图片上传失败，请重试" });
      setError("图片上传失败，请重试");
    }
  }

  async function handleStartRecording() {
    try {
      if (audioPreviewUrl) URL.revokeObjectURL(audioPreviewUrl);
      setAudioPreviewUrl(null);
      setAudioBlob(null);
      setRecordingTime(0);
      recordingHandleRef.current = await startAudioRecording();
      setIsRecording(true);
      recordingTimerRef.current = window.setInterval(() => {
        setRecordingTime((current) => current + 1);
      }, 1000);
    } catch (cause) {
      console.error("Audio recording failed to start", cause);
      showToast({ tone: "error", message: "Audio recording is unavailable" });
      setError("Audio recording is unavailable. Check browser support and microphone permission.");
    }
  }

  async function handleStopRecording() {
    const handle = recordingHandleRef.current;
    if (!handle) return;

    try {
      const blob = await handle.stop();
      setAudioBlob(blob);
      setAudioPreviewUrl(URL.createObjectURL(blob));
    } catch (cause) {
      console.error("Audio recording failed to stop", cause);
      showToast({ tone: "error", message: "Audio recording failed" });
      setError("Audio recording failed. Please try again.");
    } finally {
      recordingHandleRef.current = null;
      setIsRecording(false);
      if (recordingTimerRef.current) {
        window.clearInterval(recordingTimerRef.current);
        recordingTimerRef.current = null;
      }
    }
  }

  async function handleUploadAudio() {
    if (!audioBlob) return;

    setUploadingAudio(true);
    try {
      const uploaded = await uploadAudio(audioBlob);
      const start = contentRef.current?.selectionStart;
      const end = contentRef.current?.selectionEnd;
      const markdown = `[Audio note](${uploaded.public_url})`;
      updateDraft({
        content: insertMarkdownAtSelection(draftRef.current.content, markdown, start, end),
      });
      showToast({ tone: "success", message: "Audio uploaded" });
      setAudioBlob(null);
      if (audioPreviewUrl) URL.revokeObjectURL(audioPreviewUrl);
      setAudioPreviewUrl(null);
      window.requestAnimationFrame(() => contentRef.current?.focus());
    } catch (cause) {
      console.error("Audio upload failed", cause);
      showToast({ tone: "error", message: "Audio upload failed" });
      setError("Audio upload failed. Please try again.");
    } finally {
      setUploadingAudio(false);
    }
  }

  function formatRecordingTime(seconds: number) {
    const minutes = Math.floor(seconds / 60);
    const rest = seconds % 60;
    return `${minutes.toString().padStart(2, "0")}:${rest.toString().padStart(2, "0")}`;
  }

  function resetAudioCapture() {
    if (recordingTimerRef.current) {
      window.clearInterval(recordingTimerRef.current);
      recordingTimerRef.current = null;
    }
    if (recordingHandleRef.current) void recordingHandleRef.current.stop().catch(() => undefined);
    if (audioPreviewUrl) URL.revokeObjectURL(audioPreviewUrl);
    recordingHandleRef.current = null;
    setIsRecording(false);
    setRecordingTime(0);
    setAudioBlob(null);
    setAudioPreviewUrl(null);
    setUploadingAudio(false);
  }

  async function newNote() {
    await persistDraft();
    resetAudioCapture();
    const note = localNote();
    setNotes((current) => [note, ...current]);
    setSelectedId(note.id);
    setDraft(toDraft(note));
    draftRef.current = toDraft(note);
    setDirty(true);
    dirtyRef.current = true;
    setSaveState("saving");
    setError("");
    focusTitleRef.current = true;
    await persistDraft(note.id, toDraft(note));
  }

  async function selectNote(note: Note) {
    if (note.id === selectedIdRef.current) return;
    await persistDraft();
    resetAudioCapture();
    setSelectedId(note.id);
    setDraft(toDraft(note));
    draftRef.current = toDraft(note);
    setDirty(false);
    dirtyRef.current = false;
    setSaveState(note.local ? "offline" : "saved");
    setError("");
  }

  async function removeNote() {
    const id = selectedIdRef.current;
    if (!id || !confirm("删除这条笔记？")) return;
    try {
      if (!id.startsWith("local-")) await deleteNoteRequest(id);
      setNotes((current) => current.filter((note) => note.id !== id));
      setSelectedId(null);
      setDraft(emptyDraft());
      resetAudioCapture();
      setDirty(false);
      dirtyRef.current = false;
      setSaveState("idle");
      setError("");
    } catch (cause) {
      console.error("删除笔记失败", cause);
      setError("删除失败，请检查 API 连接后重试。");
      setSaveState("error");
    }
  }

  const selectedNote = notes.find((note) => note.id === selectedId) ?? null;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">FV</div>
          <div>
            <h1>FengVoice</h1>
            <p>Notes workspace</p>
          </div>
        </div>
        <div className={`connection ${online ? "online" : "offline"}`}>
          {online ? <Wifi size={15} /> : <WifiOff size={15} />}
          <span>{online ? "API 已连接" : "API 未连接"}</span>
        </div>
        <button className="primary-button" onClick={() => void newNote()}>
          <Plus size={17} />
          新建笔记
        </button>
        <label className="search">
          <Search size={16} />
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索笔记" />
          {query && (
            <button title="清空搜索" onClick={() => setQuery("")}>
              <X size={15} />
            </button>
          )}
        </label>
        <div className="notes-list">
          {visibleNotes.length === 0 ? (
            <div className="empty-list">
              <strong>还没有笔记</strong>
              <span>点击“新建笔记”开始记录你的第一个想法。</span>
            </div>
          ) : (
            visibleNotes.map((note) => (
              <button
                className={`note-item ${selectedId === note.id ? "selected" : ""}`}
                key={note.id}
                onClick={() => void selectNote(note)}
              >
                <div className="note-item-heading">
                  <FileText size={15} />
                  <strong>{note.title}</strong>
                  <em>{note.local ? "离线" : note.note_type}</em>
                </div>
                <span>{note.content || "暂无内容"}</span>
                <small>{new Date(note.updated_at).toLocaleString("zh-CN")}</small>
              </button>
            ))
          )}
        </div>
        <div className="theme-control">
          <span>主题亮度</span>
          <div>
            {([
              ["comfort", "深色"],
              ["warm", "暖灰"],
              ["light", "浅色"],
            ] as const).map(([value, label]) => (
              <button className={theme === value ? "active" : ""} key={value} onClick={() => setTheme(value)}>
                {label}
              </button>
            ))}
          </div>
        </div>
      </aside>

      <main className="editor">
        <header className="editor-header">
          <div>
            <p className="eyebrow">{selectedId ? "编辑笔记" : "Notes"}</p>
            <h2>{draft.title || "未命名笔记"}</h2>
          </div>
          <div className="actions">
            <span className={`save-status ${saveState}`}>
              {saveState === "saving" && "保存中..."}
              {saveState === "saved" && <><CheckCircle2 size={15} /> 已保存</>}
              {saveState === "offline" && "离线草稿"}
              {saveState === "error" && "保存失败"}
              {saveState === "idle" && (dirty ? "尚未保存" : "状态：就绪")}
            </span>
            {audioRecordingSupported && !isRecording && (
              <button className="icon-button" onClick={() => void handleStartRecording()} disabled={!selectedId} title="Record audio">
                <Mic size={18} />
              </button>
            )}
            {isRecording && (
              <button className="icon-button recording" onClick={() => void handleStopRecording()} title="Stop recording">
                <Square size={18} />
              </button>
            )}
            {!audioRecordingSupported && (
              <button className="icon-button" disabled title="Audio recording is not supported">
                <MicOff size={18} />
              </button>
            )}
            {selectedId && (
              <button className="icon-button danger" onClick={() => void removeNote()} title="删除笔记">
                <Trash2 size={18} />
              </button>
            )}
            <button className="save-button" onClick={() => void persistDraft()} disabled={!selectedId || !dirty || saveState === "saving"}>
              <Save size={17} />
              保存笔记
            </button>
          </div>
        </header>
        {error && (
          <div className="error-banner">
            <span>{error}</span>
            <button onClick={() => setError("")} title="关闭提示"><X size={16} /></button>
          </div>
        )}
        {toast && <div className={`toast ${toast.tone}`}>{toast.message}</div>}
        <section className="editor-body">
          {!selectedId && <p className="editor-empty">从左侧新建一条笔记，开始记录今天的想法。</p>}
          <input
            ref={titleRef}
            className="title-input"
            value={draft.title}
            onChange={(event) => updateDraft({ title: event.target.value })}
            placeholder="笔记标题"
            disabled={!selectedId}
          />
          <div className="meta-row">
            <select value={draft.note_type} onChange={(event) => updateDraft({ note_type: event.target.value })} disabled={!selectedId}>
              <option value="general">普通笔记</option>
              <option value="engineering">工程笔记</option>
              <option value="content">内容笔记</option>
              <option value="prompt">Prompt</option>
              <option value="rich_note">图文笔记</option>
            </select>
            <input
              value={draft.tags.join(", ")}
              onChange={(event) =>
                updateDraft({ tags: event.target.value.split(",").map((tag) => tag.trim()).filter(Boolean) })
              }
              placeholder="标签，用逗号分隔"
              disabled={!selectedId}
            />
          </div>
          {draft.note_type === "rich_note" ? (
            <RichNoteEditor
              content={draft.content}
              onChange={(serialized) => updateDraft({ content: serialized })}
            />
          ) : (
            <textarea
              ref={contentRef}
              value={draft.content}
              onChange={(event) => updateDraft({ content: event.target.value })}
              onPaste={(event) => void handleContentPaste(event)}
              placeholder="记录想法、决策、内容草稿……"
              disabled={!selectedId}
            />
          )}
          {isRecording && (
            <div className="recording-indicator">
              <span className="recording-dot" />
              <span>Recording {formatRecordingTime(recordingTime)}</span>
            </div>
          )}
          {audioPreviewUrl && !isRecording && (
            <div className="audio-preview">
              <audio controls src={audioPreviewUrl} />
              <button className="primary-button" onClick={() => void handleUploadAudio()} disabled={uploadingAudio}>
                <Upload size={15} />
                {uploadingAudio ? "Uploading" : "Upload audio"}
              </button>
            </div>
          )}
          {selectedNote?.local && <p className="local-hint">这条笔记仍保存在当前页面中，API 恢复后点击“保存笔记”即可同步。</p>}
        </section>
      </main>
    </div>
  );
}
