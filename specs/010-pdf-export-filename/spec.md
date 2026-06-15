# Feature Specification: Rename Exported Reservations PDF

**Feature Branch**: `010-pdf-export-filename`

**Created**: 2026-06-15

**Status**: Draft

**Input**: User description: "Change the name of the exported Reservations PDF to reservations_<class>_YYYYMMDD.pdf where class is the class_slot name and YYYYMMDD is the filter date"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Download PDF with new filename format (Priority: P1)

An Operator or Administrator exports a reservations list PDF and receives a file named `reservations_<class_slot_name>_YYYYMMDD.pdf` that clearly identifies the class slot and date without needing to open the file.

**Why this priority**: This is the core change — without the renamed file, the feature delivers no value.

**Independent Test**: Can be tested by filtering by any class slot and date, clicking Export PDF, and verifying the downloaded filename uses the new format.

**Acceptance Scenarios**:

1. **Given** the Operator is viewing a reservations list for class "Morning Yoga" on date 2026-06-15, **When** they click Export PDF, **Then** the downloaded filename is `reservations_Morning_Yoga_20260615.pdf`
2. **Given** the Operator is viewing a reservations list for class "Evening Climbing" on date 2026-12-01, **When** they click Export PDF, **Then** the downloaded filename is `reservations_Evening_Climbing_20261201.pdf`
3. **Given** the Administrator is viewing a reservations list for any class and date, **When** they export the PDF, **Then** the downloaded filename follows the `reservations_<class>_YYYYMMDD.pdf` format

---

### Edge Cases

- What happens when the class slot name contains characters that are invalid in filenames (e.g., `/`, `\`, `:`)? Non-alphanumeric characters (except spaces) are removed or replaced with underscores to produce a safe filename.
- What happens when the class slot name is very long? The class slot name is included as-is (sanitized), respecting filesystem filename length limits.
- What happens if the date parameter is missing or empty? The PDF is still generated with a fallback filename (e.g., `reservations_no_date.pdf`).
- What happens if the class slot name contains multiple consecutive spaces? Spaces are collapsed and replaced with single underscores.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The exported PDF filename MUST follow the format `reservations_<class>_YYYYMMDD.pdf` where `<class>` is the sanitized class slot name and `YYYYMMDD` is the filter date
- **FR-002**: The date in the filename MUST use the compact YYYYMMDD format (e.g., `20260615`), without dashes, slashes, or other separators
- **FR-003**: The class slot name in the filename MUST be sanitized: spaces are replaced with underscores, and characters invalid in filenames are removed or replaced
- **FR-004**: The exported PDF content MUST remain unchanged — only the filename is affected
- **FR-005**: If the date parameter is missing or empty, the filename MUST fall back to `reservations_<class>_no_date.pdf`
- **FR-006**: If both class slot and date are missing, the filename MUST fall back to a safe default (e.g., `reservations_export.pdf`)

### Key Entities

- **Class Slot**: Represents a scheduled class time slot (e.g., "Morning Yoga", "Evening Climbing"). Its name is used in the PDF filename.
- **Reservation**: The association between a Client, Equipment, and Class Slot for a specific date. The filter date determines the YYYYMMDD portion of the filename.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The downloaded PDF filename always matches the `reservations_<class>_YYYYMMDD.pdf` pattern regardless of which class slot or date is selected
- **SC-002**: All existing PDF export functionality (content, formatting, download behavior) is preserved — only the filename changes
- **SC-003**: Special characters in class slot names never produce invalid filenames or cause download errors
- **SC-004**: The filename change does not increase the time to generate or download the PDF

## Assumptions

- The existing PDF generation infrastructure (WeasyPrint or equivalent) remains unchanged
- The class slot name, date, and export functionality are already available in the system (as implemented in 008-reservations-list-per-class)
- Only the `Content-Disposition` filename header needs to change in the PDF response
- The class slot name is always available in the PDF view context
- Filename sanitization follows standard filesystem-safe character rules (no `/`, `\0`, control characters)
