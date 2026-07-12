# Contracts: Reservation PDF Export

## HTTP Contract (unchanged)

**Endpoint**: `GET /reservations/list/pdf/?class_slot=<id>&date=<YYYY-MM-DD>`

**Response**:
- Success: `200 OK` with `Content-Type: application/pdf`
- Error: Redirect to reservations list with error message

**Filename format**: `reservations_{sanitized_slot_name}_{compact_date}.pdf`

## PDF Content Contract

The generated PDF MUST include:
- Title: "Reservations by Class" (translated via i18n)
- Header: Date and Class name
- Table with columns: Equipment, Client, Status
- Each row: equipment name, client full name, status display
- Empty state: Header + "No reservations found for this class and date." message

## Dependency Change

| Change | Package | Rationale |
|--------|---------|-----------|
| Remove | `weasyprint>=62.0` | Requires system libraries |
| Add | `reportlab>=4.0` | Pure Python, cross-platform |

## Dockerfile Change

Remove from `backend/Dockerfile`:
```
libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf-2.0-0
```
