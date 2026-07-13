# Contract: Payment Export View

## Endpoint

- **URL**: `GET /payments/reports/export/`
- **Name**: `payments:export`
- **Access**: Superuser or "Administrators" group members only (same as `PaymentReportView`)
- **Method**: GET

## Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `fecha_inicio` | string (date, YYYY-MM-DD) | Yes | Start of date range |
| `fecha_fin` | string (date, YYYY-MM-DD) | Yes | End of date range |

## Responses

### 200 OK — successful export

- **Content-Type**: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- **Content-Disposition**: `attachment; filename="pagos_[YYYYMMDD]_[YYYYMMDD].xlsx"`
- **Body**: Binary .xlsx file stream

### 400 Bad Request — validation error

Conditions:
- Missing or invalid `fecha_inicio` or `fecha_fin`
- `fecha_inicio > fecha_fin`

```json
{
  "error": "La fecha de inicio debe ser anterior a la fecha de fin."
}
```

### 404 Not Found — no data

Condition: No payments match the date range.

```json
{
  "error": "No hay pagos en el rango de fechas seleccionado."
}
```

### 500 Internal Server Error — generation failure

Condition: Unexpected error during file generation (disk full, permissions, etc.)

```json
{
  "error": "Error al generar el archivo. Intente nuevamente."
}
```

## Frontend Integration

- **Button**: "Exportar" adjacent to "Generar reporte" in `payment_reports.html`
- **Behavior**: Pass current `fecha_inicio` and `fecha_fin` from the report form as query params
- **Loading state**: Disable button during download (FR-008)
- **Error display**: Show server error response as an alert
- **No-data display**: Show alert for 404 response, no file download
