# Data Model: Remove Reservations Dead Code

## Entity: Reservation

| Attribute | Type | Constraints | Notes |
|-----------|------|-------------|-------|
| `updated_by` | ForeignKey(User) | nullable, SET_NULL, related_name=`updated_reservations` | **Added** in migration 0004 |

All other fields remain unchanged. See [spec.md](./spec.md) for the full entity description.

## Migration Plan

1. Create `0004_add_updated_by.py` via `manage.py makemigrations reservations`
2. Remove orphaned `0004_add_updated_by.cpython-*.pyc` from `__pycache__/`
3. Run `manage.py migrate` to apply
