param(
    [string] $Proxy = $(if ($env:FENGVOICE_GITHUB_PROXY) { $env:FENGVOICE_GITHUB_PROXY } else { "socks5h://127.0.0.1:10808" })
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$proxyUri = [Uri] $Proxy
$proxyHost = $proxyUri.Host
$proxyPort = $proxyUri.Port

Write-Host "======== FengVoice GitHub CLI Check ========" -ForegroundColor Cyan
Write-Host "Repo: $repoRoot"
Write-Host "Proxy: $Proxy"

$tcp = Test-NetConnection $proxyHost -Port $proxyPort -WarningAction SilentlyContinue
if (-not $tcp.TcpTestSucceeded) {
    throw "Proxy is not reachable at ${proxyHost}:${proxyPort}. Start your local proxy before using gh."
}

$env:HTTP_PROXY = $Proxy
$env:HTTPS_PROXY = $Proxy
$env:http_proxy = $Proxy
$env:https_proxy = $Proxy

Push-Location $repoRoot
try {
    Write-Host ""
    Write-Host "[1/4] gh auth status" -ForegroundColor Yellow
    & gh auth status
    if ($LASTEXITCODE -ne 0) { throw "gh auth status failed." }

    Write-Host ""
    Write-Host "[2/4] gh repo view" -ForegroundColor Yellow
    & gh repo view fengking20171209-web/FengVoice --json nameWithOwner,url,defaultBranchRef
    if ($LASTEXITCODE -ne 0) { throw "gh repo view failed." }

    Write-Host ""
    Write-Host "[3/4] git branch divergence" -ForegroundColor Yellow
    $branch = git branch --show-current
    git fetch origin
    if ($LASTEXITCODE -ne 0) { throw "git fetch failed." }
    $divergence = git rev-list --left-right --count "HEAD...origin/$branch"
    Write-Host "${branch} vs origin/${branch}: $divergence"

    Write-Host ""
    Write-Host "[4/4] git push dry-run" -ForegroundColor Yellow
    git push --dry-run origin HEAD
    if ($LASTEXITCODE -ne 0) { throw "git push dry-run failed." }

    Write-Host ""
    Write-Host "GitHub CLI is ready." -ForegroundColor Green
} finally {
    Pop-Location
}
