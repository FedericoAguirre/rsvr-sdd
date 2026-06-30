# Session: Duplicated Reservation Alert

## Feature
026-duplicated-reservation-alert — Alert when operator tries to reserve already-reserved equipment for same class slot and date.

## Workflow
/speckit.specify → /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.implement

## Spec (via ai/features/todos/12_Duplicated_reservation_alert.md)
3 user stories: US1-form validation/alert (P1), US2-Spanish i18n (P2), US3-accessibility (P3).

## Clarifications (5)
Q1-double trigger (add+submit), Q2-scope (create only), Q3-concurrency (DB check on submit), Q4-no logging, Q5-fail-open with warning.

## Changes
- forms.py: clean() with ValidationError (gettext_lazy), checks equipment+class_slot+date+status=reserved
- reservation_form.html: Bootstrap 5 alert-warning block, role="alert", aria-live="assertive"
- locale/es/LC_MESSAGES/django.po + .mo: Spanish translation "NO DISPONIBLE"
- test_reservations_form.py: 10 tests (unit+integration), all passing
