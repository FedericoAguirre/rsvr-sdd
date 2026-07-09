# Data Model: Add Payment Button to Client Page

## Summary

This feature does not introduce any new entities, fields, or database changes. It only adds a button to an existing template and modifies an existing view to support client preselection.

## Existing Entities Referenced

### Client

- **Source**: `backend/apps/clients/models.py`
- **Role in this feature**: The client whose detail page contains the **New Payment** button; its `pk` is passed as a query parameter to pre-select on the payment creation form
- **Key fields used**: `pk`

### Payment

- **Source**: `backend/apps/payments/models.py`
- **Role in this feature**: The payment entity created via `payments/create/`; the `client` ForeignKey field is pre-populated from the query parameter

## View Changes

### PaymentCreateView (backend/apps/payments/views.py)

- **Method added**: `get_initial()` — reads `self.request.GET.get("client")` and returns `{"client": client_id}` as initial data for the form
- **Existing behavior preserved**: `get_context_data()` still passes `client_id` to template context (unchanged)
- **Direct access preserved**: No `?client=` parameter → `get_initial()` returns empty dict → client field empty

## No Schema Changes

No migrations required. The feature operates entirely within existing database structures.
