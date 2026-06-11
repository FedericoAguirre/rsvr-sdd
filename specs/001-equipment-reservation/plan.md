# Implementation Plan: Cardio Equipment Reservation

**Branch**: `001-equipment-reservation` | **Date**: 2026-06-07 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-equipment-reservation/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command.

## Summary

A Django web application for gym staff to reserve cardio equipment for classes
(Mon-Fri, 17:30 and 18:30). Operators search clients by email/mobile, pick
available equipment, and create reservations. Administrators manage equipment
status and class schedules.

## Technical Context

**Language/Version**: Python 3.12+ (Django LTS compatible)

**Primary Dependencies**: Django, psycopg2 (PostgreSQL adapter), uv (package
manager), Bootstrap 5, Docker + Docker Compose

**Storage**: PostgreSQL (containerized)

**Testing**: pytest + pytest-django

**Target Platform**: Linux server (Docker container)

**Project Type**: Web application (Django + Bootstrap/HTML5)

**Performance Goals**: Page loads under 2 seconds; reservation confirmation
under 1 second; supports up to 5 concurrent operator/admin users

**Constraints**: All services containerized via Docker; PostgreSQL as sole
datastore; uv for Python dependency management; Bootstrap 5 + HTML5 for UI

**Scale/Scope**: Single gym location; ~10 weekly class slots; ~50 equipment
items; small operator/admin team (<10 users)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate Evaluation

| Principle | Assessment | Status |
|-----------|-----------|--------|
| I. Code Quality | Standard Django project with ruff linting, black formatting, pre-commit | ✅ PASS |
| II. Testing Standards (NON-NEGOTIABLE) | TDD will be enforced; pytest for unit + integration tests | ✅ PASS |
| III. User Experience Consistency | Bootstrap 5 provides consistent UI; Django templates for server-rendered pages | ✅ PASS |
| IV. Performance Requirements | Performance criteria defined in Technical Context | ✅ PASS |

**Result**: All gates pass. No Complexity Tracking entries required.

## Project Structure

### Documentation (this feature)

```text
specs/001-equipment-reservation/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── clients/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   └── templates/
│   ├── equipment/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   └── templates/
│   ├── classes/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   └── templates/
│   └── reservations/
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── forms.py
│       ├── admin.py
│       └── templates/
├── templates/
│   ├── base.html
│   └── components/
├── static/
│   ├── css/
│   └── js/
├── Dockerfile
├── requirements.txt
├── manage.py
└── pyproject.toml

tests/
├── clients/
├── equipment/
├── classes/
├── reservations/
└── conftest.py

docker-compose.yml

db/
└── init/
    └── schema.sql
```

**Structure Decision**: Standard Django project layout with feature-based apps
(clients, equipment, classes, reservations) under `backend/`. Django Admin used
for administrator equipment/class management. Custom views for operator
reservation workflow. Docker Compose links web and db services.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations — standard Django patterns throughout.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |
