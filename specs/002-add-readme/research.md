# Research: Project README

**Feature**: Project README (`002-add-readme`)

**Date**: 2026-06-11

## Overview

Research to inform the content of the project-level README.md. No technical unknowns existed — the project was explored to gather accurate details.

## Findings

### Project Identity

- **Name**: rsvr-sdd (Reservas SDD — cardio equipment reservation system)
- **Purpose**: Django web application for gym staff to reserve cardio equipment for fitness classes
- **Domain**: Gym/health-club operations; 10 weekly class slots (Mon–Fri, 17:30 & 18:30)

### Technology Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.12+ | Project dependency |
| Framework | Django 5.0.x | Mature, batteries-included web framework |
| Database | PostgreSQL 16 | Containerized; robust relational DB |
| Frontend | Server-rendered templates + Bootstrap 5.3.3 | Simple, no JS framework needed |
| WSGI Server | Gunicorn | Production-grade WSGI server |
| Static Files | WhiteNoise | Serves static assets without a reverse proxy |
| Package Manager | `uv` | Fast Python package manager |
| Containerization | Docker + Docker Compose | Consistent dev/prod environment |
| Linter/Formatter | Ruff | Fast, single-binary Python linter |
| Testing (planned) | pytest + pytest-django | Configured in pyproject.toml but no tests written yet |

### Setup Approach

- Development environment uses Docker Compose (web + db services)
- Database initialized via `docker compose up -d`, then migrations and seed data
- Environment variables configured via `.env` file (template at `.env.example`)
- All management commands run through `docker compose exec web`

### Existing Documentation

- **Specs**: `specs/001-equipment-reservation/` contains full spec, plan, data model, quickstart, contracts, tasks
- **Quickstart**: Detailed setup guide exists at `specs/001-equipment-reservation/quickstart.md`
- **Security**: `mitigation_plan.md` documents 10 security findings (critical: hardcoded credentials, DEBUG default)
- **Agent context**: `AGENTS.md` points to plan for AI tooling

### Key Architectural Decisions

1. **Django apps** organized by domain: `clients`, `equipment`, `classes`, `reservations`
2. **Reservation uniqueness** enforced at DB level: unique constraint on (equipment, class_slot, date)
3. **Authentication**: Django built-in auth; all views require login
4. **No REST API** — pure server-rendered views
5. **No tests written yet** — pytest configured but test files not created

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| README contents | Full project README | Cover all spec FR-001 through FR-010 |
| Setup instructions | Docker Compose-based | Primary dev workflow for this project |
| Format | Standard GitHub Markdown | Universal rendering on GitHub |
| Tech stack display | Table format | Clear, scannable |
| Contribution section | Basic guidelines | Refer to existing spec workflow |

## Alternatives Considered

- **Minimal README** (just name + description): Rejected — does not meet spec requirements for setup, usage, or contribution guidance.
- **Separate CONTRIBUTING.md**: Deferred — spec only requires a section in README (FR-008: SHOULD include, not MUST).
