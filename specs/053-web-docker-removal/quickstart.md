# Quickstart Validation Guide: Remove Docker for Web Development

**Purpose**: Run these validation scenarios to confirm the feature works end-to-end.

## Prerequisites

- Python 3.12+ with `uv` installed
- Docker & Docker Compose
- No existing PostgreSQL running on port 5432 (or stop it first)

## Validation Scenarios

### Scenario 1: Fresh Setup (Complete Bootstrap)

```bash
# On a clean checkout:
bash setup.sh

# Expected:
# ✓ Dependencies checked (uv, docker, docker-compose)
# ✓ .env created from .env.example
# ✓ Dependencies installed via uv sync
# ✓ PostgreSQL started in Docker
# ✓ Migrations run
# ✓ (optional) Demo data seeded
# ✓ (optional) Admin account created
```

### Scenario 2: Dev Server Starts Fast

```bash
make serve

# Expected:
# ✓ Django server starts in < 5 seconds
# ✓ Accessible at http://localhost:8000
# ✓ Edit a Python file → hot-reload in < 2 seconds
```

### Scenario 3: Tests Pass

```bash
make test

# Expected:
# ✓ All tests pass (same count as Docker-based workflow)
# ✓ No test differences compared to running inside Docker
```

### Scenario 4: Lint Passes

```bash
make lint

# Expected:
# ✓ ruff reports no errors
```

### Scenario 5: Database Lifecycle

```bash
make db-stop
make db-up

# Expected:
# ✓ PostgreSQL stops cleanly
# ✓ PostgreSQL restarts without errors
# ✓ Data persists across restarts
```

### Scenario 6: Pre-Deployment Docker Stack Still Works

```bash
make docker-build
make docker-up

# Expected:
# ✓ Web Docker image builds successfully
# ✓ Full stack starts (db + web containers)
# ✓ App accessible at http://localhost:8000
make docker-down
# ✓ Stack stops cleanly
```

### Scenario 7: Debugger Integration

```bash
# In VS Code or PyCharm:
# Set a breakpoint in a view function
# Start the dev server via make serve
# Make a request to trigger the breakpoint

# Expected:
# ✓ Breakpoint is hit
# ✓ Step-through debugging works
# ✓ Variable inspection works
```

### Scenario 8: Idempotent Setup

```bash
bash setup.sh  # Run a second time

# Expected:
# ✓ Existing .env is not overwritten
# ✓ No errors from duplicate operations
```

## Data Model

No data model changes — see [data-model.md](data-model.md) for details.

## Contracts

No interface contract changes — see [contracts/](contracts/) for details.
