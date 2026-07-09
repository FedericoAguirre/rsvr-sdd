# Research: PostgreSQL Readiness Check for PowerShell Startup Script

## Phase 0 — Findings

### Decision: PostgreSQL Health Check Method in PowerShell

**Decision**: Two-tier check: (1) TCP socket connection via `System.Net.Sockets.TcpClient`, (2) `pg_isready` command if available. Fallback to TCP-only check with a warning if `pg_isready` is not found.

**Rationale**:
- `System.Net.Sockets.TcpClient` is built into .NET Framework / .NET Core and available in all PowerShell 5.1+ environments without additional dependencies — satisfies FR2's TCP connection requirement
- `pg_isready` is a lightweight PostgreSQL utility that performs the same health check PostgreSQL itself uses; it comes with PostgreSQL client tools and is commonly installed on developer machines — satisfies FR2's database-level query requirement
- The two-tier approach works with zero dependencies in the worst case while providing the best diagnostic depth when tools are available
- Windows Docker Desktop users will have `pg_isready` available inside containers but not on the host; the TCP fallback handles this case

**Alternatives considered**:
- Npgsql .NET assembly (rejected: requires `Install-Package` or manual assembly download; not guaranteed available on developer machines)
- `System.Data.Odbc` with PostgreSQL ODBC driver (rejected: requires ODBC driver installation and DSN configuration — heavy dependency for a startup script)
- Raw PostgreSQL wire protocol implementation via `System.Net.Sockets` (rejected: overly complex for a health check; the startup packet format is version-specific and fragile)
- `psql -c "SELECT 1"` (rejected: requires full psql client; slower startup than pg_isready; overkill for a simple liveness check)

### Decision: Connection Parameter Parsing Strategy

**Decision**: Parse `DATABASE_URL` environment variable using a regex match in PowerShell. Fall back to individual `POSTGRES_*` variables (`POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`) as a secondary source. Default host to `localhost` and port to `5432`.

**Rationale**:
- The existing `.env.example` uses `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` (not `DB_*` as the spec assumed) — using `POSTGRES_*` matches the actual project convention
- The existing `settings.py` also parses `DATABASE_URL` with a regex — mirroring this approach in PowerShell maintains consistency
- The existing `docker-compose.yml` constructs `DATABASE_URL` from individual `POSTGRES_*` vars — supporting both sources covers all deployment modes
- Defaults of `localhost:5432` match the Docker Compose and Django defaults

**Alternatives considered**:
- Only `DATABASE_URL` parsing (rejected: doesn't cover cases where only individual `POSTGRES_*` vars are set)
- Only `POSTGRES_*` vars (rejected: `DATABASE_URL` is the standard Django pattern used in settings.py)
- Connection string builder approach (rejected: adds complexity; simple regex and defaults cover all cases)

**Actual env vars in use** (from `.env.example`):
```
POSTGRES_DB=rsvr
POSTGRES_USER=rsvr
POSTGRES_PASSWORD=change-me-to-a-strong-password
```

**DATABASE_URL construction** (from `docker-compose.yml`):
```
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
```

**DATABASE_URL parsing** (from `settings.py`):
```python
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://rsvr:rsvr@localhost:5432/rsvr")
match = re.match(r"postgres://(.+):(.+)@(.+):(\d+)/(.+)", DATABASE_URL)
```

### Decision: Retry Logic Implementation

**Decision**: Use a `while` loop with `Start-Sleep -Seconds $retryInterval` inside the script. Track elapsed time with `[System.Diagnostics.Stopwatch]`. Display a dot per attempt on the same line.

**Rationale**:
- Pure PowerShell, no external dependencies
- `Stopwatch` provides precise elapsed time tracking without external calls
- Writing a dot per attempt gives visible progress without flooding the console
- Configurable via variables at the top of the script for easy tuning

**Alternatives considered**:
- PowerShell workflow / job-based retry (rejected: over-engineering for a simple sequential retry loop)
- External retry tool (rejected: no such tool is guaranteed available on Windows)
- Recursive function call (rejected: stack depth concerns; loop is cleaner)

### Decision: Error Message Granularity

**Decision**: Detect four distinct failure modes and display corresponding messages:

| Failure Mode | Detection Method | Message |
|---|---|---|
| Missing config | Check if required env vars are empty | "Database configuration incomplete. Check DATABASE_URL or POSTGRES_* variables in .env" |
| Host unreachable | `TcpClient.Connect()` throws `System.Net.Sockets.SocketException` | "PostgreSQL is not reachable at {host}:{port}. Ensure the PostgreSQL service is running." |
| Auth failure | `pg_isready` exit code indicates auth failure; TCP succeeded | "PostgreSQL at {host}:{port} is reachable but authentication failed. Check POSTGRES_USER and POSTGRES_PASSWORD." |
| DB not found | `pg_isready` with dbname returns non-zero; TCP + server auth OK | "Database '{dbname}' does not exist on {host}:{port}. Create it or check POSTGRES_DB." |

**Rationale**:
- TCP exception type is reliable for distinguishing connection failure from other errors
- `pg_isready` exit codes distinguish "server not accepting connections" from "auth failed" from "OK"
- When `pg_isready` is unavailable, only "reachable" vs "unreachable" can be distinguished — the script will note this limitation in output

**Alternatives considered**:
- Parsing error stream text from pg_isready (rejected: error text varies by locale; exit codes are stable)
- Single generic error message (rejected: defeats the purpose of FR4's differentiation requirement)

### Decision: DATABASE_URL vs POSTGRES_* Precedence

**Decision**: `DATABASE_URL` takes precedence when set. If absent, fall back to individual `POSTGRES_*` variables. This mirrors Django's configuration pattern where `DATABASE_URL` is the primary source.

**Rationale**:
- Docker Compose sets `DATABASE_URL` explicitly — developers using Docker Desktop will have this set
- Manual `.env` setups may use either format — supporting both avoids breakage
- `DATABASE_URL` is more self-contained (single var with all connection info)
