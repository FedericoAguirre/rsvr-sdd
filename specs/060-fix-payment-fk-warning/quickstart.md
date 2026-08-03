# Quickstart: Fix PaymentReservation ForeignKey Warning

## Prerequisites

- Python 3.12+ with dependencies installed (`uv sync`)
- PostgreSQL database running (Docker: `docker compose up -d db`)
- Environment variables set (`DATABASE_URL`, `SECRET_KEY`, `DEBUG=True`)

## Validation Steps

### 1. Verify the warning is present (before fix)

```bash
cd backend
uv run python manage.py check 2>&1 | grep "fields.W342"
```

**Expected**: Output shows `payments.PaymentReservation.reservation: (fields.W342) ...`

### 2. Apply the model change

Change `backend/apps/payments/models.py` line 136-142 from:
```python
reservation = models.ForeignKey(
    "reservations.Reservation",
    on_delete=models.CASCADE,
    related_name="payment_links",
    unique=True,
    verbose_name=_("Reservation"),
)
```
to:
```python
reservation = models.OneToOneField(
    "reservations.Reservation",
    on_delete=models.CASCADE,
    related_name="payment_links",
    verbose_name=_("Reservation"),
)
```

### 3. Generate and apply migration

```bash
uv run python manage.py makemigrations payments
uv run python manage.py migrate payments
```

**Expected**: Migration applied successfully. Check output for "Applying payments.XXXX..."

### 4. Run system checks

```bash
uv run python manage.py check
```

**Expected**: `System check identified no issues (0 silenced).` — no `fields.W342` warning.

### 5. Run the test suite

```bash
uv run pytest
```

**Expected**: All existing tests pass.

### 6. Verify payment-reservation associations

```bash
uv run python manage.py shell -c "
from apps.payments.models import PaymentReservation
print(PaymentReservation.objects.count())
print('OK')
"
```

**Expected**: Prints the count of existing records and "OK" — no errors.

### 7. Docker validation (optional)

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
docker exec rsvr-sdd-web-1 uv run python manage.py check
```

**Expected**: Zero warnings from the web container.
