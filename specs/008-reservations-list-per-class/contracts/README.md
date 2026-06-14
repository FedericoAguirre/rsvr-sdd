# Contracts: Create Reservations List per Class Slot

**No external interfaces.** This feature is purely internal:

- New view `reservation_list_by_slot` at `/reservations/list/?class_slot=<id>&date=<YYYY-MM-DD>` — server-rendered HTML
- New PDF export view at `/reservations/list/pdf/?class_slot=<id>&date=<YYYY-MM-DD>` — returns PDF via WeasyPrint
- Both views require authentication (`@login_required`)
- No REST API endpoints, no third-party service integrations

All existing endpoints (`/reservations/`, `/reservations/create/`, etc.) continue to work unchanged.
