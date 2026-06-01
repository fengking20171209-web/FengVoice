$ErrorActionPreference = "Stop"

$repo = "D:\Projects\FengVoice"
$logFile = "$env:TEMP\fengvoice-git-sync-$(Get-Date -Format 'yyyyMMdd-HHmmss').log"
$proxy = if ($env:FENGVOICE_GITHUB_PROXY) { $env:FENGVOICE_GITHUB_PROXY } else { "socks5h://127.0.0.1:10808" }

$env:HTTP_PROXY = $proxy
$env:HTTPS_PROXY = $proxy
$env:http_proxy = $proxy
$env:https_proxy = $proxy

Push-Location $repo
try {
    "======== FengVoice Git Sync ========" | Out-File $logFile -Encoding UTF8
    "Repo: $repo" | Add-Content $logFile -Encoding UTF8
    "Proxy: $proxy" | Add-Content $logFile -Encoding UTF8

    git fetch origin 2>&1 | Add-Content $logFile -Encoding UTF8
    if ($LASTEXITCODE -ne 0) { throw "git fetch failed. See $logFile" }

    git pull --ff-only 2>&1 | Add-Content $logFile -Encoding UTF8
    if ($LASTEXITCODE -ne 0) { throw "git pull --ff-only failed. See $logFile" }

    $branch = git branch --show-current
    $divergence = git rev-list --left-right --count "HEAD...origin/$branch"
    "[$(Get-Date)] $branch divergence: $divergence" | Add-Content $logFile -Encoding UTF8
    Write-Host "Git sync complete. Log: $logFile" -ForegroundColor Green
} finally {
    Pop-Location
}
