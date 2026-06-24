# Phase 0 Research: Payments Module

## Clarifications Resolved

### Evidence Image Storage Backend

- **Decision**: Use Django's default FileSystemStorage in development. For production, use django-storages with S3-compatible storage (MinIO for self-hosted or AWS S3).
- **Rationale**: The project already uses Docker volumes for persistent data. Adding django-storages is the standard Django pattern with zero migration cost. MinIO aligns with the existing Docker Compose setup.
- **Alternatives considered**: Local persistent volume only (fragile in multi-server), direct S3 without abstraction (tight coupling).

### Chart.js Integration Approach

- **Decision**: Use Chart.js CDN directly in the report template (no django-chartjs wrapper). Pass data as JSON embedded in the template context.
- **Rationale**: django-chartjs is not actively maintained and adds unnecessary abstraction. Chart.js 4.x has a clean JS API. Django's `json_script` template tag provides safe JSON serialization. The feature only needs 1-2 chart types (bar for daily/weekly/monthly totals, pie for payment type distribution) — no complex charting needed.
- **Alternatives considered**: django-chartjs (maintenance risk), Plotly (overkill for simple charts), Google Charts (external dependency).

## Technology Choices

### Payment Identifier Generation

- **Approach**: Python-side generation in the model's save method or via a service function. Use Django's `Q` expressions to count today's payments by payment type to get the consecutive number.
- **Format**: 2-3 letter type acronym + YYYYMMDD + client initials (uppercase, first + last initial) + 3-digit consecutive (zero-padded).
- **Edge cases**: Client with single initial → use first two letters of first name. Payments on same day with no prior → start at 001.

### Payment Evidence Upload

- **Approach**: Django `ImageField` with custom upload path `payments/evidence/{client_id}/{payment_id}/`.
- **Validation**: Validate file type (JPEG, PNG), max size 5MB, at the form level. Use Django's `FileExtensionValidator` and custom size validation.
- **Cleanup**: Handle file deletion on payment soft-delete (keep file, only remove reference, or keep as-is since audit trail requires preservation).

### Role-Based Access

- **Approach**: Django's built-in `django.contrib.auth` with Groups: "Operators" and "Administrators". All logged-in users are operators by default. Administrators are assigned to the "Administrators" group which grants report access.
- **Permission enforcement**: Decorators `@user_passes_test` or `@permission_required` on report views. Template-level `{% if perms %}` checks for UI visibility.

### Soft-Delete Implementation

- **Approach**: Add `is_deleted = BooleanField(default=False)` and `deleted_at = DateTimeField(null=True)` to the Payment model. Default model manager filters out deleted records. Admin and reports can include an optional "include deleted" toggle.
- **Audit trail**: Track edit/delete via `updated_by` and `deleted_at` fields. Use Django's `model_utils` or a simple custom mixin to track field changes.

## Integration Patterns

### Payment-Reservation Association

- **Flow**: Payment exists → On New Reservations page, after selecting client, show a list of that client's unpaid reservations → Operator selects N reservations (N ≤ payment.class_slot_count) → System creates PaymentReservation junction records.
- **Data model**: Create a `PaymentReservation` junction model with FKs to both Payment and Reservation, and a `created_at` timestamp for audit.
- **Validation**: At save time, count existing linked reservations + new count ≤ class_slot_count. Prevent double-linking a reservation to multiple payments unless the existing payment is soft-deleted.

### Existing Module Integration

- **Reservations app**: No modifications needed — the new junction model lives in the payments app. The reservation detail view can optionally show linked payment info.
- **Clients app**: Reuse Client model via FK. No modifications needed.
- **URL structure**: `/payments/` for list, `/payments/create/` for new, `/payments/{id}/` for detail, `/payments/{id}/edit/` for edit (reference/notes/evidence only), `/payments/{id}/delete/` for soft-delete, `/payments/reports/` for admin reports.

## Best Practices

### Django App Conventions (from existing codebase)

- Apps use `apps.py` with `verbose_name` in Spanish
- Models use `created_at`/`updated_at` auto-now fields
- Views use class-based views (CBVs) consistent with existing pattern
- Forms use Django ModelForm
- Templates extend `base.html` and use `{% load i18n %}`
- URL names use `app_name:name` pattern

### Testing Approach

- Unit tests for Payment model: identifier generation, validation, soft-delete
- Unit tests for PaymentForm: field validation, optional field handling
- Integration tests for Payment ↔ Reservation association (critical boundary)
- Integration tests for permission enforcement (operator vs admin)
- Use pytest fixtures matching existing test patterns (e.g., `client`, `class_slot`, `reservation` fixtures in `conftest.py`)
