import { useCallback, useEffect, useMemo, useState } from "react";
import { FileText, Plus, Save, Search, Trash2, Wifi, WifiOff } from "lucide-react";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

type Note = {
  id: string;
  title: string;
  content: string;
  note_type: string;
  tags: string[];
  status: string;
  created_at: string;
  updated_at: string;
};

type NoteDraft = Pick<Note, "title" | "content" | "note_type" | "tags" | "status">;

const emptyDraft = (): NoteDraft => ({
  title: "",
  content: "",
  note_type: "general",
  tags: [],
  status: "active",
});

export function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [draft, setDraft] = useState<NoteDraft>(emptyDraft());
  const [query, setQuery] = useState("");
  const [online, setOnline] = useState(false);
  const [saving, setSaving] = useState(false);

  const selectedNote = useMemo(
    () => notes.find((note) => note.id === selectedId) ?? null,
    [notes, selectedId],
  );

  const loadNotes = useCallback(async () => {
    const response = await fetch(`${API_BASE}/api/notes`);
    if (!response.ok) throw new Error("无法读取笔记");
    setNotes(await response.json());
  }, []);

  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((response) => setOnline(response.ok))
      .catch(() => setOnline(false));
    loadNotes().catch(() => setOnline(false));
  }, [loadNotes]);

  useEffect(() => {
    if (selectedNote) {
      setDraft({
        title: selectedNote.title,
        content: selectedNote.content,
        note_type: selectedNote.note_type,
        tags: selectedNote.tags,
        status: selectedNote.status,
      });
    }
  }, [selectedNote]);

  const visibleNotes = useMemo(() => {
    const term = query.trim().toLowerCase();
    if (!term) return notes;
    return notes.filter((note) =>
      [note.title, note.content, note.tags.join(" ")].some((value) =>
        value.toLowerCase().includes(term),
      ),
    );
  }, [notes, query]);

  function newNote() {
    setSelectedId(null);
    setDraft(emptyDraft());
  }

  async function saveNote() {
    if (!draft.title.trim()) return;
    setSaving(true);
    try {
      const response = await fetch(`${API_BASE}/api/notes${selectedId ? `/${selectedId}` : ""}`, {
        method: selectedId ? "PUT" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(draft),
      });
      if (!response.ok) throw new Error("保存失败");
      const saved: Note = await response.json();
      await loadNotes();
      setSelectedId(saved.id);
      setOnline(true);
    } finally {
      setSaving(false);
    }
  }

  async function deleteNote() {
    if (!selectedId || !confirm("删除这条笔记？")) return;
    const response = await fetch(`${API_BASE}/api/notes/${selectedId}`, { method: "DELETE" });
    if (!response.ok) return;
    newNote();
    await loadNotes();
  }

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
        <div className="status">
          {online ? <Wifi size={15} /> : <WifiOff size={15} />}
          <span>{online ? "API 已连接" : "API 未连接"}</span>
        </div>
        <button className="primary-button" onClick={newNote}>
          <Plus size={17} />
          新建笔记
        </button>
        <label className="search">
          <Search size={16} />
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索笔记" />
        </label>
        <div className="notes-list">
          {visibleNotes.length === 0 ? (
            <p className="empty-list">还没有笔记</p>
          ) : (
            visibleNotes.map((note) => (
              <button
                className={`note-item ${selectedId === note.id ? "selected" : ""}`}
                key={note.id}
                onClick={() => setSelectedId(note.id)}
              >
                <FileText size={16} />
                <span>
                  <strong>{note.title}</strong>
                  <small>{new Date(note.updated_at).toLocaleString("zh-CN")}</small>
                </span>
              </button>
            ))
          )}
        </div>
      </aside>

      <main className="editor">
        <header className="editor-header">
          <div>
            <p className="eyebrow">{selectedId ? "编辑笔记" : "新建笔记"}</p>
            <h2>{draft.title || "未命名笔记"}</h2>
          </div>
          <div className="actions">
            {selectedId && (
              <button className="icon-button danger" onClick={deleteNote} title="删除笔记">
                <Trash2 size={18} />
              </button>
            )}
            <button className="save-button" onClick={saveNote} disabled={!draft.title.trim() || saving}>
              <Save size={17} />
              {saving ? "保存中" : "保存"}
            </button>
          </div>
        </header>
        <section className="editor-body">
          <input
            className="title-input"
            value={draft.title}
            onChange={(event) => setDraft({ ...draft, title: event.target.value })}
            placeholder="笔记标题"
          />
          <div className="meta-row">
            <select value={draft.note_type} onChange={(event) => setDraft({ ...draft, note_type: event.target.value })}>
              <option value="general">普通笔记</option>
              <option value="engineering">工程笔记</option>
              <option value="content">内容笔记</option>
              <option value="prompt">Prompt</option>
            </select>
            <input
              value={draft.tags.join(", ")}
              onChange={(event) =>
                setDraft({ ...draft, tags: event.target.value.split(",").map((tag) => tag.trim()).filter(Boolean) })
              }
              placeholder="标签，用逗号分隔"
            />
          </div>
          <textarea
            value={draft.content}
            onChange={(event) => setDraft({ ...draft, content: event.target.value })}
            placeholder="记录想法、决策、内容草稿……"
          />
        </section>
      </main>
    </div>
  );
}

