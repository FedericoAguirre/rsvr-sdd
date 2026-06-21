# Feature Specification: Remove Reservations Dead Code

**Feature Branch**: `017-remove-reservations-dead-code`

**Created**: 2026-06-21

**Status**: Draft

**Input**: User description: "As developer I want to delete the reservations module dead code, take care of keep Export PDF functionality and take as baseline the reservations/ endpoint"

## Clarifications

### Session 2026-06-21

- Q: Should tests covering the removed `/reservations/list/` endpoint be deleted alongside the dead code? → A: Remove tests that exclusively cover the `/reservations/list/` endpoint.
- Q: Should the orphaned ghost migration artifact be simply deleted or properly completed? → A: Create the proper migration to add `updated_by` to the Reservation model.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Clean up redundant reservations list view (Priority: P1)

As a developer, I want to remove the redundant `/reservations/list/` endpoint and its associated view/template so that the reservations module has a single, canonical list view without dead code paths that could cause confusion or maintenance burden.

**Why this priority**: This is the core task — removing the dead code branch. The `/reservations/list/` endpoint duplicates functionality already available in the main `/reservations/` endpoint (with class_slot and date filters), and it is not linked from any template or external reference.

**Independent Test**: Can be verified by navigating to `/reservations/list/` and confirming it returns 404; verifying that the main `/reservations/` page continues to work correctly with all existing filter capabilities.

**Acceptance Scenarios**:

1. **Given** the reservations module, **When** a user visits `/reservations/list/`, **Then** they receive a 404 response
2. **Given** the reservations module, **When** a user visits `/reservations/` with class_slot and date query parameters, **Then** they see the filtered list as before
3. **Given** the reservations module, **When** a user visits `/reservations/` without query parameters, **Then** they see the full reservations list as before

---

### User Story 2 - Preserve and relocate Export PDF functionality (Priority: P1)

As a user, I want to continue exporting reservation lists as PDFs so that I can print or share class attendance records, with the export accessible from the main reservations page.

**Why this priority**: The Export PDF is a critical feature used by instructors and administrators. It must be preserved and remain accessible from the main `/reservations/` endpoint.

**Independent Test**: Can be tested by visiting the PDF export URL with class_slot and date parameters and confirming a valid PDF is returned as a downloadable file.

**Acceptance Scenarios**:

1. **Given** a user is on the reservations page with a class_slot and date selected, **When** they click "Export PDF", **Then** a PDF file is downloaded with the correct filename format
2. **Given** a developer has applied the changes, **When** the PDF export URL is accessed with valid parameters, **Then** the response Content-Type is `application/pdf`
3. **Given** the PDF export is triggered without a class_slot, **When** the request is processed, **Then** a PDF with "unknown" in the filename is generated

---

### User Story 3 - Complete abandoned `updated_by` migration (Priority: P2)

As a developer, I want to replace the orphaned compiled migration artifact with a proper migration that adds an `updated_by` field to the Reservation model, so that the model accurately tracks who last modified each reservation.

**Why this priority**: This task upgrades a simple cleanup into a meaningful model improvement by completing work that was started but abandoned, adding a field that complements the existing `created_by` and `updated_at` fields.

**Independent Test**: Can be verified by confirming the migration runs successfully, the Reservation model has an `updated_by` field, and no orphaned compiled artifacts remain in the migration directory.

**Acceptance Scenarios**:

1. **Given** the migration directory, **When** the proper migration is created and the orphaned artifact is removed, **Then** every compiled file has a corresponding source file
2. **Given** the migration is run, **When** the system migration process completes, **Then** no errors occur
3. **Given** the migration is complete, **When** checking the Reservation model definition, **Then** it includes an `updated_by` field

---

### Edge Cases

- What happens if a user has bookmarked the old `/reservations/list/` URL? They will receive a 404 — no redirect is provided since this endpoint was never linked from any UI.
- What happens if the PDF export URL needs to be accessed from external integrations? The new URL path will be documented and accessible.
- What happens if there are existing links from external systems pointing to `/reservations/list/`? These will break — no redirect is maintained for the dead endpoint.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST remove the `/reservations/list/` endpoint and its associated logic
- **FR-002**: System MUST remove the template used exclusively by the `/reservations/list/` page
- **FR-003**: System MUST remove tests that exclusively cover the removed `/reservations/list/` endpoint
- **FR-004**: System MUST relocate the Export PDF functionality from `/reservations/list/pdf/` to `/reservations/pdf/`
- **FR-005**: System MUST update all references to the old PDF export URL to use the new `/reservations/pdf/` URL
- **FR-006**: System MUST create a proper migration to add an `updated_by` field to the Reservation model and remove any orphaned compiled migration artifacts
- **FR-007**: System MUST keep the main `/reservations/` endpoint and its functionality unchanged
- **FR-008**: System MUST keep the PDF export logic and its template unchanged
- **FR-009**: System MUST keep the reservation creation, detail view, and status change functionality unchanged

### Key Entities *(include if feature involves data)*

- **Reservation**: Core entity representing a client's equipment reservation for a specific class slot on a given date. Gains an `updated_by` field to track who last modified each reservation.
- **ClassSlot**: Entity representing a time slot for a class. Remains unchanged.
- **Export PDF**: Generated document containing reservation data filtered by class slot and date. Relocated to new URL path.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The `/reservations/list/` endpoint returns 404 after cleanup — 100% of dead route requests are eliminated
- **SC-002**: Export PDF functionality works from the main `/reservations/` page with the same output quality, filename format, and content type as before
- **SC-003**: All existing tests for the main reservations list, PDF export, status management, and status display continue to pass without modification
- **SC-004**: Reservation model includes an `updated_by` field after migration, and no orphaned migration artifacts remain

## Assumptions

- The `/reservations/list/` endpoint is dead code because no template, external link, or integration references it (confirmed via codebase search)
- The main `/reservations/` endpoint already handles all filtering capabilities (by class_slot, date, and status) that the removed endpoint provided
- The Export PDF URL relocation maintains backward compatibility only at the new path — no redirect from the old path is required
- Users who bookmarked the old `/reservations/list/` URL are expected to be rare or nonexistent
