# Implementation Plan: Duplicated Reservation Alert

**Branch**: `026-duplicated-reservation-alert` | **Date**: 2026-06-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/026-duplicated-reservation-alert/spec.md`

## Summary

Add a visible alert message on the `reservations/create/` page when an operator attempts to reserve equipment that is already reserved (status RESERVED) for the same class slot and date. The alert must display the date, class slot, and equipment marked as UNAVAILABLE, support i18n (Spanish), and follow accessibility best practices.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: Django 5.0, psycopg2-binary, whitenoise, weasyprint, icalendar

**Storage**: PostgreSQL

**Testing**: pytest with Django test client

**Target Platform**: Linux web server (Django/WSGI)

**Project Type**: Web application (Django)

**Performance Goals**: Alert visible within 1 second of triggering action

**Constraints**: i18n required for all user-visible strings (constitution mandate), Django form/view patterns, PostgreSQL backend

**Scale/Scope**: Single page enhancement — reservations/create/ only

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Code Quality**: No violations anticipated. No dead code, no TODOs.
- **II. Testing Standards (NON-NEGOTIABLE)**: TDD required. Integration tests for form validation + alert behavior. Separate unit tests for detection logic. Tests MUST fail before implementation.
- **III. UX Consistency / i18n (NON-NEGOTIABLE)**: All alert strings must be internationalized. 3-step contract applies: no hardcoded strings, keys registered in translation file, Spanish output verified.
- **IV. Performance**: SC-001 defines <1s alert visibility target. Structured logging not required for this feature per FR-011 (no logging).
- **Complexity**: Low. Simple alert layer over existing duplicate detection. No justification needed.

**Gate status**: ✅ PASS — all constitutional requirements satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/026-duplicated-reservation-alert/
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
│   ├── reservations/
│   │   ├── forms.py          # Add duplicate validation logic
│   │   ├── views.py          # Pass alert context to template
│   │   ├── templates/
│   │   │   └── reservations/
│   │   │       └── create.html  # Add alert display area
│   │   └── tests/
│   │       ├── test_forms.py    # Duplicate detection tests
│   │       └── test_views.py    # Alert rendering tests
│   └── equipment/
│       └── models.py         # Existing equipment model (no changes expected)
├── locale/                   # i18n translation files
│   ├── en/
│   └── es/
```

**Structure Decision**: Web application (Django) — single backend with app-based layout. Changes isolated to `reservations` app.

## Complexity Tracking

> No complexity violations. Feature is low complexity (alert overlay over existing logic).

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | — | — |
