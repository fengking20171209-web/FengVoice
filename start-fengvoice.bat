@echo off
chcp 65001 >nul
cd /d D:\Projects\FengVoice

echo ======== FengVoice local dev ========
echo Starting API on http://localhost:8000 ...
start "FengVoice API" cmd /k "cd /d D:\Projects\FengVoice\services\api && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo Starting Web on http://localhost:3000 ...
start "FengVoice Web" cmd /k "cd /d D:\Projects\FengVoice\apps\web && npm run dev -- --host 0.0.0.0 --port 3000"

timeout /t 3 >nul
start http://localhost:3000

echo FengVoice dev windows are open.
echo Close the "FengVoice API" and "FengVoice Web" windows to stop services.
pause
