# Research: Change navigation bar menu order

No NEEDS CLARIFICATION markers existed in the spec — all technical context is well understood. This file confirms the findings used to fill the Technical Context section of the plan.

## Current Nav Structure

The navigation bar is defined in `backend/templates/base.html` (lines 17-40). Current left-to-right order:

1. Reservations (`reservations:reservation-list`)
2. Clients (`clients:client-search`)
3. Equipment (`equipment:equipment-list`) — conditional on `perms.equipment.view_equipment`
4. Schedule (`classes:class-schedule`) — conditional on `perms.classes.view_classslot`
5. Payments (`payments:list`)
6. Reports (dropdown, `payments:reports`) — conditional on `user.is_superuser`
7. Admin (`admin:index`)
8. Logout (POST form, `logout`)

## Target Order

Per spec, the reordered sequence:

1. Clientes (`clients:client-search`)
2. Pagos (`payments:list`)
3. Reservaciones (`reservations:reservation-list`)
4. Equipo (`equipment:equipment-list`)
5. Horario (`classes:class-schedule`)
6. Reportes (dropdown, `payments:reports`)
7. Admin (`admin:index`)
8. Cerrar Sesión (POST form, `logout`)

## Key Findings

- All labels already use `{% translate %}` — no i18n work needed (Constitution §III compliant)
- "Cerrar Sesión" already present in translation files (confirmed by existing `test_navbar_brand_and_nav_links_spanish` test)
- "Logout" is a `<form>` with `<button>` inside, not an `<a>` tag — must be moved as a complete `<li>` block
- Conditional items (Equipment, Schedule, Reports) must move with their `{% if %}` / `{% endif %}` wrappers intact
- Existing test `test_i18n.py::TestSpanishLabels::test_navbar_brand_and_nav_links_spanish` checks for presence of "Cerrar sesión" and "Reserva de Cardio" — will continue to pass after reorder

## Technology Context

- **Python**: 3.12+ (runtime 3.13)
- **Django**: configured via `config.settings`
- **Testing**: pytest with pytest-django
- **Template engine**: Django templates with `{% load i18n %}`
- **CSS framework**: Bootstrap 5.3 (`navbar-expand-lg`, responsive hamburger at `lg` breakpoint)
- **HTMX**: 2.0.4 (for dynamic interactions, though not relevant to nav)
- **Nav alignment**: `ms-auto` (right-aligned on desktop), responsive collapse via `navbar-toggler`
