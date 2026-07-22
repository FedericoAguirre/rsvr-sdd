# Implementation Plan: Associated Reservations Calendar Download

**Branch**: `049-associated-reservations-calendar` | **Date**: 2026-07-21 | **Spec**: `specs/049-associated-reservations-calendar/spec.md`

**Input**: Feature specification from `specs/049-associated-reservations-calendar/spec.md`

## Summary

Add a "Descargar calendario" button to the payment detail page (`payments/{id}/`) that generates and downloads an ICS file containing calendar events for all reservations associated with that payment. Each event includes the client name, class slot, date, equipment, and payment identifier. The filename follows the format `<client_name>_<payment_identifier>_<first_date>_<last_date>.ics`.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Django 5.0.x, icalendar 7.x

**Storage**: PostgreSQL 16

**Testing**: pytest + pytest-django

**Target Platform**: Linux server (Docker)

**Project Type**: Web application (Django templates + Bootstrap 5.3 + HTMX 2.x)

**Performance Goals**: ICS generation completes within 3 seconds for up to 20 reservations (SC-004); page load with the button has no noticeable overhead

**Constraints**: Reuse the existing `_generate_ics()` utility from the clients app (021 feature); filename must be ASCII-safe; ICS must be compatible with major calendar apps

**Scale/Scope**: Small business (single gym); <50 concurrent operators; max 20 reservations per payment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I (Code Quality)
- No complexity concerns — this is a straightforward view + template button reusing existing ICS utility code
- YAGNI: No new models, no new forms needed

### Principle II (Testing Standards)
- Integration test REQUIRED: new view (`PaymentCalendarView` or function) involves HTTP request/response cycle and ICS generation
- TDD: Write tests first before implementing the view

### Principle III (UX Consistency / i18n)
- Button label "Descargar calendario" MUST be i18n-registered
- All user-visible messages (empty state, errors) MUST use i18n
- Existing i18n patterns from 021 client calendar download apply here

### Principle V (External Documentation)
- `icalendar` 7.x usage MUST be verified via Context7 MCP before writing code
- Django 5.0 file response patterns MUST be verified

**Status**: GATE PASSED — no unjustified complexity violations.

## Project Structure

### Documentation (this feature)

```text
specs/049-associated-reservations-calendar/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── apps/
│   └── payments/
│       ├── views.py              # New: PaymentCalendarView or calendar endpoint
│       ├── urls.py               # New: calendar download URL pattern
│       └── templates/payments/
│           └── payment_detail.html  # Add "Descargar calendario" button
├── clients/
│   └── views.py                  # Reuse _generate_ics() (or extract to shared util)
└── tests/
    └── test_payments_calendar.py # New: test file for calendar download
```

**Structure Decision**: Django web app with apps under `backend/apps/`. New view and URL in the payments app. Reuse existing `_generate_ics()` from `apps/clients/views.py`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations to justify.

