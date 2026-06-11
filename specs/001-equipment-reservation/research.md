# Research: Cardio Equipment Reservation

## Technology Decisions

### Django + PostgreSQL + Docker

- **Decision**: Django 5.x with PostgreSQL 16, containerized via Docker Compose
- **Rationale**: Django provides built-in admin interface, ORM, form handling,
  and authentication — ideal for a data-centric reservation system with two
  user roles (operator, admin). PostgreSQL offers robust relational features
  needed for reservation integrity (unique constraints, transactions).
- **Alternatives considered**: Flask (would require more boilerplate for admin
  and auth); FastAPI (not ideal for server-rendered HTML); SQLite (lacks
  concurrent write support needed for reservation integrity)

### Frontend: Bootstrap 5 + HTML5 + Django Templates

- **Decision**: Server-rendered Django templates with Bootstrap 5
- **Rationale**: Matches the project type (internal business tool with small
  user base). No SPA complexity needed. Bootstrap provides consistent UI
  components out of the box. Django template inheritance reduces duplication.
- **Alternatives considered**: React/Vue (overkill for this scope); Tailwind
  (more setup overhead); plain CSS (inconsistent without framework)

### Package Management: uv

- **Decision**: Use `uv` (uv.pypi.org) for Python dependency management
- **Rationale**: Significantly faster than pip/poetry; native pyproject.toml
  support; lockfile generation for reproducible Docker builds.
- **Alternatives considered**: pip + venv (slower, no lockfile); Poetry
  (heavier, slower resolver); Pipenv (maintenance concerns)

### Testing: pytest + pytest-django

- **Decision**: pytest with pytest-django plugin
- **Rationale**: Industry standard for Django testing. Fixture system matches
  reservation domain well. Django's TestCase integration via plugin.
- **Alternatives considered**: Django's built-in unittest (less flexible);
  behave (BDD overhead not justified for internal tool)

### Containerization

- **Decision**: Docker Compose with `web` (Django + Gunicorn) and `db`
  (PostgreSQL) services
- **Rationale**: Matches user requirement. Docker Compose provides easy
  local development and consistent deployment. Gunicorn as production WSGI.
- **Alternatives considered**: Single-container (mixes concerns); Kubernetes
  (overkill); Podman (less community tooling)

## Domain Research

### Reservation System Patterns

- Equipment-per-class-slot model: each equipment item maps to one client per
  class time slot. Uniqueness enforced at database level via composite unique
  constraint on (equipment, class_slot, date).
- Status-based availability: equipment has an `is_active` boolean (or
  `status` enum). Only active equipment is shown in reservation picker.
- Client lookup: search by email OR mobile number with partial matching.

### Class Schedule Modeling

- Fixed weekly schedule: 10 slots (Mon-Fri × 17:30, 18:30).
- Schedule can be modeled as a lookup table or generated dynamically.
- Django choices or a database table — database table is more flexible for
  admin management (US3).
