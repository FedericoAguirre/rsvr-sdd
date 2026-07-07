# Contracts: Update Restart Docs

## Documentation Contract

### Modified Section: `## Start the App After Restart`

**File**: `docs/windows11_deployment.md`

**Current**: Three options using `cmd.exe` + `waitress-serve` (lines 295–343)

**Updated**: Three options all using PowerShell .env loader + `uv run .\manage.py runserver`

### Option 1 — Manual Start

A single PowerShell command the developer runs manually in a terminal.

### Option 2 — Launcher Script

A `.bat` file (or PowerShell `.ps1`) that wraps the env loader + server command for double-click execution.

### Option 3 — Task Scheduler Auto-Start

A Task Scheduler task that runs `powershell.exe -Command "<env loader>; uv run .\manage.py runserver"` at system startup or logon.

## PowerShell Command Contract

The inline PowerShell script MUST follow this structure:

```
Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object { $name, $value = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process') }; uv run .\manage.py runserver
```

**Requirements**:
1. Filter out comment lines (starting with `#`)
2. Filter out blank lines (no `=` sign)
3. Split on first `=` only (values may contain `=`)
4. Trim whitespace from name and value
5. Set variables in Process scope only
6. Chain `uv run .\manage.py runserver` after env loader with `;`

## Security Contract

A security note MUST be included advising:
- Restrict `.env` file permissions: `icacls .env /inheritance:r /grant "Administrators:R"`
- Task Scheduler stores commands in plain text — any user with Task Scheduler read access can see credentials
- Consider using Windows Credential Manager for secrets if additional security is needed

## Test Contract

- **Test file**: `backend/tests/test_restart_docs.py` (new)
- **Test approach**: Static analysis of PowerShell commands extracted from `docs/windows11_deployment.md`
- **Validates**: Env loader syntax, path resolution, no actual PowerShell execution
- **CI requirement**: Must pass on macOS/Linux CI (no Windows dependency)

## Modified Files

| File | Change |
|------|--------|
| `docs/windows11_deployment.md` | Rewrite Option 3; align Options 1 and 2 |
| `backend/tests/test_restart_docs.py` | New: PowerShell command validation tests |
