@echo off
chcp 65001 >nul
echo ======== FengVoice backup to Baidu Netdisk ========
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\Projects\FengVoice\sync-to-baidu.ps1"
echo.
pause
