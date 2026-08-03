# Feature Specification: Fix ClassPrice Demarcation on New Price Entry

**Feature Branch**: `062-fix-classprice-demarcation`

**Created**: 2026-08-02

**Status**: Draft

**Input**: User description: "AS a developer I want to fix a bug in the classes/prices/ webpage. The bug is when adding a new price, the previous price is not being demarked as Actual, and is not being updated in the other related fields as well"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Admin adds a new price, previous prices are automatically archived (Priority: P1)

When an admin adds a new class price, any existing price records that were marked as "Current" must be automatically updated: their `current` flag must be set to false, their `changed_at` timestamp must be set to the moment the new price is entered, and `changed_by` must record the admin who performed the action. The price history table must then show exactly one "Current" price (the newly added one) and the previously current prices must appear as "Inactive" with their superseded timestamp and user populated.

**Why this priority**: This is the core bug — the entire purpose of the `current`, `changed_at`, and `changed_by` auditing fields is to track which price is active and when/how previous prices were superseded. Without this fix, the history table shows incorrect data and multiple "Current" prices coexist, making the feature unusable.

**Independent Test**: Can be fully tested by creating an initial price (which should be "Current"), then adding a second price and verifying that the first price is no longer "Current", its `changed_at` is populated, and `changed_by` shows the admin who added the second price. The history table must show exactly one record with a green "Current" badge.

**Acceptance Scenarios**:

1. **Given** no current prices exist, **When** an admin adds a new price of $100, **Then** the new price is created with `current=True`, `created_by` set to the admin, and no existing prices are modified (there are none).
2. **Given** a current price of $100 exists, **When** an admin adds a new price of $150, **Then** the $100 price is updated to `current=False`, `changed_at` is set to the current timestamp, and `changed_by` is set to the admin who added the new price; the $150 price is created with `current=True`.
3. **Given** three current prices of $100, $120, and $130 exist (legacy state from the bug), **When** an admin adds a new price of $150, **Then** all three previous prices are updated to `current=False` with `changed_at` and `changed_by` populated; the $150 price is the only one with `current=True`.
4. **Given** a current price of $100 exists, **When** a non-admin user attempts to add a price, **Then** the operation is rejected with an access denied error and the existing price remains unchanged.

---

### Edge Cases

- What happens when an admin adds a price with the same decimal value as an existing current price? The new record is created and the old one is still archived — duplicates are allowed as separate historical records.
- What happens when the first price in the system is added? No existing prices to update — the new price is simply created with `current=True` and no errors occur.
- What happens if the database transaction fails midway? All changes within the atomic transaction are rolled back — no partial updates occur.
- What happens when multiple current prices exist from the pre-fix state? All of them are archived together when the next new price is added.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: When a new class price is entered, the system MUST set all existing price records where `current=True` to `current=False`.
- **FR-002**: When a new class price is entered, the system MUST set the `changed_at` field of each superseded price to the timestamp of when the new price is entered.
- **FR-003**: When a new class price is entered, the system MUST set the `changed_by` field of each superseded price to the user who is entering the new price.
- **FR-004**: The price entering operation (creating the new price and retiring existing ones) MUST execute within a single database transaction, so all changes succeed or none do.
- **FR-005**: After a new price is entered, the price history page MUST show exactly one price record with the "Current" badge (the most recently added one).

### Key Entities

- **ClassPrice**: A monetary amount record for class prices. Key attributes: `price` (decimal amount), `current` (boolean flag indicating active price), `created_at` (when the record was created), `created_by` (who created it), `changed_at` (when this price was superseded, nullable), `changed_by` (who superseded it, nullable). Prices cannot be deleted — only archived by setting `current=False`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After any price entry operation, exactly one price record has `current=True` in the database (verified by query).
- **SC-002**: Every superseded price record has a non-null `changed_at` timestamp and a non-null `changed_by` foreign key.
- **SC-003**: The price history page shows a "Superseded" date and "Changed by" user for every inactive price record.
- **SC-004**: An admin can add a price and see the correct history reflected on the page within a single page load cycle.

## Assumptions

- The `changed_at` field stores a simple timestamp (not a date-only field), set to the moment the new price is created.
- Prices with the same monetary value are allowed as separate historical entries; no duplicate price value enforcement is needed.
- The fix is limited to the `enter_price()` classmethod on the `ClassPrice` model — no changes to forms, templates, or views are required (the templates already render `changed_at` and `changed_by` correctly when populated).
- Existing data where multiple `current=True` records coexist (from the pre-fix state) will be corrected the next time a new price is added, since the fix archives all current prices at once. No data migration is needed.
- The `ClassPrice.enter_price()` classmethod signature (`new_price`, `changed_by`) does not change; it accepts the same arguments.
