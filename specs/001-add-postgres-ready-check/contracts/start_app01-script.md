# Contract: `start_app01.ps1`

## Overview

Windows PowerShell startup script for the rsvr-sdd Django application. Loads environment variables from `.env`, checks PostgreSQL readiness, then starts the Django development server.

## Input Contract

### Environment Variables Read (from `.env`)

| Variable | Required | Purpose |
|---|---|---|
| `DATABASE_URL` | No* | Full PostgreSQL connection string |
| `POSTGRES_DB` | No* | Database name (fallback if no DATABASE_URL) |
| `POSTGRES_USER` | No* | Database user (fallback if no DATABASE_URL) |
| `POSTGRES_PASSWORD` | No* | Database password (fallback if no DATABASE_URL) |
| `POSTGRES_HOST` | No | Database host (default: localhost) |
| `POSTGRES_PORT` | No | Database port (default: 5432) |

*Either `DATABASE_URL` OR the set of `POSTGRES_DB` + `POSTGRES_USER` + `POSTGRES_PASSWORD` must be set.

### Side Effects

- Sets process-level environment variables from `.env`
- Changes directory to `D:\Descargas\codigo\rsvr-sdd\backend`

## Output Contract

### Exit Codes

| Exit Code | Meaning |
|---|---|
| 0 | PostgreSQL ready, Django dev server started successfully |
| 1 | Configuration error — missing or incomplete database env vars |
| 2 | PostgreSQL unreachable — TCP connection failed after all retries |
| 3 | PostgreSQL not accepting connections — TCP OK but service not ready |
| 4 | PostgreSQL authentication failure — credentials rejected |

### Console Output

```
Loading environment...
Checking PostgreSQL readiness...
  ✔ Database ready            → proceed to startup
  ✖ <error message>           → exit with error code

Starting Django development server...
```

### Status Messages

| Condition | Message |
|---|---|
| Healthy, proceeding | "Database ready" |
| Config missing | "Database configuration incomplete. Check DATABASE_URL or POSTGRES_* variables in .env" |
| Host unreachable | "PostgreSQL is not reachable at {host}:{port}. Ensure the PostgreSQL service is running." |
| Auth failure | "PostgreSQL at {host}:{port} is reachable but authentication failed. Check POSTGRES_USER and POSTGRES_PASSWORD." |
| DB not found | "Database '{dbname}' does not exist on {host}:{port}. Create it or check POSTGRES_DB." |
| Retry progress | "." (one dot per failed attempt, same line) |
| Recovery after retry | "Database ready after N seconds" |

## Dependencies

| Dependency | Required | Notes |
|---|---|---|
| PowerShell 5.1+ | Yes |  |
| .NET Framework 4.5+ | Yes | For `System.Net.Sockets.TcpClient` |
| `pg_isready` | No | Optional; provides deeper diagnostics if available |
| PostgreSQL service | At startup | What we're checking for |
