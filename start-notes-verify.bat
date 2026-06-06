@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ============================================
echo   FengVoice 本地笔记验证入口
echo ============================================
echo.
echo   1. 环境检查与初始化
echo   2. 启动服务（API + Web）
echo   3. 服务健康检查
echo   4. 打开本地笔记 UI
echo   5. API 接口速查
echo.
echo   注意：首次运行请先选 1
echo.
set /p choice="请选择 (1-5 或 Q退出): "

if /i "%choice%"=="1" goto :setup
if /i "%choice%"=="2" goto :start
if /i "%choice%"=="3" goto :health
if /i "%choice%"=="4" goto :open
if /i "%choice%"=="5" goto :api
if /i "%choice%"=="q" goto :eof
if /i "%choice%"=="Q" goto :eof

echo 无效选项，请重新运行。
pause
exit /b

:: ========== 环境检查与初始化 ==========
:setup
echo.
echo --- 环境检查 ---
echo.

echo [1/4] 检查 Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo   [WARN] Python 未添加到 PATH
    echo          请确保 Python 3.10+ 已安装，或将完整路径加入启动命令
) else (
    for /f "tokens=*" %%i in ('python --version') do echo   [OK] %%i
)
echo.

echo [2/4] 检查 Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo   [WARN] Node.js 未添加到 PATH
) else (
    for /f "tokens=*" %%i in ('node --version') do echo   [OK] %%i
)
echo.

echo [3/4] 检查 Python 虚拟环境...
if not exist ".venv\Scripts\Activate.ps1" (
    if not exist "services\api\.venv\Scripts\Activate.ps1" (
        echo   [INFO] 未找到虚拟环境
        echo          首次运行需要创建：
        echo.
        echo          cd services\api
        echo          python -m venv .venv
        echo          .venv\Scripts\activate
        echo          pip install -r requirements.txt
        echo.
        set /p create_venv="是否现在创建虚拟环境? (Y/N): "
        if /i "%create_venv%"=="Y" (
            echo.
            echo --- 创建虚拟环境 ---
            python -m venv .venv
            if %errorlevel% equ 0 (
                .venv\Scripts\activate
                pip install -q -r services\api\requirements.txt
                echo   [OK] 虚拟环境创建完成，依赖已安装
            ) else (
                echo   [FAIL] 虚拟环境创建失败
            )
        )
    ) else (
        echo   [OK] 虚拟环境已存在: services\api\.venv
    )
) else (
    echo   [OK] 虚拟环境已存在: .venv
)
echo.

echo [4/4] 检查 .env 文件...
if not exist ".env" (
    echo   [INFO] .env 不存在，从 .env.example 复制...
    copy /y .env.example .env >nul
    echo   [OK] 已创建 .env（请按需编辑）
) else (
    echo   [OK] .env 已存在
)
echo.

echo [5/4] 检查 node_modules...
if not exist "apps\web\node_modules" (
    echo   [INFO] node_modules 不存在，需要安装前端依赖...
    set /p install_npm="是否现在安装? (Y/N): "
    if /i "%install_npm%"=="Y" (
        echo.
        echo --- 安装前端依赖 ---
        cd apps\web
        npm install
        cd ..\..
    )
) else (
    echo   [OK] node_modules 已存在
)
echo.

echo --- 环境就绪 ---
echo.
echo 下一步：选 2 启动服务
pause
goto :eof

:: ========== 启动服务 ==========
:start
echo.
echo --- 启动服务 ---
echo.

REM 检查数据库目录
if not exist "data" mkdir data

REM 启动 API（带虚拟环境检测）
if exist ".venv\Scripts\activate.bat" (
    echo 启动 API: .venv -> uvicorn (port 8000)
    start "FengVoice API" cmd /k "cd /d D:\Projects\FengVoice_Clean && .venv\Scripts\activate && python -m uvicorn services.api.main:app --host 127.0.0.1 --port 8000 --reload"
) else if exist "services\api\.venv\Scripts\activate.bat" (
    echo 启动 API: services\api\.venv -> uvicorn (port 8000)
    start "FengVoice API" cmd /k "cd /d D:\Projects\FengVoice_Clean\services\api && ..\..\.venv\Scripts\activate && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"
) else (
    echo 启动 API: python (port 8000)  [无虚拟环境]
    start "FengVoice API" cmd /k "cd /d D:\Projects\FengVoice_Clean\services\api && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"
)

echo 启动 Web: Vite dev server (port 5173)
start "FengVoice Web" cmd /k "cd /d D:\Projects\FengVoice_Clean\apps\web && npm run dev -- --host 127.0.0.1 --port 5173"

echo.
echo 等待 4 秒...
timeout /t 4 >nul

echo.
echo --- 服务已启动 ---
echo   API:  http://127.0.0.1:8000
echo   Web:  http://127.0.0.1:5173
echo   API docs: http://127.0.0.1:8000/docs
echo.
echo 下一步：选 3 做健康检查，选 4 打开笔记 UI
pause
goto :eof

:: ========== 健康检查 ==========
:health
echo.
echo --- 健康检查 ---
echo.

echo [1/2] API 健康检查...
curl -s http://127.0.0.1:8000/health 2>nul
if %errorlevel% neq 0 (
    echo   [FAIL] API 无法连接 (port 8000)
    echo          请先运行选 2 启动 API
) else (
    echo   [OK] API 运行正常
)
echo.

echo [2/2] Web 健康检查...
curl -s http://127.0.0.1:5173/ 2>nul | findstr /i "html" >nul
if %errorlevel% neq 0 (
    echo   [WARN] Web 未就绪 (port 5173)
    echo          请先运行选 2 启动 Web
) else (
    echo   [OK] Web 运行正常
)
echo.
pause
goto :eof

:: ========== 打开笔记 UI ==========
:open
echo.
echo --- 打开笔记 UI ---
echo.
echo 正在打开 http://127.0.0.1:5173/
start http://127.0.0.1:5173/
echo   API docs: http://127.0.0.1:8000/docs
echo   API health: http://127.0.0.1:8000/health
echo.
echo 打开后验证清单:
echo   1. 页面是否正常加载
echo   2. 新建笔记（标题 + 内容）
echo   3. 粘贴图片测试
echo   4. 切换普通笔记 / rich note 模式
echo   5. 保存并重新打开，检查 blocks 恢复
echo.
pause
goto :eof

:: ========== API 接口速查 ==========
:api
echo.
echo ============================================================
echo   FengVoice API 接口速查
echo ============================================================
echo.
echo  基础地址: http://127.0.0.1:8000
echo  Swagger UI:  http://127.0.0.1:8000/docs
echo  JSON Schema: http://127.0.0.1:8000/openapi.json
echo.
echo  --- 健康检查 ---
echo  GET  /health
echo.
echo  --- 图片上传 ---
echo  POST /api/uploads/images  [multipart/form-data, file=image]
echo.
echo  --- 音频上传 ---
echo  POST /api/notes/audio     [multipart/form-data, file=audio]
echo.
echo  --- 笔记 CRUD ---
echo  GET    /api/notes          [list, ?search=xxx]
echo  POST   /api/notes          [body: {title, content, note_type, tags, status}]
echo  GET    /api/notes/{id}     [get by id]
echo  PUT    /api/notes/{id}     [update]
echo  DELETE /api/notes/{id}     [delete by id]
echo.
echo  --- curl 示例 ---
echo  curl http://127.0.0.1:8000/health
echo  curl -X POST http://127.0.0.1:8000/api/notes ^
echo    -H "Content-Type: application/json" ^
echo    -d "{\"title\":\"测试笔记\",\"content\":\"Hello\",\"note_type\":\"general\"}"
echo.
echo  --- 数据库 ---
echo  SQLite: data/fengvoice.db
echo  表: notes, image_assets, audio_assets (如适用)
echo.
pause
goto :eof
