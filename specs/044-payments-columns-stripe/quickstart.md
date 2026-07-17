# Quickstart: Payments Columns Stripe

## What this feature does

Reorders columns in the "Reservas asociadas" table on `payments/{id}/` and adds striped rows.

**New column order**: Bloque de clase → Fecha → Equipo → Estado

## Files to modify

| File | Change |
|------|--------|
| `backend/apps/payments/templates/payments/payment_detail.html` | Reorder `<th>` and `<td>` elements, add `table-striped` class |

## Files to create

| File | Purpose |
|------|---------|
| `backend/tests/test_payments_detail.py` | TDD tests for column order |

## Commands

```bash
# Run tests
docker compose exec web uv run pytest backend/tests/test_payments_detail.py -v

# Run full suite
docker compose exec web uv run pytest
```

## Dependencies

None. All i18n strings and Bootstrap classes are already available in the project.
