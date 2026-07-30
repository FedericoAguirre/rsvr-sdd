# Research: Remove Docker for Web Development, Keep Database

## 1. DATABASE_URL Configuration (Settings Check)

**Decision**: No code changes needed in `backend/config/settings.py`.

**Rationale**: The existing `settings.py` already provides a local-development fallback:
```python
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://rsvr:rsvr@localhost:5432/rsvr")
```
When running locally without `DATABASE_URL` set, Django defaults to `localhost:5432`. The Docker Compose `web` service currently overrides this with `@db:5432` — removing the `web` service removes that override, and the fallback takes effect. Adding `DATABASE_URL=postgres://rsvr:rsvr@localhost:5432/rsvr` to `.env.example` provides an explicit local configuration.

**Alternatives considered**:
- Using `dj-database-url` library — unnecessary, existing manual parsing works fine.
- Using `django-environ` — would add dependency for no benefit.

## 2. Docker Compose Database-Only Pattern

**Decision**: Remove the `web` service entirely; keep `db` service unchanged.

**Rationale**: Docker Compose supports running a subset of services via `docker-compose up -d db`. The `db` service config (PostgreSQL 16 Alpine, health check, volume) is left intact. This is a well-established pattern documented in the Docker Compose ecosystem.

**Alternatives considered**:
- Keeping web service but adding a `profile` to disable it by default — unnecessary complexity, the service should be removed.
- Running PostgreSQL via `brew`/`apt` directly — adds platform-specific setup burden and loses reproducibility.

## 3. uv Package Manager — Local Development Setup

**Decision**: Use `uv sync` in `setup.sh` and `uv run` for all Makefile targets.

**Rationale**: The project already uses `uv` for dependency management (pyproject.toml + uv.lock present). Running `uv sync` installs the virtual environment; `uv run manage.py` runs Django commands without needing to activate the venv manually. This is the standard uv workflow.

**Key consideration**: `uv` must be available on the developer's machine. The `setup.sh` script will check for it and error with a clear message if missing.

## 4. Pre-Deployment Docker Testing

**Decision**: Keep `make docker-build` and `make docker-up` targets for full-stack Docker testing before production pushes.

**Rationale**: While local development runs natively, the production deployment uses Docker. The `docker-compose.prod.yml` (or equivalently, rebuilding with the Dockerfile for the web service) must still work. These targets provide a safety net before pushing to production.

## 5. Makefile Targets — Local Development Pattern

**Decision**: Follow GNU Make conventions with section headers, `.PHONY` declarations, and `--warn-undefined-variables`.

**Rationale**: The new Makefile will have three sections:
- **Database targets**: `db-up`, `db-stop`, `db-logs`, `db-prune`
- **Local development targets**: `serve`, `migrate`, `seed`, `createsuperuser`, `test`, `lint`, `format`
- **Pre-deployment targets**: `docker-build`, `docker-up`, `docker-down`, `install`

This follows standard Django project Makefile patterns seen in practice.

## 6. setup.sh Bootstrap Script

**Decision**: Create a single idempotent setup script at repository root.

**Rationale**: A single bash script that checks dependencies, sets up `.env`, installs packages, starts the database, runs migrations, and optionally seeds data. This is the standard approach for Django projects and eliminates the multi-step manual setup currently documented.

**Key considerations**:
- Must handle partial setup (idempotent)
- Must check for `uv`, `docker`, `docker-compose` before proceeding
- Must not overwrite existing `.env`
- Interactive prompts for seed data and superuser creation
- macOS and Linux only; Windows users use WSL/Git Bash

## 7. .env.example Updates

**Decision**: Add `DATABASE_URL`, reorder sections, provide sensible local defaults.

**Rationale**: The current `.env.example` lacks `DATABASE_URL` because it was only set in `docker-compose.yml`. For local development, it must be explicit. Also add `DEBUG=True` for local development convenience (default was `False`).

## 8. README Updates

**Decision**: Replace the Docker-based quickstart with local development instructions. Keep Docker full-stack instructions in a separate section.

**Rationale**: The primary onboarding path is now local development. The pre-deployment Docker testing is secondary but still documented.
