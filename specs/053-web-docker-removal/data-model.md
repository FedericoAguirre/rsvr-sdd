# Data Model: Remove Docker for Web Development

**Status**: No changes to application data model.

This feature does not introduce, modify, or remove any database entities, fields, relationships, or constraints. The PostgreSQL schema (tables for reservations, clients, payments, equipment, classes, etc.) is completely unaffected.

The only change is the **connection method**: the Django application connects to the same PostgreSQL database at `localhost:5432` instead of through a Docker network. The database schema, data, and migrations remain identical regardless of how the application is started.

## Verification

- Run `python manage.py showmigrations` locally — should show the same migration state as when running inside Docker.
- Run `python manage.py inspectdb` — should produce the same output.
