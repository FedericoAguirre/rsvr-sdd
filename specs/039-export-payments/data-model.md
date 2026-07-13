# Data Model: Export Payments

## Entities

No new database entities are required. The feature exports existing `Payment` records.

### Payment (existing — no changes)

| Field | Type | Export Column |
|-------|------|---------------|
| `id` | AutoField (PK) | Identificador |
| `client.display_name` (or similar) | FK → Client (via `client`) | Cliente |
| `amount` | DecimalField | Monto |
| `payment_type` | CharField (choices) | Tipo |
| `date` | DateField | Fecha |
| `class_slot_count` | PositiveSmallIntegerField | Clases (mapped from class_slot_count — the "Clases" column represents the number of class slots covered by this payment) |

**Filter**: `Payment.objects.filter(is_deleted=False, date__gte=start_date, date__lte=end_date)`

**Order**: By date ascending (same as reports view)

### Export Data Flow

```
PaymentReportView date filter
        │
        ▼
Payment.objects.filter(is_deleted=False, date__range=[start, end])
        │
        ▼
PaymentExportView (new)
        │
        ▼
openpyxl Workbook (write-only mode, streaming)
        │
        ▼
HttpResponse (Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
        │
        ▼
Download: pagos_YYYYMMDD_YYYYMMDD.xlsx
```

## Validation Rules

| Rule | Source | Behavior |
|------|--------|----------|
| Start date must be before end date | Clarification Q1 | Show validation error, prevent export |
| No payments in range | FR-006 | Show alert, no file generated |
| Generation failure | Clarification Q3 | Show error with retry, log server-side |
