# Quickstart: Payments Client Search

## Scope

Add a search field to the payments list page that filters payments by client name, email, or mobile number.

## Key Files

| File | Action |
|------|--------|
| `backend/apps/payments/forms.py` | Add `PaymentSearchForm` with a single `q` CharField |
| `backend/apps/payments/views.py` | Modify `PaymentListView.get_queryset()` to accept `q` param and filter via Client join |
| `backend/apps/payments/templates/payments/payment_list.html` | Replace client ID input with search input with HTMX attributes |
| `backend/apps/payments/templates/payments/partials/_payment_search_results.html` | New partial for HTMX-swappable grid content |
| `backend/tests/test_payments_search.py` | New tests |
| `backend/locale/es/LC_MESSAGES/django.po` | Add i18n strings |

## Implementation Steps

1. Write tests in `tests/test_payments_search.py`
2. Create `PaymentSearchForm` (single `q` field)
3. Modify `PaymentListView.get_queryset()` to filter by `q` when present:
   - Parse `q` from GET params
   - If `len(q) >= 3`: find active clients matching name/email/mobile, filter payments by those client IDs
   - If `len(q) < 3`: return unfiltered payments
4. Modify `PaymentListView.get_context_data()` to pass `q` to template
5. Modify `payment_list.html` to use HTMX search form
6. Create `_payment_search_results.html` partial
7. Add i18n strings to django.po
8. Compile translations (django.mo)

## HTMX Pattern

Follow the exact pattern from `clients/search.html`:
- Form with `hx-get`, `hx-trigger="keyup changed delay:300ms"`, `hx-target`, `hx-select`, `hx-swap`
- Also include submit button for explicit search
- Partial template renders only the grid content

## Test Plan

| Test | Type | What to Verify |
|------|------|----------------|
| Search by client name | Integration | Payments of matching clients appear |
| Search by email | Integration | Payments of matching client email |
| Search by mobile | Integration | Payments of matching client mobile |
| Minimum 3 characters | Integration | No search triggered with <3 chars |
| Case insensitive | Integration | Uppercase/lowercase match |
| No results | Integration | NOT FOUND message |
| Inactive clients excluded | Integration | Inactive client payments not shown |
| Grid format preserved | Integration | Same columns, pagination unchanged |
| Clear search | Integration | All payments shown when field cleared |
