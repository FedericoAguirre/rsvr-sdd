# Implementation Plan: Reorder Payment Form Fields for Improved UX

**Branch**: `054-payments-form-reorder` | **Date**: 2026-07-30 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/054-payments-form-reorder/spec.md`

## Summary

Reorder the field display order on the payment creation form (`/payments/create/`) to follow a logical workflow: client identification → transaction details → context/notes → documentation → submit.

## Technical Context

**Language/Version**: Python 3.12+ (Django 5.0.x)

**Primary Dependencies**: Django Forms (ModelForm), Bootstrap 5.3, HTMX 2.x

**Storage**: N/A — no database schema changes

**Testing**: pytest (existing test suite), manual visual verification

**Target Platform**: Web browser (Chrome, Firefox, Safari) on desktop and mobile

**Project Type**: Web application (Django)

**Performance Goals**: Page load and form submission times unchanged

**Constraints**: No changes to Payment model, validation logic, or payment processing. Field labels and help text must match existing i18n conventions.

**Scale/Scope**: Two files changed — `payments/forms.py` (field order in `Meta.fields`) and `templates/payments/create.html` (rendering order). View logic unchanged.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1 — Code Quality (Principle I)

**No violation**: The form template and form class changes are minimal — field reordering only. No dead code or commented code introduced.

### Gate 2 — Testing Standards (Principle II — NON-NEGOTIABLE)

**No violation**: Existing payment form tests must continue to pass. No new tests required — this is a cosmetic/layout change only.

### Gate 3 — Internationalization (Principle III — NON-NEGOTIABLE)

**No violation introduced by this feature**: The form fields already have Spanish labels in the existing template. This feature reorders existing fields and does not introduce any new user-visible strings. Labels, error messages, and help text remain unchanged. The existing i18n coverage (or lack thereof) is a pre-existing concern outside this feature's scope.

### Gate 4 — Performance (Principle IV)

**No violation**: Field order has zero performance impact on page rendering or form processing.

### Gate 5 — External Documentation (Principle V)

**No violation**: Django form field ordering and Bootstrap form layout are well-known patterns. If implementation requires specific API references, Context7 should be consulted.

**Result**: All gates pass. No violations require justification.

## Project Structure

### Documentation (this feature)

```text
specs/054-payments-form-reorder/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── payments/
│   └── forms.py              # Reorder fields in Meta.fields list
├── templates/
│   └── payments/
│       └── create.html       # Reorder field rendering, add responsive layout
```

**Structure Decision**: Django web application with backend-only changes. No new files needed — only two existing files are modified.

## Complexity Tracking

No constitution violations requiring justification.
