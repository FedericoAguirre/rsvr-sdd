# Feature Specification: Remove Custom Range

**Feature Branch**: `033-remove-custom-range`

**Created**: 2026-07-10

**Status**: Draft

**Input**: User description: "In the payments/reports webpage, remove the 'Rango personalizado' option from the 'Agrupar por' dropdown list and remove the associated functionality and code"

## User Scenarios & Testing

### User Story 1 — Dropdown no longer shows "Custom Range" (P1)

An administrator navigates to Reports > Payments and sees the "Group by" dropdown with three options: Day, Week, Month. The "Custom Range" option is no longer present. The date range inputs remain visible for filtering the selected grouping.

**Why this priority**: This is the single requirement — removing the option and its associated code. No other changes are needed.

**Independent Test**: Can be tested by loading the Reports > Payments page and confirming the dropdown contains only Day, Week, and Month options.

**Acceptance Scenarios**:

1. **Given** an administrator is on the Reports > Payments page, **When** they open the "Group by" dropdown, **Then** the only options are "Day", "Week", and "Month".
2. **Given** the page is loaded with a `?grouping=range` query parameter (e.g., from a previously saved bookmark), **When** the view processes the request, **Then** it defaults to "month" grouping instead of crashing or showing an error.
3. **Given** the backend code has been updated, **When** any request is processed with `grouping=range`, **Then** the system treats it as if grouping was not specified (defaults to month).

### Edge Cases

- What happens if a user has a bookmark with `?grouping=range`? The system should gracefully fall back to the default grouping (month) without error.
- Are the date range inputs (`start`/`end`) still useful without "Custom Range"? Yes — they still filter the data for Day, Week, and Month groupings.
- What if existing tests reference the `range` grouping? They must be updated to remove the "range" test cases.

## Requirements

### Functional Requirements

- **FR-001**: System MUST remove "Custom Range" from the "Group by" dropdown on the Reports > Payments page.
- **FR-002**: System MUST remove the backend logic that handles the `range` grouping value in the view.
- **FR-003**: System MUST fall back to the default grouping (month) when an unrecognized or removed grouping value is submitted.
- **FR-004**: Date range inputs (Start Date, End Date) MUST remain functional for filtering data in Day, Week, and Month groupings.

### Key Entities

- **Payment Report View**: The existing view in `payments/views.py` that handles `grouping` parameter values "day", "week", "month", and "range". The `range` case must be removed; it is functionally equivalent to `day` and no longer needed.
- **Payment Reports Template**: The dropdown in `payment_reports.html` lists four options. The `range` option must be removed.

## Success Criteria

### Measurable Outcomes

- **SC-001**: The "Group by" dropdown displays exactly three options (Day, Week, Month) after the change.
- **SC-002**: Submitting `?grouping=range` gracefully defaults to month grouping without error.
- **SC-003**: All existing report tests pass after updating/removing "range" test cases.
- **SC-004**: Date range inputs continue to work with all remaining grouping modes.

## Assumptions

- The `range` grouping value is functionally identical to `day` grouping in the current code (both use `.values("date", "payment_type")`). Removing it loses no unique functionality.
- The date range inputs (`start`/`end`) should remain visible and functional — they serve Day, Week, and Month groupings by filtering the date range.
- No i18n changes are needed beyond removing the "Custom Range" key from `django.po` to keep translations clean.
