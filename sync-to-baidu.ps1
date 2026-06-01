# FengVoice -> Baidu Netdisk backup
# Direction: local workspace -> Baidu Netdisk sync folder
# Mirrors project files. GitHub remains the code remote; Baidu Netdisk keeps a local snapshot.

$ErrorActionPreference = "Stop"

$src = "D:\Projects\FengVoice"
$baiduSyncFolder = -join ([char[]] (0x767E, 0x5EA6, 0x7F51, 0x76D8, 0x540C, 0x6B65, 0x6587, 0x4EF6))
$dst = Join-Path "E:\BaiduNetdiskDownload" (Join-Path $baiduSyncFolder "BaiduSyncdisk\Projects\FengVoice")
$logFile = "$env:TEMP\fengvoice-sync-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
$start = Get-Date

Write-Host "======== FengVoice backup to Baidu Netdisk ========" -ForegroundColor Cyan
Write-Host "Source: $src"
Write-Host "Target: $dst"
Write-Host "Start: $start"

$excludeDirs = @(
    '.git',
    'node_modules',
    '.venv',
    '__pycache__',
    '.tools',
    '.kimi-code',
    'dist',
    'build',
    '.next',
    '.output'
)

$xdArgs = $excludeDirs | ForEach-Object { '/XD', $_ }

robocopy $src $dst /MIR /COPY:DAT /R:1 /W:1 /NDL /NP /MT:4 `
    $xdArgs /XF "*.baiduyun.*" /LOG+:$logFile

$robocopyExit = $LASTEXITCODE

Write-Host ""
Write-Host "Finished: $(Get-Date)" -ForegroundColor Green
Write-Host "Elapsed: $('{0:N1}' -f ((Get-Date)-$start).TotalSeconds)s"
Write-Host "Log: $logFile"

if (Get-Process -Name BaiduNetdisk -ErrorAction SilentlyContinue) {
    Write-Host "BaiduNetdisk is running; synced files should upload automatically." -ForegroundColor Yellow
} else {
    Write-Host "BaiduNetdisk is not running; start it to upload the backup." -ForegroundColor Yellow
}

if ($robocopyExit -ge 8) {
    exit $robocopyExit
}

exit 0
