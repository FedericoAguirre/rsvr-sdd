# Quickstart: Validate ClassPrice Demarcation Fix

**Feature**: 062-fix-classprice-demarcation
**Date**: 2026-08-02

## Prerequisites

- Docker running (`docker compose up -d`)
- An admin user in the database (create via `docker compose exec web python manage.py createsuperuser` if needed)

## Validation Scenarios

### Scenario 1: First price — no archiving needed

```bash
# Ensure no prices exist (via admin or shell)
docker compose exec web python manage.py shell -c "
from apps.classes.models import ClassPrice
ClassPrice.objects.all().delete()  # if test data exists
"
```

1. Log in as admin at `/accounts/login/`
2. Navigate to `/classes/prices/add/`
3. Enter price `100.00`, click Save
4. Verify: Price history shows one row with green "Current" badge, Superseded shows "—"

**Expected**: One `current=True` record, no records with `changed_at` or `changed_by` populated.

### Scenario 2: Second price — previous is archived

1. Navigate to `/classes/prices/add/`
2. Enter price `150.00`, click Save
3. Verify: Price history shows $150 as "Current" (green badge), $100 as "Inactive" (gray badge)
4. Verify: $100 row shows a Superseded date and Changed by user (not "—")

**Expected**: Exactly one "Current" record ($150). The $100 record has `current=False`, non-null `changed_at` and `changed_by`.

### Scenario 3: Multiple legacy current prices archived at once

```bash
# Simulate pre-fix state: insert multiple current records directly
docker compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.classes.models import ClassPrice

User = get_user_model()
admin = User.objects.filter(is_superuser=True).first()

ClassPrice.objects.create(price=10, current=True, created_by=admin)
ClassPrice.objects.create(price=20, current=True, created_by=admin)
ClassPrice.objects.create(price=30, current=True, created_by=admin)
print('Created 3 legacy current prices')
"
```

1. Navigate to `/classes/prices/add/`
2. Enter price `50.00`, click Save
3. Verify: Only $50 shows "Current" badge; all three legacy prices show "Inactive" with Superseded date and Changed by user populated

**Expected**: All four previously-current records now have `current=False` with filled audit fields.

### Scenario 4: Transaction atomicity

```bash
docker compose exec web python manage.py shell -c "
from django.contrib.auth import get_user_model
from apps.classes.models import ClassPrice
from django.db import transaction

User = get_user_model()
admin = User.objects.filter(is_superuser=True).first()

# Verify enter_price works atomically
from django.utils import timezone

# Create initial price
ClassPrice.objects.create(price=75, current=True, created_by=admin)

# Enter new price via classmethod
result = ClassPrice.enter_price(100, admin)

# Verify exactly one current
current_count = ClassPrice.objects.filter(current=True).count()
print(f'Current count: {current_count}')  # Should be 1

# Verify the old one was archived
old = ClassPrice.objects.get(price=75)
print(f'Old price current: {old.current}')  # Should be False
print(f'Old price changed_at: {old.changed_at}')  # Should be non-null
print(f'Old price changed_by: {old.changed_by}')  # Should be admin
"
```

**Expected**: `current_count=1`, old price `current=False`, `changed_at` and `changed_by` populated.

## Running the Test Suite

```bash
docker compose exec web pytest backend/tests/test_classes_classprice.py -v
```

All existing tests must continue to pass. Tests covering `enter_price()` need updating to assert the new archiving behavior.
