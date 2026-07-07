# Quickstart: Add PostgreSQL Readiness Check

## Implementation Steps

### Step 1: Read the spec and plan

```
spec.md              — Feature specification (requirements, scenarios)
plan.md              — Implementation plan (structure, gates)
research.md          — Researched decisions (check method, parsing, retry)
data-model.md        — Data model (connection config, state machine)
contracts/           — Interface contract (exit codes, messages)
```

### Step 2: Modify `backend/start_app01.ps1`

The existing 4-line script (`cd → load .env → cd backend → runserver`) needs the PostgreSQL readiness check inserted between env loading and runserver.

**Key implementation points**:

1. **Parse connection parameters**: After loading `.env`, extract `DATABASE_URL` or `POSTGRES_*` vars. Use regex for DATABASE_URL: `^postgres://(.+):(.+)@(.+):(\d+)/(.+)$`

2. **TCP socket check**: Use `$tcp = New-Object System.Net.Sockets.TcpClient; $tcp.Connect($host, $port); $tcp.Close()` wrapped in try/catch

3. **pg_isready check** (optional): If `Get-Command pg_isready` succeeds, run `pg_isready -h $host -p $port -d $dbname -U $user` and check `$LASTEXITCODE`

4. **Retry loop**: `$sw = [System.Diagnostics.Stopwatch]::StartNew()`; while `$sw.Elapsed.TotalSeconds -lt $maxDuration`; `Start-Sleep -Seconds $interval`; write a dot per attempt

5. **Exit codes per contract**: Use `exit 1` through `exit 4` per the contract

6. **Console output**: Follow the format in `contracts/start_app01-script.md`

### Step 3: Manual Test Protocol

Run each of these from a PowerShell terminal (no CI available):

| Test | Setup | Expected Result |
|---|---|---|
| PostgreSQL running | Start PostgreSQL service, run script | Script says "Database ready", starts dev server |
| PostgreSQL stopped | Stop PostgreSQL service, run script | Script retries 30s, exits with code 2, shows unreachable error |
| Missing .env | Rename .env, run script | Script exits with code 1, shows config error |
| Wrong password | Set wrong POSTGRES_PASSWORD in .env, run script | Script exits with code 4, shows auth failure |
| PostgreSQL starts mid-retry | Stop PostgreSQL, run script, start PostgreSQL within 30s | Script recovers, shows "Database ready after N seconds" |

### Step 4: Verify exit codes

After each test, run `$LASTEXITCODE` in PowerShell to confirm the exit code matches the contract.
