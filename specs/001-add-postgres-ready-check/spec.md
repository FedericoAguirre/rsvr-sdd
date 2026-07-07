# Add PostgreSQL Readiness Check to App Startup Script

## Feature Overview

**Problem**: The Windows app startup script (`backend/start_app01.ps1`) attempts to launch the Django development server without verifying that the PostgreSQL database service is running and accepting connections. This causes startup failures with cryptic error messages when the database is unavailable, forcing developers to manually diagnose the issue.

**Solution**: Enhance `backend/start_app01.ps1` to check PostgreSQL readiness before launching the server, with clear status reporting, configurable retry logic, and graceful timeout handling.

**User Value**: Developers and DevOps engineers get a reliable, self-diagnosing startup experience that either confirms the database is ready or points directly to the root cause with actionable messages.

## User Scenarios & Testing

### Scenario 1: PostgreSQL is running and ready
**Given** a Windows development environment with PostgreSQL service running and the database created
**When** the user runs `start_app01.ps1`
**Then** the script successfully connects to PostgreSQL, reports "Database ready", and proceeds to start the Django dev server

### Scenario 2: PostgreSQL service is not running
**Given** a Windows development environment where the PostgreSQL service is stopped
**When** the user runs `start_app01.ps1`
**Then** the script attempts to connect for the configured retry duration
**And** after timeout, displays a clear error: "PostgreSQL is not reachable. Ensure the PostgreSQL service is running."
**And** the script exits with a non-zero exit code
**And** the Django dev server is not started

### Scenario 3: PostgreSQL credentials are missing or invalid
**Given** a Windows development environment where the `.env` file lacks database connection variables
**When** the user runs `start_app01.ps1`
**Then** the script detects the missing configuration before attempting connection
**And** displays: "Database configuration incomplete. Check DATABASE_URL or DB_* variables in .env"
**And** the script exits with a non-zero exit code

### Scenario 4: Database does not exist
**Given** a Windows development environment where PostgreSQL is running but the target database has not been created
**When** the user runs `start_app01.ps1`
**Then** the script confirms PostgreSQL is reachable but reports "Database '<name>' does not exist. Run migrations first."
**And** the script exits with a non-zero exit code

### Scenario 5: PostgreSQL becomes ready during retry window
**Given** a Windows development environment where PostgreSQL is restarting
**When** the user runs `start_app01.ps1`
**Then** the script retries connection every 2 seconds
**And** once PostgreSQL accepts connections, proceeds with normal startup
**And** reports "Database ready after N seconds"

## Functional Requirements

### FR1: Connection Parameter Discovery
The script must read PostgreSQL connection parameters from the environment (sourced from `.env`). Supported parameters: host, port, database name, user, password. The script shall support detection via standard Django database URL (`DATABASE_URL`) or individual `DB_*` variables.

### FR2: Readiness Probe
The script must attempt to establish a TCP connection to the PostgreSQL host:port, then perform a simple database-level query (`SELECT 1`) to confirm the database service is accepting queries. Both checks must succeed for the readiness check to pass.

### FR3: Retry with Backoff
If the initial connection attempt fails, the script must retry with a configurable interval (default 2 seconds) for up to a configurable maximum duration (default 30 seconds). Output a dot or status indicator for each retry attempt so the user knows the script is working.

### FR4: Graceful Error Handling
The script must differentiate between and report distinct error conditions:
- PostgreSQL host unreachable (network/service down)
- Authentication failure (wrong credentials)
- Database not found (database name does not exist)
- Missing configuration (env vars not set)

### FR5: Exit Behavior
If the readiness check fails after exhausting retries, the script must exit with a non-zero exit code and NOT start the Django dev server. If the check passes, it proceeds to `runserver`.

### FR6: Feedback to User
The script must display clear, human-readable status messages at each phase:
- Loading environment...
- Checking PostgreSQL readiness...
- Database ready ✓ (or ✗ with reason)
- Starting Django development server...

## Success Criteria

### SC1: Startup reliability
When PostgreSQL is running and reachable, the script starts the Django dev server within 5 seconds of completing the readiness check (excludes database connection time).

### SC2: Failure clarity
When PostgreSQL is unavailable, the script exits within the configured timeout + 5 seconds and displays an error message that identifies the specific failure reason without requiring the user to inspect logs or code.

### SC3: No impact on healthy startup
The addition of the readiness check adds no more than 1 second of overhead when PostgreSQL is already running and accepting connections.

### SC4: Recovery from transient failure
If PostgreSQL becomes available within the retry window, the script automatically proceeds with startup without manual intervention.

## Key Entities

### PostgreSQL Connection Config
- Host (string, default: localhost)
- Port (integer, default: 5432)
- Database name (string)
- Username (string)
- Password (string, sensitive)

### Retry Configuration
- Retry interval (integer, seconds, default: 2)
- Maximum retry duration (integer, seconds, default: 30)

## Assumptions

- The `.env` file is present in the project root and contains valid `DATABASE_URL` or individual `DB_*` PostgreSQL connection variables
- PostgreSQL client tools (`psql`) may not be installed; readiness check will use .NET TCP client and Npgsql if available, or fall back to raw TCP socket check
- The script runs on Windows PowerShell 5.1 or later (compatible with Windows 10/11 and Windows Server 2019+)
- Network connectivity from the development machine to the PostgreSQL host is available (no firewall blocking)
- The PostgreSQL service on Windows is named `postgresql-*` or is discoverable via `sc query` if local

## Dependencies

- `backend/start_app01.ps1` — the script to be modified
- `.env` file in project root — source of database connection parameters
- PowerShell 5.1+ runtime on Windows

## Out of Scope

- Cross-platform compatibility (Linux/macOS startup scripts are separate)
- Database migration execution (running `migrate`/`makemigrations`)
- Database creation (creating the database if it doesn't exist)
- Monitoring or health checks beyond startup time
- SSL/TLS certificate verification for PostgreSQL connections
