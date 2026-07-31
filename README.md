# rsvr-sdd — Cardio Equipment Reservation System

[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

Reservas SDD is a web application for gym staff to reserve cardio equipment for fitness classes. It supports class scheduling, equipment management, client lookup, and reservation tracking — all via a server-rendered Django interface.

## Features

- **Reservation management** — Create, view, and manage equipment reservations per class slot
- **Client lookup** — Search clients by email or mobile phone number
- **Equipment inventory** — Track equipment status (in-service / out-of-service)
- **Class schedule** — Manage weekly class slots with active/inactive toggle
- **Admin panel** — Full admin interface for advanced management
- **Unique booking enforcement** — Prevents double-booking the same equipment in the same class slot on the same date

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.12+ |
| Framework | Django 5.0.x |
| Database | PostgreSQL 16 |
| Frontend | Django Templates + Bootstrap 5.3.3 |
| WSGI Server | Gunicorn |
| Package Manager | `uv` |
| Containerization | Docker + Docker Compose |
| Linter/Formatter | Ruff |

## Prerequisites

- Python 3.12+ (managed by `uv`)
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) (database only)

> **Windows 11 Home deployment**: See [docs/windows11_deployment.md](docs/windows11_deployment.md) for a container-free setup guide.

## Quick Start (Local Development)

Run the automated setup script to bootstrap your environment:

```bash
bash setup.sh
```

This will:
- Check that `uv`, `docker`, and `docker-compose` are installed
- Create `.env` from `.env.example` (if not present)
- Install Python dependencies with `uv sync`
- Start PostgreSQL in Docker
- Run database migrations
- Optionally seed demo data and create an admin account

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

## Usage

### Reserving Equipment

1. Log in with your operator account
2. Navigate to **Reservations → Create**
3. Search for a client by email or mobile number
4. Select an in-service equipment item and a class slot
5. Submit to create the reservation

### Managing Equipment

1. Go to **Equipment** in the navigation bar
2. View all equipment items and their current status
3. Add, edit, or toggle equipment status as needed

### Managing Class Schedule

1. Go to **Classes** in the navigation bar
2. View the weekly schedule with all class slots
3. Toggle individual slots active/inactive

## Running Tests

```bash
# Run tests locally
make test

# Or run the full Docker stack for pre-deployment validation
make docker-build && make docker-up
```

## AI Development Data Export

A management command collects data from completed AI-assisted features and outputs a CSV for SDLC process analysis. Data is sourced from `ai/features/done/`, `specs/*/spec.md`, and `ai/sessions/`.

```bash
# Option A — Run directly with uv (no Docker required)
cd backend && uv run manage.py collect_ai_dev_data --output ../ai_dev_data.csv

# Option B — Run in Docker with repo root mounted (no DB needed)
docker run --rm -v "$(pwd):/repo" rsvr-sdd_web uv run /app/manage.py collect_ai_dev_data \
  --output /repo/ai_dev_data.csv \
  --done-dir /repo/ai/features/done \
  --specs-dir /repo/specs \
  --sessions-dir /repo/ai/sessions
```

The CSV includes: feature title, complexity (1/2/3/5/8), implementation minutes, AI model, timestamps, spec quality (1–5), and iteration count.

For full details, see [`specs/052-ai-dev-data-collection/`](specs/052-ai-dev-data-collection/).

## Linting

```bash
make lint
```

## AI Agent Skills

[autoskills.sh](https://www.autoskills.sh/) automatically detects your tech stack and installs curated AI agent skills for your project.

```bash
npx autoskills
```

This project uses Django, so running the above command will detect it and offer to install relevant Django skills:

| Skill | Description |
|-------|-------------|
| [django-expert](https://skills.sh/vintasoftware/django-ai-plugins/django-expert) | Expert-level Django development patterns |
| [django-patterns](https://skills.sh/affaan-m/everything-claude-code/django-patterns) | Common Django patterns and best practices |
| [django-security](https://skills.sh/affaan-m/everything-claude-code/django-security) | Django security best practices |

Additional skills for other technologies in the stack (Bootstrap, PostgreSQL, Docker) will also be offered. Use `--dry-run` to preview before installing:

```bash
npx autoskills --dry-run
```

## Project Structure

```text
backend/
├── config/           # Django project settings, URLs, WSGI
├── apps/
│   ├── clients/      # Client (gym member) management
│   ├── equipment/    # Equipment inventory management
│   ├── classes/      # Class schedule management
│   └── reservations/ # Reservation creation and listing
├── templates/        # Shared templates (base, login)
└── manage.py
```

## Contributing

1. Feature branches follow sequential numbering: `###-feature-name`
2. All work follows the **Specify → Plan → Tasks → Implement** cycle
3. Commits must be atomic and descriptive
4. Every PR must pass linting and include documentation updates
5. See `specs/` directory for existing feature specifications and plans

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
