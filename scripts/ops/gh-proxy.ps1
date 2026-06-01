param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $GhArgs
)

$ErrorActionPreference = "Stop"

$proxy = if ($env:FENGVOICE_GITHUB_PROXY) {
    $env:FENGVOICE_GITHUB_PROXY
} else {
    "socks5h://127.0.0.1:10808"
}

$env:HTTP_PROXY = $proxy
$env:HTTPS_PROXY = $proxy
$env:http_proxy = $proxy
$env:https_proxy = $proxy

if (-not $GhArgs -or $GhArgs.Count -eq 0) {
    Write-Host "Usage: powershell -ExecutionPolicy Bypass -File scripts\ops\gh-proxy.ps1 <gh args>"
    Write-Host "Proxy: $proxy"
    exit 0
}

& gh @GhArgs
exit $LASTEXITCODE
