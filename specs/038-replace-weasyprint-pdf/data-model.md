# Data Model: Reservation PDF Output

## PDF Document Structure

The ReportLab-generated PDF follows this layout:

```
┌──────────────────────────────────────────┐
│      Reservations by Class               │  ← h2, centered
├──────────────────────────────────────────┤
│ Date: 2026/07/12 — Class: Morning Yoga   │  ← header line, centered
├──────────┬──────────────┬────────────────┤
│ Equipment│ Client       │ Status         │  ← table header (bold, grey bg)
├──────────┼──────────────┼────────────────┤
│ Cinta #1 │ Juan Pérez   │ Confirmado     │  ← data rows
│ Bici #3  │ María García │ Presente       │
│ ...      │ ...          │ ...            │
├──────────┴──────────────┴────────────────┤
│ No reservations found... (if empty)      │  ← empty state message
└──────────────────────────────────────────┘
```

## Fields

| Field | Source | Type | Notes |
|-------|--------|------|-------|
| Title | i18n `_("Reservations by Class")` | static string | Translated via Django gettext |
| Date label | i18n `_("Date")` | static string | Rendered as "Date: {date_display}" |
| Date value | `date_display` from view context | string | Format: `YYYY/MM/DD` |
| Class label | i18n `_("Class")` | static string | Rendered as "Class: {class_slot}" |
| Class value | `class_slot` from view context | string | Class slot name |
| Equipment header | i18n `_("Equipment")` | static string | Table column header |
| Client header | i18n `_("Client")` | static string | Table column header |
| Status header | i18n `_("Status")` | static string | Table column header |
| Equipment name | `r.equipment.name` | string | From Reservation model |
| Client full name | `r.client|full_name` | string | From Reservation model |
| Status display | `r.get_status_display()` | string | Localized status text |
| Empty message | i18n `_("No reservations found for this class and date.")` | static string | Shown when no reservations exist |

## Validation Rules

- All user-visible strings MUST use Django i18n `gettext()` (constitution requirement)
- Non-ASCII characters (ñ, accented characters) MUST render correctly using ReportLab built-in fonts
- PDF filename format preserved: `reservations_{sanitized_slot_name}_{compact_date}.pdf`
