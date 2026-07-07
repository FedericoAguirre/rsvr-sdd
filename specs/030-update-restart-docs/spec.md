# Feature Specification: Update Restart Docs

**Feature Branch**: `030-update-restart-docs`

**Created**: 2026-07-06

**Status**: Draft

**Input**: Use the @ai/features/todos/15-Start_the_app_after_restart.md file to create the new feature spec

## User Scenarios & Testing

### User Story 1 - Update Auto-Start Documentation (Priority: P1)

As a developer deploying the reservation system on Windows 11, I want all three auto-start options to use a consistent PowerShell-based `.env` variable loading approach instead of the current `cmd.exe` / `waitress-serve` approach.

**Why this priority**: This is the core deliverable — replacing the outdated instructions with a consistent, correct approach across all startup methods that uses the project's actual toolchain (`uv`, `manage.py runserver`) and loads environment variables from `.env`.

**Independent Test**: Can be fully tested by following the updated instructions on a Windows 11 Home machine and confirming the app starts automatically after reboot without manual intervention.

**Acceptance Scenarios**:

1. **Given** any of the three updated auto-start options, **When** a developer follows the instructions, **Then** the `.env` variables are loaded into the process environment via PowerShell
2. **Given** the `.env` variables are loaded, **When** the startup command executes, **Then** `uv run .\manage.py runserver` starts the Django development server
3. **Given** the deployment path is `D:\Descargas\codigo\rsvr-sdd`, **When** the PowerShell script runs, **Then** relative paths resolve correctly from this directory
4. **Given** the laptop restarts, **When** Windows boots and the task runs, **Then** the application is accessible at `http://localhost:8000`

---

### User Story 2 - Add Test Method for the New Approach (Priority: P2)

As a developer, I want a test method that validates the new auto-start PowerShell commands so that the documentation change can be verified in CI without a physical Windows machine.

**Why this priority**: Adding test coverage ensures the PowerShell commands are syntactically valid and the instructions remain consistent with the project setup.

**Independent Test**: Can be tested by running the test script and confirming it passes.

**Acceptance Scenarios**:

1. **Given** a test method for the auto-start approach, **When** the test is executed, **Then** it validates the PowerShell `.env` loader script parses correctly by checking the syntax of the inline command extracted from the documentation
2. **Given** a test method for the auto-start approach, **When** the test is executed, **Then** it validates that the `uv run .\manage.py runserver` command path (`D:\Descargas\codigo\rsvr-sdd`) resolves to a known project structure
3. **Given** a test method for the auto-start approach, **When** the test is executed, **Then** it does NOT attempt to run PowerShell or start the server (no execution, only static analysis)

---

### Edge Cases

- What happens when the `.env` file has comments or blank lines? The PowerShell script filters them out (`Where-Object { $_ -match '=' -and $_ -notmatch '^#' }`)
- What happens if `uv` is not installed? The Task Scheduler task will fail and the app won't start; the documentation should note this prerequisite
- What happens if the project path contains spaces? PowerShell handles paths with spaces correctly when quoted
- What happens if multiple `.env` variables have the same name? The last one wins (standard behavior)
- What happens on a path other than `D:\Descargas\codigo\rsvr-sdd`? The instructions should use a variable for the project root so it can be adapted
- What if the `.env` file has open NTFS permissions? The documentation should recommend `icacls .env /inheritance:r /grant "Administrators:R"` to restrict access

## Clarifications

### Session 2026-07-06

- Q: How should Task Scheduler invoke PowerShell? → A: Inline commands via powershell.exe -Command
- Q: What should the test method validate? → A: PowerShell command syntax and path resolution, without actual execution
- Q: Should Options 1 and 2 also be updated to load .env? → A: Yes, update all three options to use the .env loader pattern for consistency
- Q: Should Options 1 and 2 also switch from waitress-serve to uv run? → A: Yes, all three options use uv run .\manage.py runserver
- Q: Should the documentation include .env file security guidance? → A: Yes, add a brief security note about NTFS file permissions

## Requirements

### Functional Requirements

- **FR-001**: The "Option 3: Auto-Start Using Task Scheduler" section MUST be updated to use PowerShell instead of `cmd.exe`
- **FR-002**: The updated section MUST include an `.env` loader script that parses `KEY=VALUE` lines, skipping comments (`#`) and blank lines
- **FR-003**: All three options MUST use `uv run .\manage.py runserver` as the application start command
- **FR-004**: The PowerShell script MUST set environment variables in the process scope using `[System.Environment]::SetEnvironmentVariable(..., 'Process')`
- **FR-005**: The PowerShell commands MUST resolve relative paths correctly from `D:\Descargas\codigo\rsvr-sdd`
- **FR-006**: Options 1 (Manual Start) and 2 (Launcher Script) MUST also be updated to load .env variables using the same PowerShell pattern before starting the application
- **FR-007**: A test method MUST be added or updated to validate the new PowerShell auto-start approach
- **FR-008**: The Task Scheduler action MUST use `powershell.exe` with the `-Command` flag passing the entire inline script (env loader + uv run)
- **FR-009**: The documentation MUST include a security note about restricting `.env` file access via NTFS permissions (icacls) to prevent credential exposure

### Key Entities

- **windows11_deployment.md**: The deployment guide document being updated
- **Task Scheduler Task**: The Windows scheduled task configuration for auto-starting the application
- **.env File**: The environment variable file parsed by the PowerShell loader script
- **Test Method**: A test that validates the PowerShell commands and project paths

## Success Criteria

### Measurable Outcomes

- **SC-001**: A developer following the updated Option 3 can successfully start the app after reboot without manual intervention (verified by successful HTTP response at localhost:8000)
- **SC-002**: The PowerShell `.env` loader correctly loads all non-comment `KEY=VALUE` lines from `.env` into the process environment
- **SC-003**: The test method passes in CI and validates the PowerShell command syntax
- **SC-004**: The total time to set up auto-start from scratch is under 10 minutes for a developer familiar with Windows

## Assumptions

- The project location `D:\Descargas\codigo\rsvr-sdd` is the target deployment path on the Windows machine
- `uv` (Python package manager) is already installed on the system per the project prerequisites
- The `.env` file exists at the project root with the correct database and application configuration
- The application uses Django's built-in development server (`manage.py runserver`) for local deployment
- Options 1 (Manual Start) and 2 (Launcher Script) will be updated to include the same .env loading pattern for consistency
- PostgreSQL service is configured for automatic startup (unchanged from current documentation)
