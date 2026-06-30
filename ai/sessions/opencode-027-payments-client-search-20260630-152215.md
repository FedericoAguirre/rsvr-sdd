# Session: Payments Client Search

## Feature
027-payments-client-search — Add client search field to payments list page that filters payments by client name, email, or mobile using HTMX.

## Workflow
/speckit.specify → /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.implement

## Spec (via ai/features/todos/11_Payments_client_search.md)
2 user stories: US1-search by client name/email/mobile (P1), US2-no results handling (P2).

## Clarifications (2)
Q1-search trigger: real-time debounce + explicit submit button. Q2-exclude soft-deleted (inactive) clients.

## Changes
- forms.py: PaymentSearchForm with q CharField
- views.py: PaymentListView.get_queryset() filters by q (icontains on name/email/mobile, 3-char min, inactive excluded); get_context_data() passes q/not_found; render_to_response() returns partial for HTMX
- payment_list.html: replaced client ID input with HTMX search form (hx-get, hx-trigger keyup delay:300ms, submit+clear buttons, indicator)
- partials/_payment_search_results.html: HTMX-swappable grid with pagination preserving ?q=, aria-live="polite"
- test_payments_search.py: 8 integration tests (name, email, mobile, 3-char min, case-insensitive, inactive exclusion, not-found, clear)
- locale/es/LC_MESSAGES/django.po + .mo: Spanish translations for search strings
