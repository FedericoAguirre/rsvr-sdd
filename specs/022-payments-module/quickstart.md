# Quickstart: Payments Module

## Prerequisites

- Running on branch `022-payments-module`
- Django project configured, migrations up-to-date
- Chart.js 4.x loaded via CDN in `base.html`

## Steps

1. **Create the payments app**:
   ```bash
   cd backend
   python manage.py startapp payments apps/payments
   ```

2. **Add to INSTALLED_APPS** in `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       "apps.payments",
   ]
   ```

3. **Add Chart.js to base.html**:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
   ```

4. **Create the Payment model** (see [data-model.md](data-model.md)):
   - Add fields per data model
   - Implement `save()` for payment identifier auto-generation
   - Add soft-delete support

5. **Create and run migrations**:
   ```bash
   python manage.py makemigrations payments
   python manage.py migrate
   ```

6. **Create views**:
   - `PaymentListView` (paginated, client filtering)
   - `PaymentCreateView` (with client select, from-reservation support)
   - `PaymentDetailView`
   - `PaymentUpdateView` (limited to reference/notes/evidence)
   - `PaymentDeleteView` (soft-delete)
   - `PaymentReportView` (admin only, Chart.js integration)

7. **Create templates** under `templates/payments/`:
   - Extend `base.html` with `{% extends "base.html" %}`
   - Use `{% load i18n %}` for Spanish translations

8. **Wire URLs** in `config/urls.py`:
   ```python
   path("payments/", include("apps.payments.urls")),
   ```

9. **Set up groups** for role-based access:
   - Create "Operators" and "Administrators" groups
   - Assign permissions to views accordingly

10. **Create tests** in `backend/tests/test_payments.py`:
    - Test payment creation with valid/invalid data
    - Test payment identifier auto-generation
    - Test soft-delete
    - Test Payment-Reservation association (integration)
    - Test permission enforcement (operator vs admin)
    - Test report aggregation

## Verification

```bash
cd backend
python manage.py check
pytest tests/test_payments.py -v
python manage.py runserver
# Navigate to /payments/ and /payments/reports/
```
