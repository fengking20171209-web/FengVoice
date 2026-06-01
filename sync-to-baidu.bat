@echo off
chcp 65001 >nul
echo ======== FengVoice 备份到百度网盘 ========
powershell -ExecutionPolicy Bypass -File "D:\Projects\FengVoice\sync-to-baidu.ps1"
echo.
pause
