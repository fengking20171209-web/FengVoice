# PN-0.5 Startup & Local Hardening Final Report

## Result

WARN

PN-0.5 completed the startup script and local hardening tasks. It created a Windows launcher, added the missing Python bytecode ignore pattern, backed up `_local/patches` to a project-external directory, and generated smoke/backup/final reports.

WARN reason: startup scripts were not used to launch long-running services in this phase, and the smoke secret scan produced a false positive on the comment word `secrets`.

## Created Files

- `start-notes.ps1`
- `start-notes.bat`
- `reports/personal-notes/pn0_5/start-script-smoke.md`
- `reports/personal-notes/pn0_5/patches-backup-report.md`
- `reports/personal-notes/pn0_5/final-pn0-5-report.md`

## `.gitignore` Update

Added missing local runtime artifact rules:

```gitignore
*.py[cod]
.vite/
data/
```

Existing rules already covered:

- `__pycache__/`
- `*.pyc`
- `.venv/`
- `node_modules/`
- `dist/`
- `.vite/`
- `_local/`
- `*.log`
- `runtime/`
- `public/uploads/`
- `data/`

## Patch Backup

Source:

```text
D:\Projects\FengVoice\_local\patches\
```

Target:

```text
D:\Backups\FengVoice_Patches_Bak\patches-20260606-103054\
```

Result:

- File count: 19
- Total size: 137K
- Source not deleted
- Backup manifest created in the target directory

## Startup Script Usage

Double-click:

```text
start-notes.bat
```

Or run:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\start-notes.ps1
```

The script opens separate PowerShell windows for:

- API: `http://127.0.0.1:8000`
- Web: `http://127.0.0.1:5173`

Then it opens:

```text
http://127.0.0.1:5173/
```

The script does not install dependencies. If Python venv or `apps/web/node_modules` is missing, it warns the user.

## Smoke Test Summary

- `start-notes.ps1` exists: PASS
- `start-notes.bat` exists: PASS
- PowerShell parse: PASS
- Non-local URL scan: PASS
- Localhost/127.0.0.1 only: PASS
- Secret scan: WARN false positive on comment text
- Long-running service startup: NOT RUN

## Business Code Safety

No business/runtime code paths were modified:

- `apps/web/`: none
- `services/api/`: none
- `runtime/`: none
- `public/uploads/`: none
- `data/`: none

## Not Done

- Did not push.
- Did not merge.
- Did not tag.
- Did not apply patches.
- Did not restore API draft work.
- Did not process OSS tracked draft files.
- Did not create PN-1 note.
- Did not write production GBrain.
- Did not connect to cloud services, COS, MCP, or SSH.

## Recommendation

Proceed to PN-1 after reviewing the PN-0.5 diff. The first real note should be:

```text
工作区清理与主线恢复复盘
```

Suggested tags:

```text
workflow, decision, review, notes
```

GBrain status:

```text
candidate, but do not write production GBrain automatically
```
