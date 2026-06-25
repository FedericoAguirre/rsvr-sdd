# Data Model: Reports Menu Option

**Phase 1** — No new data entities introduced.

This feature is purely a navigation structure change. It reuses the following existing entities:

| Entity | How Used | Existing Source |
|--------|----------|-----------------|
| `User` (auth) | `user.is_superuser` gates Reports menu visibility | `django.contrib.auth.models.User` |
| `Payment` | Displayed on the target reports page (no changes) | `apps.payments.models.Payment` |

## Validation Rules

No new validation rules required.

## State Transitions

No state transitions introduced.
