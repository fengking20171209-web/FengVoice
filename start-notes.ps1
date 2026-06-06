<#
FengVoice local notes launcher.

Starts the local FastAPI backend and Vite web app in separate PowerShell
windows, then opens the local web UI. This script does not install
dependencies, read secrets, connect to cloud services, or modify project data.
#>

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ApiDir = Join-Path $Root "services\api"
$WebDir = Join-Path $Root "apps\web"
$RootVenvActivate = Join-Path $Root ".venv\Scripts\Activate.ps1"
$ApiVenvActivate = Join-Path $ApiDir ".venv\Scripts\Activate.ps1"
$WebNodeModules = Join-Path $WebDir "node_modules"
$WebUrl = "http://127.0.0.1:5173/"

Write-Host "FengVoice local notes launcher" -ForegroundColor Cyan
Write-Host "Root: $Root"

if (-not (Test-Path $ApiDir)) {
    Write-Error "API directory not found: $ApiDir"
}

if (-not (Test-Path $WebDir)) {
    Write-Error "Web directory not found: $WebDir"
}

if (-not (Test-Path $RootVenvActivate) -and -not (Test-Path $ApiVenvActivate)) {
    Write-Warning "No Python virtual environment found at .venv or services\api\.venv. Create one before starting the API."
}

if (-not (Test-Path $WebNodeModules)) {
    Write-Warning "apps\web\node_modules was not found. Run 'npm ci' or 'npm install' in apps\web before starting the web app."
}

$ApiCommand = @"
`$ErrorActionPreference = 'Stop'
cd `"$ApiDir`"
if (Test-Path `"$ApiVenvActivate`") {
    . `"$ApiVenvActivate`"
} elseif (Test-Path `"$RootVenvActivate`") {
    . `"$RootVenvActivate`"
} else {
    Write-Warning 'No virtual environment found. Trying python from PATH.'
}
Write-Host 'Starting FengVoice API on http://127.0.0.1:8000' -ForegroundColor Green
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
"@

$WebCommand = @"
`$ErrorActionPreference = 'Stop'
cd `"$WebDir`"
if (-not (Test-Path `"$WebNodeModules`")) {
    Write-Warning 'node_modules is missing. Run npm ci or npm install in apps\web first.'
    Read-Host 'Press Enter to close this window'
    exit 1
}
Write-Host 'Starting FengVoice web app on http://127.0.0.1:5173' -ForegroundColor Green
npm run dev -- --host 127.0.0.1 --port 5173
"@

Start-Process powershell -ArgumentList @("-NoExit", "-Command", $ApiCommand)
Start-Process powershell -ArgumentList @("-NoExit", "-Command", $WebCommand)

Start-Sleep -Seconds 3
Start-Process $WebUrl

Write-Host "Opened $WebUrl" -ForegroundColor Cyan
