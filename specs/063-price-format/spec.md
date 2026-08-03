# Feature Specification: Price Format Display

**Feature Branch**: `063-price-format`

**Created**: 2026-08-02

**Status**: Draft

**Input**: User description: "As an operator I want to see the price in format $NNN,NNN.NN"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Operator views class prices with formatted amounts (Priority: P1)

An operator navigates to the class prices page and sees all prices displayed with a dollar sign, thousand separators, and exactly two decimal places. Previously, prices appeared as raw numbers (e.g., `100.00`) without currency symbols or separators, making them harder to read at a glance. Now they appear as `$100.00`, `$1,500.00`, or `$10,000.00`.

**Why this priority**: This is the core request — making prices human-readable in the format explicitly requested by the operator. All other price display locations benefit from the same formatting change.

**Independent Test**: Can be fully tested by navigating to the class prices page and verifying that every price value in the current prices alert and the price history table is displayed as `$N,NNN.NN` format (dollar sign, commas for thousands, dot for decimals, exactly two decimal places). Raw decimal values without formatting confirm the fix.

**Acceptance Scenarios**:

1. **Given** a current price of 100.00 exists, **When** the operator views the class prices page, **Then** the price is displayed as `$100.00`.
2. **Given** multiple current prices of 1500.00 and 3000.00 exist, **When** the operator views the class prices page, **Then** the prices are displayed as `$1,500.00` and `$3,000.00` respectively.
3. **Given** the price history table contains an inactive price of 100000.00, **When** the operator views the table, **Then** the price is displayed as `$100,000.00`.
4. **Given** a price with an integer value of 50, **When** the operator views the class prices page, **Then** the price is displayed as `$50.00` (always shows two decimal places).
5. **Given** a price of 0.00 exists (edge case), **When** the operator views the class prices page, **Then** the price is displayed as `$0.00`.

---

### User Story 2 - Operator sees formatted prices on the class prices input form (Priority: P2)

When editing or entering a class price via the form, the input field displays a clear, properly formatted numeric interface consistent with the display format seen on the price list page.

**Why this priority**: Form consistency enhances user experience and reduces data entry errors, but the primary value is in the display (Story 1).

**Independent Test**: Can be tested by opening the class price form and verifying the price input field clearly indicates expected format and displays the amount correctly when editing.

**Acceptance Scenarios**:

1. **Given** the operator opens the "add new price" form, **When** the page loads, **Then** the price input field uses a numeric input with appropriate step value for decimal entry.
2. **Given** the operator enters a price of 1500.00 and submits, **When** the page reloads with the list of prices, **Then** the newly entered price is displayed as `$1,500.00`.

---

### Edge Cases

- What happens when a price has a value with more than 2 decimal places? The database stores `Decimal(10, 2)`, so values are always rounded to 2 decimal places — the formatting reflects this.
- What happens when a price value is `None` or null? The system displays an empty string or a dash, not an error.
- What happens with very large prices (e.g., 99999999.99)? The format handles up to the maximum stored value (10 total digits) correctly with thousand separators (e.g., `$99,999,999.99`).
- What happens when the operator's browser has locale settings that differ from the app's format? The display format is fixed and does not depend on browser locale — the operator always sees the consistent `$N,NNN.NN` format.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST display all class price amounts with a leading dollar sign (`$`).
- **FR-002**: The system MUST format class price amounts with commas as thousand separators (e.g., `$1,500.00`).
- **FR-003**: The system MUST display class price amounts with exactly two decimal places, using a dot as the decimal separator (e.g., `$100.00`).
- **FR-004**: The formatted price format MUST be applied consistently to both the "Current prices" summary section and the price history table on the class prices page.
- **FR-005**: The price input form MUST continue to accept numeric decimal input with two-decimal precision.
- **FR-006**: The system MUST handle null or missing price values gracefully, displaying an empty string rather than an error.

### Key Entities

- **ClassPrice**: A monetary amount record for class prices. Key attribute: `price` (Decimal field with max 10 digits and 2 decimal places). The display format should render this value as `$N,NNN.NN`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every price value on the class prices page is displayed with a `$` prefix, comma thousand separators, and exactly two decimal places (verified by visual inspection of the rendered page).
- **SC-002**: An operator can distinguish between prices like $1,500.00 and $150.00 at a glance without counting digits — the thousand separator makes the magnitude immediately clear.
- **SC-003**: Displaying formatted prices does not break the ability to enter and save new prices via the form — a price entered as a decimal value saves correctly and appears formatted on the subsequent page load.
- **SC-004**: Zero formatting-related errors appear in the application logs during normal price viewing, entry, or editing operations.

## Assumptions

- The existing `currency` template filter in the payments app (`payment_extras.currency`) already produces the exact format requested (`$N,NNN.NN`) and can be reused or adapted for class prices.
- The format is static (not locale-aware) — the operator always sees the dollar sign format regardless of browser or server locale settings. This matches the existing payment display behavior.
- No changes to the `ClassPrice` model or database schema are needed — only presentation-layer formatting changes.
- The price form input field remains a numeric input (not a formatted text field) to preserve browser-native numeric validation and keyboard behavior.
- i18n tags are already in place on the class prices template; this feature does not introduce new user-visible text strings that require translation.
