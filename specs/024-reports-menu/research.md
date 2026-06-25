# Research: Reports Menu Option

**Phase 0** — Resolved unknowns and technical approach.

## Navigation Pattern

**Decision**: Use Bootstrap 5 `.dropdown` component within the existing navbar.

**Rationale**: The project already uses Bootstrap 5 (CDN in `base.html`). The navbar is built with Bootstrap classes. A dropdown is the standard Bootstrap pattern for hierarchical navigation.

**Alternatives considered**: Dropup (less discoverable), offcanvas sidebar (over-engineered for a single sub-item), flat link (spec requires dropdown per FR-003).

## Permission Check

**Decision**: Check `user.is_superuser` in the template to gate Reports menu visibility.

**Rationale**: The existing `PaymentReportView.test_func()` checks `is_superuser or Administrators group`. Django templates cannot query group membership without a custom template tag or context processor. Using `is_superuser` in the template is the simplest approach that covers the most common admin case. The view's own `UserPassesTestMixin` remains the authoritative gate — the template check is a UX convenience, not a security boundary.

**Alternatives considered**:
- Custom template filter to check group membership — adds unnecessary complexity for this simple feature
- Context processor injecting `is_administrator` — also over-engineered for a single menu item
- Using `perms.payments.view_payment` — both Operators and Administrators groups have this permission, so it would not distinguish admins

## i18n Approach

**Decision**: Use existing `{% translate %}` template tag pattern with Django's `django.po` file.

**Rationale**: This is the established pattern throughout the project. Spanish translations are required by the constitution (NON-NEGOTIABLE).

## Existing Reports Page

**Decision**: No changes to the `PaymentReportView` or `payment_reports.html` template.

**Rationale**: The page already exists and functions correctly at `/payments/reports/`. This feature only adds navigation access.

## Test Approach

**Decision**: Use Django `TestCase` with `assertContains` to verify the Reports menu appears for admin users and is absent for non-admin users.

**Rationale**: This matches existing test patterns in the project. The test will render `base.html` via the Django test client and check for the Reports and Payments link text in the response HTML.
