# GitHub and Baidu Netdisk Sync

This project uses two separate sync paths:

- GitHub stores committed source code.
- Baidu Netdisk stores a local project snapshot in the folder configured by `sync-to-baidu.ps1`.

## After Restart

Before using GitHub CLI, make sure the local proxy is running on `127.0.0.1:10808`.

Run the health check:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\ops\check-github-cli.ps1
```

The check verifies:

- local proxy port
- `gh auth status`
- repository API access
- `git fetch origin`
- branch divergence
- `git push --dry-run origin HEAD`

## GitHub CLI Commands

Use the proxy wrapper for direct `gh` commands:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\ops\gh-proxy.ps1 repo view fengking20171209-web/FengVoice
```

If the proxy port changes, set `FENGVOICE_GITHUB_PROXY` first:

```powershell
$env:FENGVOICE_GITHUB_PROXY = "socks5h://127.0.0.1:10808"
```

## Save Progress

Run:

```bat
save-progress.bat
```

This checks GitHub CLI/Git status, prints the working tree state, and then mirrors the project snapshot to Baidu Netdisk.

## Credential Note

GitHub CLI is currently configured to store its token in:

`C:\Users\Aerc\AppData\Roaming\GitHub CLI\hosts.yml`

This was chosen to bypass a broken Windows keyring entry. Later optimization should migrate the token back to the Windows credential store after cleaning the stale keyring state.
