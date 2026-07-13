# Quickstart: Export Payments

## Test the export

```bash
# Ensure Docker is running
make restart

# Run existing tests
docker compose exec web uv run pytest backend/tests/test_payments.py -k export -v

# Navigate to reports page
open http://localhost:8000/payments/reports/
```

## Usage

1. Go to **Reportes de Pagos** at `/payments/reports/`
2. Select **Fecha de inicio** and **Fecha de fin**
3. Click **Exportar** (next to **Generar reporte**)
4. Download `pagos_[start]_[end].xlsx`
