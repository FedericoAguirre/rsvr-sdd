# Feature Specification: Remove Docker for Web Development, Keep Database

**Feature Branch**: `053-web-docker-removal`

**Created**: 2026-07-30

**Status**: Draft

**Input**: User description: "Remove Docker containerization of the Django web application while keeping PostgreSQL database in Docker for local development."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Set Up a Local Development Environment (Priority: P1)

As a developer joining the project, I want to run a single setup script that checks dependencies, configures my environment, starts the database, and installs Python packages so that I can start contributing in minutes rather than debugging Docker configuration.

**Why this priority**: Without a working local environment, no other development can happen. This is the entry point for every contributor.

**Independent Test**: Can be fully tested on a clean checkout by running `bash setup.sh` and verifying the server starts with `make serve`.

**Acceptance Scenarios**:

1. **Given** a developer has cloned the repo on a machine with `uv` and Docker installed, **When** they run `bash setup.sh`, **Then** the script completes without errors, creates a `.env` file, installs dependencies, starts PostgreSQL in Docker, and runs migrations.
2. **Given** a developer runs `setup.sh` but `uv` is not installed, **When** the script checks dependencies, **Then** it prints a clear error message and exits without making changes.
3. **Given** a developer runs `setup.sh` but Docker is not installed, **When** the script checks dependencies, **Then** it prints a clear error message and exits without making changes.
4. **Given** a developer runs `setup.sh` and a `.env` file already exists, **When** the script checks for `.env`, **Then** it skips the copy step and uses the existing file.

---

### User Story 2 - Run the Development Server Locally (Priority: P1)

As a developer actively working on the codebase, I want to start the Django dev server directly on my machine (not inside Docker) so that I get instant hot-reload, native I/O performance, and seamless IDE debugger integration.

**Why this priority**: This is the core development loop — edit, save, see changes. Speed here directly impacts developer productivity.

**Independent Test**: Can be fully tested by running `make serve` and confirming the app is accessible at `http://localhost:8000`, and that editing a Python file causes an immediate reload.

**Acceptance Scenarios**:

1. **Given** the database is running via `make db-up`, **When** I run `make serve`, **Then** the Django dev server starts on `http://localhost:8000` within 5 seconds.
2. **Given** the Django dev server is running, **When** I edit a Python file and save, **Then** the server reloads and the change is reflected in under 2 seconds.
3. **Given** the Django dev server is running, **When** I attach a debugger (e.g., VS Code or PyCharm), **Then** breakpoints are hit and I can step through code.

---

### User Story 3 - Run Tests and Quality Checks Locally (Priority: P2)

As a developer, I want to run the full test suite and linter directly on my machine without Docker overhead so that I get fast feedback during development.

**Why this priority**: Fast feedback loops are critical for maintaining development velocity, but the test/lint workflow is secondary to the basic ability to run the server.

**Independent Test**: Can be fully tested by running `make test` and `make lint` and verifying they work with the same output as before.

**Acceptance Scenarios**:

1. **Given** the database is running and dependencies are installed, **When** I run `make test`, **Then** pytest executes all tests and reports results.
2. **Given** dependencies are installed, **When** I run `make lint`, **Then** ruff checks all files and reports issues.
3. **Given** the codebase has no formatting issues, **When** I run `make format`, **Then** ruff formats all files in place.

---

### Edge Cases

- What happens when a developer already has PostgreSQL running on port 5432? The Docker container will fail to start due to port conflict. The error message should be clear enough to diagnose.
- What happens when the `.env` file is missing required variables? The setup script creates it from `.env.example` and warns the user to review it.
- What happens when a team member uses Windows? The `setup.sh` script is bash-specific and will not work. Users on Windows need to use Git Bash, WSL, or manual setup.
- What happens when the database container is stopped but the server is still running? The server will return database connection errors until the database is restarted.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project MUST provide a `setup.sh` bootstrap script that checks for `uv`, Docker, and Docker Compose before proceeding.
- **FR-002**: The `setup.sh` script MUST create a `.env` file from `.env.example` if one does not already exist.
- **FR-003**: The `setup.sh` script MUST install Python dependencies via `uv sync` before starting the server.
- **FR-004**: The project MUST provide a Makefile target (`make db-up`) to start only the PostgreSQL container.
- **FR-005**: The project MUST provide a Makefile target (`make db-stop`) to stop the PostgreSQL container.
- **FR-006**: The project MUST provide a Makefile target (`make serve`) to start the Django dev server locally via `uv run`.
- **FR-007**: The project MUST provide Makefile targets for common tasks (`make test`, `make lint`, `make format`, `make migrate`, `make seed`, `make createsuperuser`).
- **FR-008**: The project MUST retain the ability to build and test the full Docker stack for pre-deployment verification via Makefile targets (`make docker-build`, `make docker-up`, `make docker-down`).
- **FR-009**: The `docker-compose.yml` file MUST be updated to contain only the database service and its associated volume configuration.
- **FR-010**: The `.env.example` file MUST be updated so that `DATABASE_URL` uses `localhost` instead of a Docker service name.
- **FR-011**: The README MUST be updated with local development setup instructions that replace the Docker-based workflow.

### Key Entities

No new data entities are introduced by this feature. The existing data model (PostgreSQL database, reservations, clients, payments, etc.) remains unchanged. The only change is how the development environment connects to the database — using `localhost:5432` directly rather than through a Docker network.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can go from a clean checkout to a running dev server in under 3 minutes using `bash setup.sh && make serve`.
- **SC-002**: The Django dev server starts in under 5 seconds from running `make serve`.
- **SC-003**: Hot-reload reflects Python file changes in under 2 seconds (measured from save to server reload).
- **SC-004**: All existing tests pass when run via `make test` (same test count and results as the Docker-based workflow).
- **SC-005**: The database can be cleanly started and stopped using `make db-up` and `make db-stop` without errors.
- **SC-006**: The full Docker stack build and test workflow (`make docker-build && make docker-up`) still works for pre-deployment verification.
- **SC-007**: `make lint` runs without errors on the committed codebase.

## Assumptions

- All developers have `uv` installed (or are willing to install it) as the Python package manager.
- All developers have Docker and Docker Compose installed for running the database container.
- The existing `.env.example` file already exists and can be used as a template for `.env`.
- The application's `settings.py` already reads `DATABASE_URL` from the environment and does not need code changes.
- Developers on Windows will use Git Bash, WSL, or manually follow the setup steps rather than running `setup.sh` directly.
- The project uses macOS or Linux as the primary development OS — Windows is a secondary concern.
- Pre-deployment Docker testing is still required and will remain as an explicit workflow step.
