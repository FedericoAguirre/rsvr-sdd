# Research: Add Reservation Status

## Overview

Research decisions for adding a status field to the Reservation model. All technology choices are resolved by examining the existing project codebase — no external research was needed.

## Decisions

### Status Field Representation

- **Decision**: Use Django `CharField` with `choices` (not a separate model or integer field)
- **Rationale**: Simplest approach matching existing patterns in the project (`Equipment.status` uses the same pattern). Only 3 discrete values with no dynamic additions needed. Using a separate model would add unnecessary complexity (YAGNI).
- **Alternatives considered**:
  - IntegerField with constants: More complex to read in database and templates, adds translation overhead
  - Separate Status model: Over-engineered for 3 fixed values

### Status Values

- **Decision**: Three states: `reserved` (default), `used`, `unused`
- **Rationale**: Directly matches the feature spec requirements. The "reserved" default maintains backward compatibility with existing reservations that have no explicit status.
- **Alternatives considered**:
  - Two states (used/unused with absence = reserved): Less explicit, harder to filter
  - Four states (+ "cancelled"): Out of scope per spec

### UI Interaction for Status Change

- **Decision**: Status change via action buttons on the reservation detail view (POST requests), not via the edit form
- **Rationale**: Prevents accidental status changes during data edits. Clear, single-purpose actions are safer and more discoverable. Matches spec requirement of "marking" a reservation.
- **Alternatives considered**:
  - Dropdown in list view: Could cause accidental changes
  - Toggle button with confirmation: Adds unnecessary UX complexity
  - Via edit form (ModelForm): Too easy to accidentally change status while editing other fields

### i18n Approach

- **Decision**: Use Django's existing i18n `gettext` / `{% trans %}` with the existing Spanish locale at `backend/locale/es/LC_MESSAGES/django.po`
- **Rationale**: The project already has i18n configured with `LANGUAGE_CODE = "es"` and 351 existing translations. Reusing the existing system maintains consistency.
- **Alternatives considered**:
  - Hardcoded Spanish strings: Violates Constitution III (User Experience Consistency) which requires i18n package usage
  - Separate locale file: Unnecessary — the existing django.po already covers the reservations app

### Authorization

- **Decision**: Reuse existing `@login_required` + `@user_passes_test(is_staff)` or `StaffRequiredMixin` patterns from the project's existing views
- **Rationale**: The spec requires Administrator and Operator roles. The project already restricts reservation management to staff users.
- **Alternatives considered**:
  - Custom permission system: Over-engineered — existing staff-based auth is sufficient
  - Django admin-only changes: Would require operators to use admin interface (poor UX)

### Test Strategy

- **Decision**: Update existing test file `test_reservations_list.py` with new test classes for status display, status filtering, and status change. Follow existing patterns using `@pytest.mark.django_db`, class-based tests, and model fixtures.
- **Rationale**: TDD is non-negotiable per Constitution II. Existing tests provide clear patterns to follow.
- **Alternatives considered**:
  - New test file: Adds unnecessary file count — status tests logically belong with reservation list tests
