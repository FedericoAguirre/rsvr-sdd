# OpenCode Session

**Model**: deepseek-v4-flash-free (opencode/deepseek-v4-flash-free)
**Date**: 2026-06-24
**Branch**: 022-payments-module

## Project
rsvr-sdd — Equipment reservation system (Django + Docker/Compose)

## Session Summary

### Completed Work
- Fixed HTMX CSRF: added `htmx:configRequest` JS in `base.html` to read `csrftoken` cookie and set `X-CSRFToken` header — standard Django+HTMX pattern
- Fixed `django.template.context_processors.csrf` missing from `TEMPLATES.OPTIONS.context_processors`
- Added `status_badge_class` and `status_label` template filters in `reservation_extras.py`
- Created `reservation_row.html` partial for HTMX row swap
- Added status badge rendering + inline "Used"/"Unused" action buttons to reservation list templates
- Modified `reservation_change_status` view to return HTMX partial + `HX-Trigger`
- Added JSON body fallback for `hx-vals` sent as `application/json`
- Wrote 11 tests, all 102 passing
- Applied Ruff linting
- Translated all payments user-facing strings to Spanish, ran `compilemessages`
- Amount format: used `f"${float(value):,.2f}"` in custom `currency` filter (bypasses Django locale interference)
- Default date: `date.initial = date.today()` and `DateInput(format="%Y-%m-%d")` for browser compatibility
- Right-aligned Monto and Clases columns (`text-end`)
- Renamed "Bloques" header to "Clases"
- Changed form layout from `col-md-6` (2-column) to `col-12` (stacked, label above input)

### Key Decisions
- Chart.js 4 CDN directly (no django-chartjs wrapper)
- Custom `currency` filter overcomes Django `floatformat` + `intcomma` locale interference
- All HTMX CSRF in one place (JS in `base.html`) — no per-button `hx-headers`/`hx-include`
- JSON body fallback in view as defensive measure

### Open Issues
None
