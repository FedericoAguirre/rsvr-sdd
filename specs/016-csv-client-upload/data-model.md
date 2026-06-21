# Data Model: CSV Client Upload

No new database entities are required. The CSV upload operates on the existing `Client` model.

## Existing Model

### `Client`

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| `id` | BigAutoField | PK | Auto-generated |
| `first_name` | CharField(100) | NOT NULL | Required |
| `last_name` | CharField(100) | NOT NULL | Required |
| `email` | EmailField | UNIQUE, NULL, BLANK | Optional (but at least one of email/mobile required) |
| `mobile` | CharField(20) | UNIQUE, NULL, BLANK | Optional (but at least one of email/mobile required) |
| `is_active` | BooleanField | default=True | New records set to ACTIVE |
| `created_at` | DateTimeField | auto_now_add | Set on creation |
| `updated_at` | DateTimeField | auto_now | Updated on every save |

**Validation**: Model-level `clean()` ensures at least one of `email` or `mobile` is provided.

### CSV Processing State

The CSV upload is a **stateless process** (no persistent processing state). Results are computed in-memory and displayed to the Operator in the response. No new tables or models needed.

### Concurrency

Standard PostgreSQL row-level locking applies. If two Operators upload conflicting CSV data simultaneously:
- UNIQUE constraint violations on `email` or `mobile` will raise `IntegrityError`
- These are caught and reported as row-level errors in the summary

This is acceptable for the expected low concurrency of an internal gym management system.
