# FengVoice 个人笔记系统 - 部署说明

## 简介

FengVoice 是一个本地优先的个人笔记平台，支持富文本图文笔记、图像粘贴上传、音频录制和 Markdown 编辑。

**当前版本**: v0.2.0-alpha  
**核心功能**: 图文笔记、图像粘贴、音频录制、标签搜索

---

## 快速开始（3 分钟上手）

### 前置条件

| 工具 | 版本要求 | 下载地址 |
|------|---------|---------|
| Python | 3.10+ | https://www.python.org/downloads/ |
| Node.js | 18+ | https://nodejs.org/ |
| Git | 任何版本 | https://git-scm.com/ |

### 步骤 1：克隆项目

```powershell
git clone https://github.com/fengking20171209-web/FengVoice.git
cd FengVoice
```

### 步骤 2：安装后端依赖

```powershell
cd services\api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
cd ..\..
```

### 步骤 3：安装前端依赖

```powershell
cd apps\web
npm install
cd ..\..
```

### 步骤 4：配置环境变量

```powershell
copy .env.example .env
```

### 步骤 5：一键启动

```powershell
.\start-notes.bat
```

或使用增强验证脚本：

```powershell
.\start-notes-verify.bat
```

启动后浏览器自动打开 http://127.0.0.1:5173

---

## 服务地址

| 服务 | 地址 | 用途 |
|------|------|------|
| Web UI | http://127.0.0.1:5173 | 笔记编辑器 |
| API | http://127.0.0.1:8000 | 后端接口 |
| API 文档 | http://127.0.0.1:8000/docs | Swagger 交互式文档 |
| 图片上传 | http://127.0.0.1:8000/uploads/notes/ | 静态文件 |

---

## 手动启动（替代方案）

### 终端 1 — 启动后端 API

```powershell
cd services\api
.venv\Scripts\activate
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 终端 2 — 启动前端

```powershell
cd apps\web
npm run dev -- --host 127.0.0.1 --port 5173
```

### 终端 3 — 打开浏览器

```powershell
start http://127.0.0.1:5173
```

---

## Docker 部署（可选）

如果笔记本已安装 Docker Desktop：

```powershell
docker compose up -d
```

访问 http://localhost:3000

数据存储在 Docker volume 中：

```powershell
# 查看数据
docker volume inspect fengvoice_fengvoice_data

# 备份数据
docker run --rm -v fengvoice_fengvoice_data:/data -v $(pwd):/backup alpine tar czf /backup/fengvoice_backup.tar.gz -C /data .

# 恢复数据
docker run --rm -v fengvoice_fengvoice_data:/data -v $(pwd):/backup alpine tar xzf /backup/fengvoice_backup.tar.gz -C /data
```

---

## 数据管理

### 数据存储位置

| 数据 | 路径 | 说明 |
|------|------|------|
| 笔记数据库 | `data/fengvoice.db` | SQLite |
| 上传的图片 | `public/uploads/notes/` | PNG/JPEG/WebP |
| 音频文件 | `public/uploads/audio/` | WebM/OGG |
| 图像索引 | `runtime/asset-index/note-images.jsonl` | JSONL 元数据 |

### 数据备份

备份重要数据文件（换机器前必做）：

```powershell
# 创建备份目录
mkdir D:\FengVoiceBackups

# 复制数据文件
copy data\fengvoice.db D:\FengVoiceBackups\
xcopy public\uploads D:\FengVoiceBackups\uploads\ /E /I
copy runtime\asset-index\note-images.jsonl D:\FengVoiceBackups\
```

### 恢复数据

在新笔记本上恢复：

```powershell
# 将备份文件放回项目目录
copy D:\FengVoiceBackups\fengvoice.db data\
xcopy D:\FengVoiceBackups\uploads\ public\uploads\ /E /I
copy D:\FengVoiceBackups\note-images.jsonl runtime\asset-index\
```

---

## 常见问题

### 问题 1：Python 找不到

**症状**: `python: command not found`

**解决**: 安装 Python 3.10+，勾选 "Add Python to PATH"

### 问题 2：node_modules 缺失

**症状**: `Cannot find module 'react'`

**解决**: `cd apps\web && npm install`

### 问题 3：端口被占用

**症状**: `Port 8000 is already in use`

**解决**: 修改启动命令中的端口号，或关闭占用端口的程序

### 问题 4：图片显示不出来

**症状**: 图文笔记中图片区域显示为空白或错误提示

**原因**: Vite dev server 请求 `/uploads/` 时是 5173 端口，但图片文件在 8000 端口的 API 下

**解决**:
1. 确认 API 正在运行: `curl http://127.0.0.1:8000/health`
2. 直接打开图片 URL 验证: `http://127.0.0.1:8000/uploads/notes/xxx.png`
3. 如果 API 不通，检查防火墙设置

### 问题 5：数据库损坏

**症状**: 笔记列表加载失败，API 报错

**解决**:
```powershell
# 删除损坏的数据库，从备份恢复
del data\fengvoice.db
copy D:\FengVoiceBackups\fengvoice.db data\
# 重启 API 服务
```

---

## 技术栈

| 层 | 技术 | 说明 |
|----|------|------|
| 前端 | React 19 + TypeScript + Vite | SPA 单页应用 |
| 后端 | FastAPI + Python 3.10 | RESTful API |
| 数据库 | SQLite | 本地文件数据库 |
| 图标 | Lucide React | 轻量图标库 |
| 部署 | 本地开发 | 支持 Docker |

---

## 下一步

- 冷冻观察期：使用 `05-rich-note-v1-freeze-observation.md` 模板记录真实使用体验
- 数据备份：换机器前备份 `data/fengvoice.db` 和 `public/uploads/`
- 远程访问：需自行配置 ngrok 或 frp（本项目不内置）

---

## 许可证

MIT License - 详见 LICENSE 文件
