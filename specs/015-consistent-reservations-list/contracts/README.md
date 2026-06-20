# Contracts: Consistent Reservations List

This project is a server-rendered Django web application with no external API or library interfaces. All interaction is through the web UI (HTML forms, HTMX requests). No interface contracts need to be defined for this feature.

The relevant URL endpoints (unchanged by this feature):
- `GET /reservations/` — main reservations page with filter form
- `GET /reservations/list/?class_slot=&date=&status=` — filtered list view
- `GET /reservations/list/pdf/?class_slot=&date=` — PDF export (out of scope)
