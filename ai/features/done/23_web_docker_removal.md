# 053 — Remove Docker for Web Development, Keep Database

**Status**: Ready for Implementation  
**Complexity**: 2  
**Priority**: Medium  
**Epic**: Developer Experience

---

## Objective

Improve local development speed by removing Docker containerization of the Django web application while keeping the PostgreSQL database in Docker. This hybrid approach maintains database reproducibility and isolation while leveraging local Python tooling, hot-reload, and faster I/O.

---

## Motivation

**Current State**: Both the Django web app and PostgreSQL database run in Docker containers via `docker-compose`.

**Problem**: Docker introduces performance overhead on local development:
- File system I/O overhead from volume mounts (especially on Mac/Windows)
- Hot-reload delays from container rebuild/sync cycles
- Memory/CPU overhead from container runtime
- Network latency between containers
- Friction integrating IDE debuggers and native Python tooling

**Desired State**: 
- Django app runs locally via `uv run manage.py runserver`
- PostgreSQL database remains in Docker for reproducibility and isolation
- Development workflow is faster with instant hot-reload
- All tooling (debuggers, linters, formatters) work natively

**Impact**: Developer velocity improves by reducing feedback loops in the edit→test→debug cycle.

---

## Scope

### Changes
1. Remove `web` service from `docker-compose.yml`
2. Update Makefile with local development targets
3. Add `.env` setup instructions for local development
4. Update README with local development workflow
5. Create `setup.sh` script to automate local environment bootstrap
6. Keep `docker-compose.yml` database-only for reproducible database setup

### Out of Scope
- Changes to Django application code
- CI/CD pipeline modifications (handled separately)
- Production deployment setup (still uses Docker)

---

## Current Setup

```yaml
services:
  db: postgresql:16
  web: Django app (Dockerfile in backend/)
```

**docker-compose.yml responsibilities**:
- `web` service: builds image, runs Django server
- `db` service: runs PostgreSQL

**Makefile targets**:
- `make up` — start both containers
- `make stop` — stop containers
- `make weblog` — tail web container logs
- `make build` — rebuild web image

---

## Desired Setup

```yaml
services:
  db: postgresql:16  # unchanged
```

**Local development**:
- Clone repo locally
- Install dependencies: `uv sync`
- Run database: `docker-compose up -d db`
- Run server: `uv run manage.py runserver`

**Makefile targets** (refactored for local dev):
- `make db-up` — start database only
- `make db-stop` — stop database
- `make db-logs` — view database logs
- `make serve` — start Django dev server locally
- `make migrate` — run migrations
- `make seed` — seed demo data
- `make test` — run pytest
- `make lint` — run ruff checks
- `make docker-build` — build web image for production testing
- `make docker-test` — spin up full stack in Docker for pre-deployment QA

---

## Implementation

### 1. Update `docker-compose.yml`

**Remove the `web` service entirely**. Keep database service and volume:

```yaml
services:
  db:
    image: postgres:16.14-alpine3.23
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-rsvr}
      POSTGRES_USER: ${POSTGRES_USER:-rsvr}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-rsvr}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-rsvr}"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### 2. Refactor `Makefile`

Replace container-focused targets with local development commands:

```makefile
SHELL := /bin/bash
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Database targets:"
	@echo "  db-up      Start PostgreSQL in Docker"
	@echo "  db-stop    Stop PostgreSQL"
	@echo "  db-logs    Tail database logs"
	@echo "  db-prune   Stop DB and prune Docker resources"
	@echo ""
	@echo "Local development targets:"
	@echo "  serve      Run Django dev server locally (http://localhost:8000)"
	@echo "  migrate    Run database migrations"
	@echo "  seed       Seed demo data (classes, equipment, clients)"
	@echo "  createsuperuser  Create admin account"
	@echo "  test       Run pytest suite"
	@echo "  lint       Run ruff linter on backend/"
	@echo "  format     Format code with ruff"
	@echo ""
	@echo "Pre-deployment testing:"
	@echo "  docker-build   Build web Docker image (for production testing)"
	@echo "  docker-up      Start full stack in Docker (DB + web container)"
	@echo "  docker-down    Stop full Docker stack"

.PHONY: db-up
db-up:
	docker-compose up -d db

.PHONY: db-stop
db-stop:
	docker-compose stop db

.PHONY: db-logs
db-logs:
	docker compose logs -f db

.PHONY: db-prune
db-prune: db-stop
	docker container prune -f
	docker image prune -f
	docker volume prune -f

.PHONY: serve
serve:
	uv run manage.py runserver

.PHONY: migrate
migrate:
	uv run manage.py migrate

.PHONY: seed
seed:
	uv run manage.py seed_data

.PHONY: createsuperuser
createsuperuser:
	uv run manage.py createsuperuser

.PHONY: test
test:
	uv run pytest

.PHONY: lint
lint:
	ruff check .

.PHONY: format
format:
	ruff format .

# Pre-deployment: test in actual Docker container before pushing to production
.PHONY: docker-build
docker-build:
	docker build -f backend/Dockerfile -t rsvr-sdd:latest backend/

.PHONY: docker-up
docker-up:
	docker-compose -f docker-compose.prod.yml up -d

.PHONY: docker-down
docker-down:
	docker-compose -f docker-compose.prod.yml down

.PHONY: install
install:
	cd backend && uv sync
```

### 3. Create `setup.sh` Bootstrap Script

Create a new file `setup.sh` in repo root to automate first-time setup:

```bash
#!/bin/bash
set -e

echo "🚀 Setting up rsvr-sdd for local development..."
echo ""

# Check dependencies
echo "📋 Checking dependencies..."
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Install from https://github.com/astral-sh/uv"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Install from https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Install from https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ All dependencies found"
echo ""

# Setup environment
echo "📝 Setting up .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env (update with your SECRET_KEY and other values)"
else
    echo "✅ .env already exists"
fi
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
uv sync
cd ..
echo "✅ Dependencies installed"
echo ""

# Start database
echo "🐘 Starting PostgreSQL..."
docker-compose up -d db
echo "✅ PostgreSQL started (listening on localhost:5432)"
echo ""

# Wait for database
echo "⏳ Waiting for database to be ready..."
until docker-compose exec -T db pg_isready -U ${POSTGRES_USER:-rsvr} > /dev/null 2>&1; do
    sleep 1
done
echo "✅ Database is ready"
echo ""

# Migrations
echo "🔄 Running migrations..."
uv run manage.py migrate
echo "✅ Migrations complete"
echo ""

# Seed data
read -p "Seed demo data? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    uv run manage.py seed_data
    echo "✅ Demo data seeded"
fi
echo ""

# Create superuser
read -p "Create admin account? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    uv run manage.py createsuperuser
    echo "✅ Admin account created"
fi
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Review .env file with any custom settings"
echo "  2. Run: make serve"
echo "  3. Open http://localhost:8000 in your browser"
echo ""
echo "Useful commands:"
echo "  make db-up          Start database"
echo "  make db-stop        Stop database"
echo "  make serve          Start Django dev server"
echo "  make migrate        Run migrations"
echo "  make test           Run test suite"
echo "  make lint           Check code style"
```

Make it executable: `chmod +x setup.sh`

### 4. Update `.env` Configuration

Ensure `.env.example` includes proper local development settings:

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DATABASE_URL=postgres://rsvr:rsvr@localhost:5432/rsvr
POSTGRES_DB=rsvr
POSTGRES_USER=rsvr
POSTGRES_PASSWORD=rsvr
```

Note: Database now uses `localhost` instead of Docker service name `db`.

### 5. Update README.md — Local Development Setup

Replace the Docker-based setup instructions with:

```markdown
## Quick Start (Local Development)

### Prerequisites
- Python 3.12+ (managed by `uv`)
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Docker & Docker Compose (database only)

### Setup

```bash
# 1. Clone repository
git clone <repo-url> && cd rsvr-sdd

# 2. Run automated setup
bash setup.sh

# This will:
# - Check dependencies
# - Create .env from .env.example
# - Install Python dependencies with uv
# - Start PostgreSQL in Docker
# - Run migrations
# - Optionally seed demo data and create admin account
```

### Running the App

```bash
# Terminal 1: Start database (once)
make db-up

# Terminal 2: Start Django dev server
make serve

# Open http://localhost:8000
```

### Common Tasks

| Task | Command |
|------|---------|
| Start database | `make db-up` |
| Stop database | `make db-stop` |
| View database logs | `make db-logs` |
| Run migrations | `make migrate` |
| Seed demo data | `make seed` |
| Create admin user | `make createsuperuser` |
| Run tests | `make test` |
| Lint code | `make lint` |
| Format code | `make format` |

## Pre-Deployment Testing (Docker Full Stack)

Before deploying to production, test the full Docker stack:

```bash
# Build web image
make docker-build

# Start full stack (db + web in containers)
make docker-up

# Run against http://localhost:8000

# Stop stack
make docker-down
```
```

---

## Database Configuration

### Local Connection String
Change from Docker service name to localhost:

```
# Old (Docker): postgres://user:pass@db:5432/dbname
# New (Local):  postgres://user:pass@localhost:5432/dbname
```

Update in:
- `.env` — `DATABASE_URL` should use `localhost`
- `settings.py` — already uses `DATABASE_URL` env var ✓
- Makefile — local commands use `uv run` (auto-reads `.env`)

### Database Health Checks
Local development doesn't need container health checks. The `docker-compose.yml` health check remains for the container itself.

---

## Testing Strategy

### Local Development Testing
```bash
make test              # Unit/integration tests via pytest
make lint              # Code quality checks
```

### Pre-Deployment Docker Testing
```bash
make docker-build      # Build exact production image
make docker-up         # Spin up full stack
# Manual testing at http://localhost:8000
make docker-down       # Cleanup
```

---

## Migration Path

### Phase 1: Setup (Day 1)
1. Run `bash setup.sh` on local machine
2. Verify `make serve` starts app at `http://localhost:8000`
3. Test login and basic CRUD operations

### Phase 2: Verification (Day 1-2)
1. Run `make test` — all tests pass locally
2. Run `make docker-build && make docker-up` — verify full Docker stack works
3. Run `make lint` — code quality checks pass

### Phase 3: Cleanup (Optional)
1. Remove `web` service from `docker-compose.yml`
2. Delete old Docker web-related build files if applicable
3. Update team documentation and onboarding guides

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Local database state diverges from Docker | Always run `make db-stop && make db-up` to reset to clean state |
| Dev environment works but Docker fails | Use `make docker-build && make docker-up` before each commit to production branch |
| IDE/debugger conflicts | All tooling runs natively — no Docker friction |
| Team setup inconsistency | Use `setup.sh` script for reproducible bootstrap |

---

## Rollback Plan

If local development proves problematic, revert to full Docker:

1. Restore original `docker-compose.yml` (includes `web` service and Dockerfile)
2. Restore original `Makefile` with Docker targets
3. Run `docker-compose up -d` and `make weblog` to monitor

---

## Success Criteria

- ✅ `bash setup.sh` completes without errors on clean checkout
- ✅ `make serve` starts Django server locally in <5 seconds
- ✅ Hot-reload works (edit `.py` file → browser refresh shows change in <2 seconds)
- ✅ All tests pass: `make test` runs successfully
- ✅ Database isolation maintained: `make db-up/stop` cleanly manages PostgreSQL
- ✅ Pre-deployment Docker test passes: `make docker-build && make docker-up`
- ✅ IDE debugger works with local Python interpreter
- ✅ All commands in Makefile `help` are current and functional

---

## Deliverables

1. Updated `docker-compose.yml` (database only)
2. Refactored `Makefile` with local dev targets
3. New `setup.sh` bootstrap script
4. Updated `.env.example` with local DB connection string
5. Updated README.md with local development instructions
6. Optional: `docker-compose.prod.yml` for explicit production compose file

---

## Timeline

- **Implementation**: ~1 hour (file edits + testing)
- **Team rollout**: ~30 minutes (run setup.sh, verify)
- **Buffer for issues**: ~30 minutes

**Total**: ~2 hours

---

## References

- [uv Package Manager](https://github.com/astral-sh/uv)
- [Django Development Server](https://docs.djangoproject.com/en/5.0/ref/django-admin/#runserver)
- [Docker for Database Only](https://docs.docker.com/compose/intro/)
