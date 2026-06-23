# Contracts: Quick Reservation Status Management

## HTMX View Contract

### Endpoint: `POST /reservations/<pk>/status/`

This is the **existing** `reservation-change-status` endpoint, modified to support HTMX responses.

#### Request

| Field | Type | Location | Required | Description |
|-------|------|----------|----------|-------------|
| `status` | string | POST body | Yes | One of: `"used"`, `"unused"`, `"reserved"` |
| `HX-Request` | header | HTTP header | Implicit | Set automatically by HTMX to `"true"` |

#### Response (HTMX path)

When `HX-Request` header is present:

| Condition | Status | Content-Type | Body |
|-----------|--------|-------------|------|
| Valid status change | 200 OK | `text/html` | Rendered `partials/reservation_row.html` with updated reservation |
| Invalid status value | 400 Bad Request | `text/html` | Rendered error partial or plain error message |
| Reservation not found | 404 Not Found | `text/html` | Error message |
| Unauthenticated | 302 Redirect | — | Redirect to login (standard Django behavior — HTMX follows redirect) |

The response **must** include the `HX-Trigger` header set to `"statusChanged"` so other parts of the UI can react if needed.

#### Response (non-HTMX path)

When `HX-Request` header is absent, behavior is **unchanged** — redirect to `reservations:reservation-detail`.

#### HTMX Swap Target

- **Target**: `#row-{{ reservation.pk }}` — each table row has a unique ID
- **Swap method**: `outerHTML` — replaces the entire row with the updated one
- **Trigger**: The action button's `hx-post` attribute

## Template Contracts

### Partial: `reservations/partials/reservation_row.html`

Renders a single `<tr id="row-{{ r.pk }}">` containing:
- Status badge (colored span using Bootstrap badge classes)
- All existing row data columns (date, client, class, equipment)
- Inline action buttons ("Mark as used", "Mark as unused")
- Error/success message area (optional)

**Context**: `reservation` — a single `Reservation` instance.

### Template Tag: `status_badge_class`

A custom template filter or simple tag that maps status values to Bootstrap CSS classes:

| Status | Class |
|--------|-------|
| `reserved` | `badge bg-success` |
| `used` | `badge bg-primary` |
| `unused` | `badge bg-secondary` |
