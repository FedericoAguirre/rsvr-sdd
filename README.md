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

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- `uv` (optional — only for local development outside Docker)

## Setup

```bash
# 1. Clone the repository
git clone <repo-url> && cd rsvr-sdd

# 2. Copy environment variables
cp .env.example .env
# Edit .env with your own values (at minimum, set a strong SECRET_KEY)

# 3. Start services
docker-compose up -d

# 4. Run database migrations
docker-compose exec web python manage.py migrate

# 5. Seed demo data (class slots, equipment, sample clients)
docker-compose exec web python manage.py seed_data

# 6. Create an admin/operator account
docker-compose exec web python manage.py createsuperuser

# 7. Open in your browser
open http://localhost:8000
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

No tests have been written yet. When available, run:

```bash
docker-compose exec web python -m pytest
```

## Linting

```bash
docker-compose exec web ruff check .
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
