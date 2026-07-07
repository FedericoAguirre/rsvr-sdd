# Data Model: Update Restart Docs

## Summary

This feature does not introduce any new database entities, fields, or schema changes. It only updates documentation and adds a test.

## Artifacts Referenced

### docs/windows11_deployment.md

- **Location**: `docs/windows11_deployment.md`
- **Role**: The deployment guide being updated. The `## Start the App After Restart` section (currently lines 295–343) will be rewritten.

### .env File

- **Location**: `/D:Descargas\codigo\rsvr-sdd\.env` (on target Windows machine)
- **Role**: Environment variable file parsed by the PowerShell loader script. Contains `DATABASE_URL`, `SECRET_KEY`, `MEDIA_ROOT`, and other Django configuration.

### PowerShell Env Loader

- **Pattern**: Not a persistent artifact — it's an inline script executed at startup
- **Signature**: `Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object { $name, $value = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process') }`

### Test File

- **Location**: `backend/tests/test_restart_docs.py` (new)
- **Role**: Validates PowerShell command syntax by extracting commands from the markdown documentation

## No Schema Changes

No migrations required. The feature operates entirely within existing project documentation and test infrastructure.
