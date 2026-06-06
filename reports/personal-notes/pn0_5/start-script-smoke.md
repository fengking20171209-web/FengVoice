# PN-0.5 Start Script Smoke Test

## Result

WARN

Startup scripts were created and passed existence, PowerShell parse, and remote URL checks. No services were started for a long-running test.

WARN reason: the sensitive-string scan matched the plain English word `secrets` in a safety comment. No API key, token, password, or private key value was found.

## Files Checked

- `start-notes.ps1`
- `start-notes.bat`

## Checks

| Check | Result | Notes |
| --- | --- | --- |
| `start-notes.ps1` exists | PASS | File exists. |
| `start-notes.bat` exists | PASS | File exists. |
| PowerShell parse | PASS | `[scriptblock]::Create((Get-Content -Raw ...))` succeeded. |
| Secret scan | WARN | False positive on comment text: `read secrets`; no secret value found. |
| Remote URL scan | PASS | PCRE2 scan found no non-local `http://` or `https://` URL. |
| Local URL use | PASS | Script uses `http://127.0.0.1:5173/`, `127.0.0.1:8000`, and `127.0.0.1:5173`. |
| Long-running service start | NOT RUN | Deferred until user wants manual PN-0 startup validation. |

## Notes

The script intentionally does not install Python or Node dependencies. It warns if `.venv` or `apps/web/node_modules` is missing.
