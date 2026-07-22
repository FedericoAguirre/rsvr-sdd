<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan at
`specs/050-calendar-downloading-reservations/plan.md`
<!-- SPECKIT END -->

<!-- CONTEXT7 START -->
## Context7 MCP — MANDATORY (Constitution Principle V)

Before writing any code that uses a library, package, or framework
dependency, you MUST:

1. Resolve the library ID via `context7_resolve-library-id`
2. Query current docs via `context7_query-docs` with the full question
3. Use version-specific IDs (e.g. `/django/django/5.0`) when targeting
   a specific version

This applies to ALL dependencies: Django 5.0, Bootstrap 5.3, HTMX 2.x,
Chart.js 4.x, ReportLab 5.x, pytest, gunicorn, psycopg2, Whitenoise,
openpyxl, icalendar, pdfminer-six, i18n, and any future additions.

See the `<!-- context7 -->` block in the system prompt for full usage
instructions.

**Rationale**: LLM training data may not reflect recent API changes,
deprecations, security patches, or version-specific behavior.
<!-- CONTEXT7 END -->

## Session Summary (2026-07-21)

This session is on branch **050-calendar-downloading-reservations** — see `specs/050-calendar-downloading-reservations/plan.md`.

### Completed
- Spec written and validated via Spec Kit workflow
- Plan generated with Technical Context, Constitution Check, and Structure
- Research artifacts (research.md, data-model.md, quickstart.md) generated
- ICS contract documented
- All quality checklist items pass
