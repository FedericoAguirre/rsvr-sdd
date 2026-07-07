# Data Model: PostgreSQL Readiness Check

## PostgreSQL Connection Config

Parsed from environment variables (sourced from `.env`). Used to establish the readiness probe connection.

| Field | Type | Source | Default | Required | Sensitive |
|---|---|---|---|---|---|
| Host | string | `DATABASE_URL` (parsed) or `$env:POSTGRES_HOST` | `localhost` | No | No |
| Port | integer | `DATABASE_URL` (parsed) or `$env:POSTGRES_PORT` | `5432` | No | No |
| Database | string | `DATABASE_URL` (parsed) or `$env:POSTGRES_DB` | — | Yes | No |
| Username | string | `DATABASE_URL` (parsed) or `$env:POSTGRES_USER` | — | Yes | No |
| Password | string | `DATABASE_URL` (parsed) or `$env:POSTGRES_PASSWORD` | — | Yes | Yes |

### DATABASE_URL Format

```
postgres://<user>:<password>@<host>:<port>/<database>
```

Parsed via regex: `^postgres://(.+):(.+)@(.+):(\d+)/(.+)$`

### Resolution Precedence

1. If `DATABASE_URL` is set → parse it, extract all 5 fields
2. Else if individual `POSTGRES_*` vars are set → use them individually
3. Else → error: missing configuration

## Retry Configuration

| Field | Type | Source | Default | Description |
|---|---|---|---|---|
| Retry Interval | integer (seconds) | Script constant | 2 | Time between readiness check attempts |
| Max Retry Duration | integer (seconds) | Script constant | 30 | Total time before giving up |
| Max Attempts | integer | Derived | 15 | `MaxRetryDuration / RetryInterval` (ceiling) |

## State Machine

```
                ┌─────────────────────────┐
                │  Start: Load .env vars   │
                └──────────┬──────────────┘
                           │
                           ▼
                ┌─────────────────────────┐
                │  Parse connection config │
                └──────────┬──────────────┘
                           │
              ┌────────────┴───────────┐
              │                        │
              ▼                        ▼
    ┌──────────────────┐     ┌──────────────────┐
    │ Config valid     │     │ Config invalid   │
    └────────┬─────────┘     └────────┬─────────┘
             │                        │
             ▼                        ▼
    ┌──────────────────┐     ┌──────────────────┐
    │ TCP socket check │     │ Exit 1: "missing │
    │ (host:port)      │     │ configuration"   │
    └────────┬─────────┘     └──────────────────┘
             │
    ┌────────┴──────────┐
    │                   │
    ▼                   ▼
┌────────────┐    ┌──────────────┐
│ TCP OK     │    │ TCP failed   │
└──────┬─────┘    └──────┬───────┘
       │                 │
       ▼                 ▼
┌────────────┐    Wait $interval
│ pg_isready │    ──────────────►  retry loop (max $duration)
│ check      │         │
└──────┬─────┘         │
       │               │
    ┌──┴──────────┐    │
    │             │    │
    ▼             ▼    │
┌────────┐  ┌────────┐ │
│ Ready  │  │ Not    │ │
│        │  │ ready  │ │
└───┬────┘  └───┬────┘ │
    │           │      │
    │           └──────┘
    ▼
┌────────────┐
│ Proceed to │
│ runserver  │
└────────────┘
```

## Validation Rules

| Rule | Condition | Action |
|---|---|---|
| Missing connection info | Neither `DATABASE_URL` nor required `POSTGRES_*` vars are set | Exit 1, show config error |
| Unreachable host | TCP connection fails after all retries | Exit 1, show unreachable error |
| Service not accepting | TCP succeeds but `pg_isready` (or TCP-only fallback) fails for all retries | Exit 1, show service not ready error |
| Auth failure | `pg_isready` indicates authentication error | Exit 1, show auth error |
| DB not found | `pg_isready` with dbname fails but server is accepting | Exit 1, show missing database error |
| Healthy | TCP succeeds + pg_isready passes | Proceed to runserver |
