# FengVoice 本地笔记 - 功能验证指南

## 🔗 服务地址

| 服务 | 地址 | 说明 |
|------|------|------|
| Web UI | http://127.0.0.1:5173 | Vite 开发服务器 |
| API | http://127.0.0.1:8000 | FastAPI 后端 |
| API Docs | http://127.0.0.1:8000/docs | Swagger UI（交互式 API 文档） |
| API Health | http://127.0.0.1:8000/health | 健康检查端点 |
| Static Uploads | http://127.0.0.1:5173/uploads/notes/ | 上传的静态文件 |

## 🚀 启动步骤

### 方式一：使用启动脚本（推荐）

```powershell
cd D:\Projects\FengVoice_Clean
.\start-notes-verify.bat
```

### 方式二：手动启动

```powershell
# 1. 启动 API（需要 Python + venv）
cd D:\Projects\FengVoice_Clean\services\api
.venv\Scripts\activate
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# 2. 启动 Web（需要 Node.js）
cd D:\Projects\FengVoice_Clean\apps\web
npm run dev -- --host 127.0.0.1 --port 5173

# 3. 浏览器打开
start http://127.0.0.1:5173
```

## ✅ 功能验证清单

### A. API 层验证

```powershell
# 1. 健康检查
curl http://127.0.0.1:8000/health

# 2. 创建笔记
curl -X POST http://127.0.0.1:8000/api/notes ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"API测试笔记\",\"content\":\"Hello from curl\",\"note_type\":\"general\"}"

# 3. 列出笔记
curl http://127.0.0.1:8000/api/notes

# 4. 查看单条笔记
curl http://127.0.0.1:8000/api/notes/{note_id}

# 5. 搜索笔记
curl "http://127.0.0.1:8000/api/notes?search=测试"
```

### B. 图像上传验证

```powershell
# 图片上传（需要先有图片文件）
curl -X POST http://127.0.0.1:8000/api/uploads/images ^
  -F "file=@D:\test.png"

# 预期返回：
# { "url": "...", "alt": "pasted image", "image_id": "..." }
```

### C. Web UI 验证

1. **页面加载** — http://127.0.0.1:5173/ 正常打开
2. **新建笔记** — 输入标题和内容，保存成功
3. **笔记列表** — 刚创建的笔记出现在列表中
4. **普通笔记粘贴图片** — 插入 `![pasted image](url)`
5. **新建 rich note** — 切换图文笔记模式
6. **中文输入** — 长句不卡、不截断
7. **粘贴纯文本** — 不触发图片上传
8. **粘贴图片** — 生成 image block + 空 paragraph
9. **特殊字符** — 双引号、反斜杠、`code` 保存后正确显示
10. **Blocks 恢复** — 切换笔记再回来，blocks 能恢复

## 📊 数据库

- **路径**: `data/fengvoice.db`
- **引擎**: SQLite
- **表结构**:
  - `notes` — 笔记（id, title, content, note_type, tags, status, created_at, updated_at）

## 🔐 .env 配置

复制并编辑：

```bash
cp .env.example .env
# 编辑 .env 按需配置：
# VITE_API_BASE_URL=http://localhost:8000
# FENGVOICE_DB_PATH=data/fengvoice.db
```

## 🐛 常见问题

| 问题 | 解决 |
|------|------|
| Python 未找到 | 安装 Python 3.10+ 并加入 PATH |
| 虚拟环境不存在 | `python -m venv .venv` + `pip install -r services/api/requirements.txt` |
| node_modules 缺失 | `cd apps\web && npm install` |
| API 端口被占用 | 修改 `main:app --port 8000` 中的端口号 |
| 前端跨域错误 | `main.py` 已配置 `allow_origins=["*"]`，通常不需要额外设置 |

## 📁 关键文件

| 文件 | 用途 |
|------|------|
| `start-notes-verify.bat` | 一键启动 + 验证入口 |
| `services/api/main.py` | FastAPI 后端 |
| `apps/web/src/api.ts` | 前端 API 客户端 |
| `data/fengvoice.db` | 本地 SQLite 数据库 |
| `public/uploads/notes/` | 上传的图像文件 |
