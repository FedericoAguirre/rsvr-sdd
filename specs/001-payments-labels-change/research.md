# Research: Payments Labels Change

## Overview

This feature involves purely presentational changes to the payments listing page. No NEEDS CLARIFICATION markers exist in the spec. All decisions are derivable from the existing codebase.

## i18n Key Verification

### Existing keys in `clients/search` that will be reused

| English Key | Spanish Translation | Source File |
|-------------|-------------------|-------------|
| `"Search Clients"` | `"Buscar Clientes"` | `clients/templates/clients/search.html:3,5` |
| `"Search clients..."` | `"Buscar clientes..."` | `clients/forms.py:12` |
| `"Search"` | `"Buscar"` | `clients/templates/clients/search.html:14` (already used in payments) |

All three keys **exist** in `backend/locale/es/LC_MESSAGES/django.po` and are properly translated.

### Current keys in `payments/payment_list.html` to be replaced

| Current Key | Spanish | Replaced By |
|-------------|---------|-------------|
| `"Search by Client"` | `"Buscar por cliente"` | `"Search Clients"` |
| `"Search by client name, email or mobile..."` | `"Buscar por nombre, correo electrónico o móvil del cliente..."` | `"Search clients..."` |

### i18n cleanup after changes

- `"Search by Client"` (used only in `payment_list.html:23`) becomes unused — entry can be removed from `django.po`
- `"Search by client name, email or mobile..."` (used in `forms.py:18` AND `payment_list.html:24`) — the template usage is replaced, but the form definition still uses it. The entry stays because `forms.py` still references it.
- `"Search clients..."` (currently only used in `clients/forms.py:12`) will gain a new reference from `payment_list.html`

## Existing Test Coverage

- `backend/tests/test_payments_search.py` — tests search functionality
- `backend/tests/test_payments_create_button.py` — tests "New Payment" button behavior
- No tests currently verify specific CSS classes or label text on the list page
- Tests will need to be updated to verify the new labels and button classes

## Current Button Classes

| Button | Current Class | New Class |
|--------|--------------|-----------|
| Search/Filter submit | `btn btn-outline-secondary` | `btn btn-primary` |
| "New Payment" link | `btn btn-primary` | `btn btn-success` |

## No Data Model or Schema Changes

This feature does not touch models, views, URLs, or any Python logic. Changes are limited to:
1. `backend/apps/payments/templates/payments/payment_list.html`
2. `backend/locale/es/LC_MESSAGES/django.po`
3. `backend/locale/es/LC_MESSAGES/django.mo` (regenerated)
4. Test files (if existing tests need updating)
