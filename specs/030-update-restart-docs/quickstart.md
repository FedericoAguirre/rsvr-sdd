# Quickstart: Update Restart Docs

## What you need to know

A documentation-only feature — update `docs/windows11_deployment.md` to replace the `cmd.exe` + `waitress-serve` startup instructions with a PowerShell `.env` loader + `uv run .\manage.py runserver` approach.

## Files to modify

1. **`docs/windows11_deployment.md`** — Rewrite all three startup options in the `## Start the App After Restart` section:
   - Option 1 (Manual Start): Single PowerShell command
   - Option 2 (Launcher Script): `.bat` or `.ps1` wrapper
   - Option 3 (Task Scheduler): `powershell.exe -Command` action
   - Add security note about `.env` file permissions

2. **`backend/tests/test_restart_docs.py`** — New file: static analysis tests that extract PowerShell commands from the markdown and validate their syntax

## No database changes

No migrations. No new models. No application code changes.

## Core PowerShell pattern

```powershell
Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object { $name, $value = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process') }; uv run .\manage.py runserver
```

## Testing

```bash
pytest backend/tests/test_restart_docs.py
# Expected: Tests extract PowerShell commands from docs/ and validate syntax
# No Windows/PowerShell execution required
```

## Commands

```bash
# Lint
ruff check docs/windows11_deployment.md backend/tests/test_restart_docs.py

# Run tests
pytest backend/tests/test_restart_docs.py -v
```
