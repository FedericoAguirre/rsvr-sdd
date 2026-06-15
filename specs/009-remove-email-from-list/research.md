# Research: Remove Email from Client Column in Reservations List

**Feature**: [spec.md](./spec.md)

## Overview

Minimal research needed — feature is a pure template/view change with no new dependencies, external services, or schema changes.

## Decision Record

| Decision | Choice | Rationale | Alternatives Considered |
|----------|--------|-----------|------------------------|
| Approach | Template-level change | Spec constraint FR-004: `Client.__str__` must not change | Modifying `__str__` (rejected — would affect all client displays) |
| Whitespace handling | Strip extra spaces | Chosen in clarification Q1 — avoids "John " or " Smith" display bugs | Raw concatenation or custom template filter |
| New tests | Yes, view-level | Chosen in clarification Q2 — verifies email absent in all 3 list views | Only existing tests |
| Name formatting | `full_name` filter | Cleanest approach — handles missing parts and whitespace in one place | Template `{% if %}` logic or inline filters |

## Template Filter Design

A `full_name` template filter will be added to the reservations templatetags:

- Input: `Client` instance
- Output: `"FirstName LastName"` if both present, `"FirstName"` or `"LastName"` if only one, empty string if neither
- Handles leading/trailing whitespace: uses `' '.join(filter(None, [first, last]))` logic

## Files to Modify

| File | Change |
|------|--------|
| `backend/apps/reservations/templates/reservations/reservation_list.html` | Lines 46, 58: `{{ r.client }}` → `{{ r.client\|full_name }}` |
| `backend/apps/reservations/templates/reservations/reservation_list_by_slot.html` | Line 26: `{{ r.client }}` → `{{ r.client\|full_name }}` |
| `backend/apps/reservations/templates/reservations/reservation_list_pdf.html` | Line 34: `{{ r.client }}` → `{{ r.client\|full_name }}` |
| `backend/apps/reservations/templatetags/` (new) | Create `reservation_extras.py` with `full_name` filter |
| `backend/tests/test_reservations_list.py` | Add tests for email absence in all 3 views |
