# Feature Specification: Class Price Versioning & Audit

**Feature Branch**: `058-class-prices`

**Created**: 2026-08-02

**Status**: Draft

**Input**: User description: "Using @ai/features/todos/28_Class_prices.md create the specs for the new feature"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Update a Class Price with Full History Preservation (Priority: P1)

As an administrator, when I update the price of a class, the previous price is automatically retired and retained with a full record of who changed it and when, so that the pricing history of every class is always traceable and no pricing data is ever lost.

**Why this priority**: Accurate and tamper-proof pricing records are essential for billing transparency, financial audits, and compliance. Losing or overwriting pricing history directly undermines trust and accountability.

**Independent Test**: Can be fully tested by an administrator setting an initial price for a class, then updating it to a new value, and confirming that both the previous and the new price are visible with their respective creation and change metadata, and that only the newest entry is flagged as the active price.

**Acceptance Scenarios**:

1. **Given** a class with no prior price, **When** an administrator sets a new price, **Then** a new active price record is created with the current date and the administrator is recorded as its creator, and there is exactly one active price for that class.
2. **Given** a class with an active price, **When** an administrator enters a new price, **Then** the previous active price is automatically marked as inactive with the date and user of the change recorded, a new active price is created for that class, and the previous price remains visible and queryable.
3. **Given** a class with a currently active price, **When** the price is changed, **Then** only one active (current) price exists for that class afterward, and no price record is removed from history.

---

### User Story 2 - Review Complete Price History for a Class (Priority: P2)

As an administrator, I want to view all price records for a class ordered from most recent to oldest, with the active price clearly highlighted, so I can quickly understand the current pricing and audit every change that ever occurred.

**Why this priority**: Administrators need a single, trustworthy view to answer questions such as "what was the price last month?" or "who changed it?" without hunting across multiple systems or screens.

**Independent Test**: Can be fully tested by an administrator opening the class prices view for a class that has been re-priced multiple times and verifying that records appear in descending chronological order, that the current price carries a clear visual indicator, and that every record shows the user and date that created it.

**Acceptance Scenarios**:

1. **Given** a class with multiple price records (active and inactive), **When** an administrator opens the class prices view, **Then** all records are displayed in descending order (most recent first) and the currently active price is clearly indicated.
2. **Given** a price list for a class, **When** an administrator inspects an individual historical record, **Then** the record shows who created it and when, and if it was superseded, who changed it and when it became inactive.
3. **Given** a class whose price has been updated more than once, **When** the prices are listed, **Then** every historical price remains accessible and queryable.

---

### User Story 3 - Prevent Deletion of Price Records (Priority: P3)

As an administrator, any attempt to delete a class price record is rejected, so that the pricing history can never be lost or tampered with.

**Why this priority**: Price records form part of the financial audit trail; allowing deletion would create gaps that could hide irregularities or complicate compliance reporting.

**Independent Test**: Can be fully tested by attempting to delete any price record (active or historical) and confirming the action is refused and the record remains intact and unchanged.

**Acceptance Scenarios**:

1. **Given** a class with existing price records, **When** an administrator attempts to delete an active price record, **Then** the deletion is refused and the record remains in place.
2. **Given** a class with historical price records, **When** an administrator attempts to delete an inactive (historical) price record, **Then** the deletion is refused and the record remains unchanged.
3. **Given** a rejected deletion attempt, **Then** the user receives a clear message explaining that price records cannot be deleted.

---

### Edge Cases

- What happens when a price is set for a class that has never had a price? A new active price record is created; there is no prior record to retire.
- What happens when an administrator attempts to delete a price record? The deletion is rejected with a clear explanation that price history cannot be deleted.
- What happens when two administrators change a class price at nearly the same time? The system guarantees that only one active price results for the class and both changes are captured in the history.
- What happens if a class accumulates many years of price history? All historical records remain queryable and displayable regardless of volume.
- What happens if historical price records are modified directly? Historical records are immutable; modifications to past records are not permitted, and any attempt to alter them is rejected.
- What happens when a non-administrator tries to change a price? Price changes are restricted to authorized administrators only.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST preserve the previous price record as inactive when a new price is entered for a class.
- **FR-002**: The system MUST record the date and time a price became inactive (the change date) when it is superseded.
- **FR-003**: The system MUST create a new active price record with the current date whenever a price is entered or changed for a class.
- **FR-004**: The system MUST record the identity of the user who created each price record.
- **FR-005**: The system MUST record the identity of the user who retired each price record when it is superseded.
- **FR-006**: The system MUST display all price records for a class in descending order (most recent first).
- **FR-007**: The system MUST clearly indicate which price record is currently active on the class prices view.
- **FR-008**: The system MUST prevent deletion of any class price record, whether active or historical.
- **FR-009**: The system MUST ensure that only one active price exists for any given class at any point in time.
- **FR-010**: The system MUST retain all historical price records and keep them queryable for audit purposes.
- **FR-011**: The system MUST restrict the ability to change class prices to authorized administrators only.
- **FR-012**: The system MUST attach creation metadata (who and when) to every price record.

### Key Entities *(include if feature involves data)*

- **Class Price Record**: A versioned record representing a price for a class at a point in time. Attributes include the price amount, the date it became effective, the date it became inactive (when superseded), a flag indicating whether it is the current active price, and creation/change metadata (which user and when). Each record is permanently tied to the class it prices.
- **Current Price**: The single price record flagged as active for a class at any given moment. Exactly one current price may exist per class, and it is replaced rather than overwritten when a price changes.
- **Inactive Price**: Any price record no longer flagged as active. These records are permanently retained and queryable, forming the complete pricing history of a class.
- **Audit Trail**: The complete, immutable history of all price records for a class, including who created or changed each record and when.
- **Class**: The bookable offering to which one or more price records belong; each class may have at most one active price at a time.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of price change history is preserved with no data loss: whenever a class price is updated, the previous price is retained as a historical record rather than overwritten.
- **SC-002**: The class prices view loads and displays the complete price history for any class in under 2 seconds.
- **SC-003**: At all times, only one active (current) price exists for any given class; duplicate active prices never occur.
- **SC-004**: At least 95% of administrators can correctly identify the currently active price on the class prices view within 10 seconds of opening it.
- **SC-005**: 100% of price records are non-deletable: no attempt to delete an active or historical price record ever succeeds.
- **SC-006**: 100% of price changes are attributable to a specific administrator (each creation and each retirement records the acting user).
- **SC-007**: All historical price records remain queryable and accessible for at least as long as the class exists.

## Assumptions

- The application already provides administrator authentication and role-based permission management; this feature reuses that existing authorization model.
- Classes already exist in the system as bookable offerings and are uniquely identifiable.
- Price is a single positive monetary decimal value.
- Prices are managed centrally by administrators; students and instructors do not change prices themselves.
- The class prices view is accessible from the existing class management area and is not itself in scope for redesign.
- No automated or scheduled price changes are applied by the system; all price changes are initiated by an administrator action.
- This initial version does not include a reason/note field for price changes or approval workflows (identified as future enhancements).
- Bulk price uploads are out of scope for the initial implementation.

## Out of Scope

- Price forecasting or predictive analytics.
- Bulk price uploads.
- Scheduled or automated future price changes.
- Price change notifications to students or instructors.
- Reason/note field for price changes (future enhancement).
- Approval workflow for price changes (future enhancement).
- Price change impact analysis (affected classes, revenue projections) (future enhancement).

## Future Enhancements

- Audit log export functionality.
- Price change notifications.
- Reason/note field for price changes.
- Approval workflow for price changes.
- Price change impact analysis (affected classes, revenue projections).
- Scheduled price changes.
- Bulk price uploads.
