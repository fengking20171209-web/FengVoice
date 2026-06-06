# Rich Note Helper Patch Report

## Workspace

- **path:** `D:\Projects\FengVoice_Clean`
- **branch:** `codex/personal-notes-strategy-docs`

## Changed Files

- `apps/web/src/richNote.ts` — 新增未跟踪文件，已有实现基础上追加硬约束 10（尾部 image 后自动补空 paragraph）
- `reports/personal-notes/rich-note/01-rich-note-helper-report.md` — 本报告

## Validation

| Item | Result |
|------|--------|
| dependency install | N/A (node_modules 已存在，未执行 npm ci / npm install) |
| npm run build | PASS (tsc + vite build 成功，3.93s) |
| newline preservation | PASS — `normalizeParagraphText` 直接返回 string，无 `.trim()` 或无空格清洗 |
| non-string paragraph handling | PASS — null/undefined → `""`，其他值 → `String(value)` |
| markdown sniff | PASS — `sniffRichNoteJson` 轻量检查 startsWith `{` + 包含 `"blocks"` |
| invalid JSON | PASS — `parseRichNoteContent` try/catch 返回 null |
| empty blocks fallback | PASS — `blocks.length === 0` 返回 `createEmptyRichNote()` |
| extra fields sanitization | PASS — normalize 函数均创建新对象，不含 unknown_field |
| trailing paragraph after final image | PASS — `ensureValidRichNote` 新增检测：最后 block 为 image 时追加空 paragraph |
| append image | PASS — `appendImageBlock` 追加 image + 空 paragraph |

## Forbidden Paths

| Path | Status |
|------|--------|
| `apps/web/src/App.tsx` | 未修改 |
| `apps/web/src/RichNoteEditor.tsx` | 不存在，未创建 |
| `apps/web/src/imagePaste.ts` | 未修改 |
| `apps/web/src/api.ts` | 未修改 |
| `apps/web/src/styles.css` | 未修改 |
| `services/api/` | 未修改 |
| `runtime/` | 未修改 |
| `public/uploads/` | 未修改 |
| `data/` | 未修改 |
| `package.json` | 未修改 |
| `package-lock.json` | 未修改 |

## Result

**PASS** — 所有硬约束满足，build 正常，禁止路径未触达。