@echo off
chcp 65001 >nul
echo ======== FengVoice save progress ========

echo 1. Check GitHub CLI and Git push state
cd /d D:\Projects\FengVoice
powershell -ExecutionPolicy Bypass -File "D:\Projects\FengVoice\scripts\ops\check-github-cli.ps1"
if errorlevel 1 goto failed

echo.
echo 2. Git working tree
git status --short --branch

echo.
echo 3. Backup to Baidu Netdisk
powershell -ExecutionPolicy Bypass -File "D:\Projects\FengVoice\sync-to-baidu.ps1"
if errorlevel 1 goto failed

echo.
echo Progress saved.
pause
exit /b 0

:failed
echo.
echo Save progress failed. Check the error above.
pause
exit /b 1
