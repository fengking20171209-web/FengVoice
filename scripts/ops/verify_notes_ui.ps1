$ErrorActionPreference = "Stop"

$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$profile = Join-Path $PSScriptRoot "..\..\.chrome-test-profile"
$debugPort = 9222
$webUrl = "http://localhost:3000"
$apiUrl = "http://localhost:8000"

function Wait-Until {
    param(
        [scriptblock]$Condition,
        [string]$Message,
        [int]$TimeoutMs = 5000
    )

    $deadline = [DateTime]::UtcNow.AddMilliseconds($TimeoutMs)
    do {
        if (& $Condition) {
            return
        }
        Start-Sleep -Milliseconds 100
    } while ([DateTime]::UtcNow -lt $deadline)

    throw "Timed out: $Message"
}

function Start-DebugChrome {
    if (-not (Test-Path -LiteralPath $chrome)) {
        throw "Chrome not found at $chrome"
    }

    $listener = Get-NetTCPConnection -State Listen -LocalPort $debugPort -ErrorAction SilentlyContinue
    if (-not $listener) {
        New-Item -ItemType Directory -Force -Path $profile | Out-Null
        Start-Process -FilePath $chrome -ArgumentList @(
            "--headless=new",
            "--disable-gpu",
            "--remote-debugging-port=$debugPort",
            "--user-data-dir=$profile",
            $webUrl
        ) -WindowStyle Hidden
    }

    Wait-Until -Message "Chrome DevTools endpoint" -Condition {
        try {
            Invoke-RestMethod -Uri "http://127.0.0.1:$debugPort/json/list" | Out-Null
            $true
        } catch {
            $false
        }
    }
}

function Connect-Cdp {
    $targets = Invoke-RestMethod -Uri "http://127.0.0.1:$debugPort/json/list"
    $target = $targets | Where-Object { $_.type -eq "page" -and $_.url.StartsWith($webUrl) } | Select-Object -First 1
    if (-not $target) {
        throw "FengVoice browser target not found"
    }

    $script:socket = [System.Net.WebSockets.ClientWebSocket]::new()
    $script:socket.ConnectAsync([Uri]$target.webSocketDebuggerUrl, [Threading.CancellationToken]::None).GetAwaiter().GetResult() | Out-Null
    $script:messageId = 0
}

function Send-Cdp {
    param(
        [string]$Method,
        [hashtable]$Params = @{}
    )

    $script:messageId += 1
    $id = $script:messageId
    $payload = @{ id = $id; method = $Method; params = $Params } | ConvertTo-Json -Depth 20 -Compress
    $bytes = [Text.Encoding]::UTF8.GetBytes($payload)
    $segment = [ArraySegment[byte]]::new($bytes)
    $script:socket.SendAsync($segment, [Net.WebSockets.WebSocketMessageType]::Text, $true, [Threading.CancellationToken]::None).GetAwaiter().GetResult() | Out-Null

    do {
        $stream = [IO.MemoryStream]::new()
        do {
            $buffer = New-Object byte[] 65536
            $receiveSegment = [ArraySegment[byte]]::new($buffer)
            $result = $script:socket.ReceiveAsync($receiveSegment, [Threading.CancellationToken]::None).GetAwaiter().GetResult()
            $stream.Write($buffer, 0, $result.Count)
        } while (-not $result.EndOfMessage)
        $json = [Text.Encoding]::UTF8.GetString($stream.ToArray())
        $stream.Dispose()
        $message = $json | ConvertFrom-Json
    } while ($message.id -ne $id)

    if ($message.error) {
        throw "$Method failed: $($message.error.message)"
    }
    return $message.result
}

function Invoke-Js {
    param([string]$Expression)
    $result = Send-Cdp -Method "Runtime.evaluate" -Params @{
        expression = $Expression
        awaitPromise = $true
        returnByValue = $true
    }
    if ($result.exceptionDetails) {
        $description = $result.exceptionDetails.exception.description
        throw "JavaScript failed: $($result.exceptionDetails.text) $description"
    }
    return $result.result.value
}

function Assert-Equal {
    param($Actual, $Expected, [string]$Message)
    if ($Actual -ne $Expected) {
        throw "$Message. Expected '$Expected', received '$Actual'"
    }
}

function Assert-True {
    param($Actual, [string]$Message)
    if (-not $Actual) {
        throw $Message
    }
}

function Reload-Page {
    Send-Cdp -Method "Page.reload" -Params @{ ignoreCache = $true } | Out-Null
    Wait-Until -Message "FengVoice page render" -Condition {
        Invoke-Js "Boolean(document.querySelector('.connection'))"
    }
}

Start-DebugChrome
Connect-Cdp
Send-Cdp -Method "Runtime.enable" | Out-Null
Send-Cdp -Method "Page.enable" | Out-Null
Send-Cdp -Method "Network.enable" | Out-Null
Send-Cdp -Method "Network.setBlockedURLs" -Params @{ urls = @() } | Out-Null

Invoke-Js "fetch('$apiUrl/api/notes').then(r => r.json()).then(async notes => { for (const note of notes) await fetch('$apiUrl/api/notes/' + note.id, { method: 'DELETE' }); return true; })" | Out-Null
Reload-Page
Wait-Until -Message "API connected label" -Condition {
    Invoke-Js "document.querySelector('.connection')?.textContent.trim() === 'API \u5df2\u8fde\u63a5'"
}

Write-Host "UI acceptance: initial state"
$initial = Invoke-Js "({ connected: document.querySelector('.connection')?.textContent.trim() === 'API \u5df2\u8fde\u63a5', notes: document.querySelectorAll('.note-item').length })"
Assert-True $initial.connected "API connection label"
Assert-Equal $initial.notes 0 "Initial note count"

Invoke-Js "document.querySelector('.primary-button').click()" | Out-Null
Start-Sleep -Milliseconds 80
Write-Host "UI acceptance: optimistic create"
$immediate = Invoke-Js "({ notes: document.querySelectorAll('.note-item').length, titleMatches: document.querySelector('.note-item strong').textContent === '\u672a\u547d\u540d\u7b14\u8bb0', focused: document.activeElement === document.querySelector('.title-input') })"
Assert-Equal $immediate.notes 1 "Optimistic draft count"
Assert-True $immediate.titleMatches "Optimistic draft title"
Assert-True $immediate.focused "Title field was not focused after creating a note"

Start-Sleep -Milliseconds 1100
Wait-Until -Message "initial note server save" -Condition {
    Invoke-Js "document.querySelector('.save-status')?.textContent.trim() === '\u5df2\u4fdd\u5b58' && Boolean(document.querySelector('.note-item em'))"
}
Write-Host "UI acceptance: server save"
$saved = Invoke-Js "({ saved: document.querySelector('.save-status').textContent.trim() === '\u5df2\u4fdd\u5b58', badge: document.querySelector('.note-item em').textContent })"
Assert-True $saved.saved "Server save state"
Assert-Equal $saved.badge "general" "Server id did not replace optimistic draft"

$setNoteContent = @'
(() => {
  const title = document.querySelector('.title-input');
  const inputSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
  inputSetter.call(title, '\u4e2d\u6587\u754c\u9762\u9a8c\u6536\u7b14\u8bb0');
  title.dispatchEvent(new Event('input', { bubbles: true }));
  const content = document.querySelector('textarea');
  const textareaSetter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
  textareaSetter.call(content, '\u8fd9\u662f\u7528\u4e8e\u5237\u65b0\u548c\u641c\u7d22\u9a8c\u8bc1\u7684\u4e2d\u6587\u5185\u5bb9');
  content.dispatchEvent(new Event('input', { bubbles: true }));
})()
'@
Invoke-Js $setNoteContent | Out-Null
Start-Sleep -Milliseconds 1200
Wait-Until -Message "edited note autosave" -Condition {
    Invoke-Js "document.querySelector('.save-status')?.textContent.trim() === '\u5df2\u4fdd\u5b58' && Boolean(document.querySelector('.note-item strong'))"
}
Write-Host "UI acceptance: autosave"
$autosaved = Invoke-Js "({ saved: document.querySelector('.save-status').textContent.trim() === '\u5df2\u4fdd\u5b58', titleMatches: document.querySelector('.note-item strong').textContent === '\u4e2d\u6587\u754c\u9762\u9a8c\u6536\u7b14\u8bb0', summaryMatches: document.querySelector('.note-item span').textContent === '\u8fd9\u662f\u7528\u4e8e\u5237\u65b0\u548c\u641c\u7d22\u9a8c\u8bc1\u7684\u4e2d\u6587\u5185\u5bb9' })"
Assert-True $autosaved.saved "Autosave state"
Assert-True $autosaved.titleMatches "Autosaved title"
Assert-True $autosaved.summaryMatches "Autosaved content summary"

Reload-Page
$refreshed = Invoke-Js "({ notes: document.querySelectorAll('.note-item').length, titleMatches: document.querySelector('.note-item strong').textContent === '\u4e2d\u6587\u754c\u9762\u9a8c\u6536\u7b14\u8bb0' })"
Assert-Equal $refreshed.notes 1 "Refreshed note count"
Assert-True $refreshed.titleMatches "Refreshed title"

$setSearch = @'
(() => {
  const search = document.querySelector('.search input');
  const inputSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
  inputSetter.call(search, '\u4e2d\u6587\u754c\u9762');
  search.dispatchEvent(new Event('input', { bubbles: true }));
})()
'@
Invoke-Js $setSearch | Out-Null
$search = Invoke-Js "({ notes: document.querySelectorAll('.note-item').length, titleMatches: document.querySelector('.note-item strong').textContent === '\u4e2d\u6587\u754c\u9762\u9a8c\u6536\u7b14\u8bb0', clear: Boolean(document.querySelector('.search button')) })"
Assert-Equal $search.notes 1 "Search result count"
Assert-True $search.titleMatches "Search result title"
Assert-True $search.clear "Search clear button is missing"
Invoke-Js "document.querySelector('.search button').click()" | Out-Null
Invoke-Js "document.querySelector('.note-item').click()" | Out-Null
Start-Sleep -Milliseconds 100

$ctrlSave = @'
(() => {
  const title = document.querySelector('.title-input');
  const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
  setter.call(title, 'Ctrl S save check');
  title.dispatchEvent(new Event('input', { bubbles: true }));
})()
'@
Invoke-Js $ctrlSave | Out-Null
Start-Sleep -Milliseconds 80
Invoke-Js "document.querySelector('.title-input').focus()" | Out-Null
Invoke-Js "window.__ctrlProbe = null; window.addEventListener('keydown', event => { window.__ctrlProbe = { key: event.key, ctrlKey: event.ctrlKey, metaKey: event.metaKey, target: event.target.className }; }, { once: true })" | Out-Null
Invoke-Js "document.querySelector('.title-input').dispatchEvent(new KeyboardEvent('keydown', { key: 's', code: 'KeyS', ctrlKey: true, bubbles: true, cancelable: true }))" | Out-Null
$ctrlProbe = Invoke-Js "window.__ctrlProbe"
Write-Host "Ctrl+S probe: $($ctrlProbe | ConvertTo-Json -Compress)"
Start-Sleep -Milliseconds 350
Wait-Until -Message "Ctrl+S save" -TimeoutMs 2000 -Condition {
    Invoke-Js "document.querySelector('.save-status')?.textContent.trim() === '\u5df2\u4fdd\u5b58'"
}
Write-Host "UI acceptance: Ctrl+S"
$ctrlSaved = Invoke-Js "({ saved: document.querySelector('.save-status').textContent.trim() === '\u5df2\u4fdd\u5b58', title: document.querySelector('.note-item strong').textContent })"
if (-not $ctrlSaved.saved) {
    $ctrlDebug = Invoke-Js "({ status: document.querySelector('.save-status').textContent.trim(), title: document.querySelector('.note-item strong').textContent, input: document.querySelector('.title-input').value, probe: window.__ctrlProbe })"
    Write-Host "Ctrl+S debug: $($ctrlDebug | ConvertTo-Json -Compress)"
}
Assert-True $ctrlSaved.saved "Ctrl+S save state"
Assert-Equal $ctrlSaved.title "Ctrl S save check" "Ctrl+S saved title"

foreach ($theme in @(
    @{ index = 1; value = "warm"; bg = "#f3f0e8" },
    @{ index = 2; value = "light"; bg = "#f7f8fa" },
    @{ index = 0; value = "comfort"; bg = "#151a1f" }
)) {
    Invoke-Js "document.querySelectorAll('.theme-control button')[$($theme.index)].click()" | Out-Null
    $current = Invoke-Js "({ theme: document.documentElement.dataset.theme, stored: localStorage.getItem('fengvoice-theme'), bg: getComputedStyle(document.documentElement).getPropertyValue('--bg').trim(), notes: document.querySelectorAll('.note-item').length })"
    Assert-Equal $current.theme $theme.value "Applied theme"
    Assert-Equal $current.stored $theme.value "Stored theme"
    Assert-Equal $current.bg $theme.bg "Theme background color"
    Assert-Equal $current.notes 1 "Theme switch changed note data"
}
Reload-Page
Assert-Equal (Invoke-Js "document.documentElement.dataset.theme") "comfort" "Theme after refresh"

Send-Cdp -Method "Network.setBlockedURLs" -Params @{ urls = @("$apiUrl/*") } | Out-Null
Invoke-Js "document.querySelector('.primary-button').click()" | Out-Null
Start-Sleep -Milliseconds 1000
Write-Host "UI acceptance: offline draft"
$offline = Invoke-Js "({ notes: document.querySelectorAll('.note-item').length, offline: document.querySelector('.save-status').textContent.trim() === '\u79bb\u7ebf\u8349\u7a3f', banner: document.querySelector('.error-banner').textContent.includes('\u521b\u5efa\u5931\u8d25'), badge: document.querySelector('.note-item em').textContent === '\u79bb\u7ebf', editable: !document.querySelector('.title-input').disabled })"
Assert-Equal $offline.notes 2 "Offline draft list count"
Assert-True $offline.offline "Offline draft state"
Assert-True $offline.banner "Offline error banner is missing"
Assert-True $offline.badge "Offline draft badge"
Assert-True $offline.editable "Offline draft is not editable"

$editOfflineDraft = @'
(() => {
  const content = document.querySelector('textarea');
  const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
  setter.call(content, 'offline retained content');
  content.dispatchEvent(new Event('input', { bubbles: true }));
  window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
})()
'@
Invoke-Js $editOfflineDraft | Out-Null
Start-Sleep -Milliseconds 100
$offlineEditing = Invoke-Js "({ content: document.querySelector('textarea').value, bannerDismissed: !document.querySelector('.error-banner') })"
Assert-Equal $offlineEditing.content "offline retained content" "Offline input retention"
Assert-True $offlineEditing.bannerDismissed "Escape did not dismiss the error banner"

Send-Cdp -Method "Network.setBlockedURLs" -Params @{ urls = @() } | Out-Null
Invoke-Js "document.querySelector('.save-button').click()" | Out-Null
Start-Sleep -Milliseconds 1100
Wait-Until -Message "offline draft recovery save" -Condition {
    Invoke-Js "document.querySelector('.save-status')?.textContent.trim() === '\u5df2\u4fdd\u5b58' && Boolean(document.querySelector('.note-item em'))"
}
$recovered = Invoke-Js "({ saved: document.querySelector('.save-status').textContent.trim() === '\u5df2\u4fdd\u5b58', badge: document.querySelector('.note-item em').textContent })"
Assert-True $recovered.saved "Recovered draft save state"
Assert-Equal $recovered.badge "general" "Recovered draft server id"

Send-Cdp -Method "Emulation.setDeviceMetricsOverride" -Params @{ width = 390; height = 844; deviceScaleFactor = 1; mobile = $true } | Out-Null
Reload-Page
$mobile = Invoke-Js "({ overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth, width: document.documentElement.clientWidth })"
Assert-Equal $mobile.overflow $false "Mobile horizontal overflow"
Assert-Equal $mobile.width 390 "Mobile viewport width"
Send-Cdp -Method "Emulation.clearDeviceMetricsOverride" | Out-Null

Invoke-Js "fetch('$apiUrl/api/notes').then(r => r.json()).then(async notes => { for (const note of notes) await fetch('$apiUrl/api/notes/' + note.id, { method: 'DELETE' }); return true; })" | Out-Null

[PSCustomObject]@{
    online_create = "passed"
    autosave = "passed"
    refresh = "passed"
    chinese_search = "passed"
    ctrl_s = "passed"
    themes = "passed"
    offline_draft = "passed"
    offline_recovery = "passed"
    mobile_layout = "passed"
} | ConvertTo-Json -Compress
