# Feature Specification: Replace WeasyPrint with ReportLab for Cross-Platform PDF

**Feature Branch**: `038-replace-weasyprint-pdf`

**Created**: 2026-07-12

**Status**: Draft

**Input**: User description: "As a System Architect, I want to change the weasyprint for the reportlab packge to support pdf creation in linux/max and windows production env"

## User Scenarios & Testing

### User Story 1 - Developer Sets Up Project on Any OS (Priority: P1)

A developer clones the project on macOS, Linux, or Windows, installs dependencies with `pip install`, and can immediately generate PDFs without installing any system-level packages.

**Why this priority**: Removing platform-specific system dependencies is the core motivation for the change. Without this, the feature delivers no value.

**Independent Test**: Developer runs `pip install` on a clean environment on each target OS (macOS, Linux, Windows) then invokes the PDF generation endpoint. PDF is returned without errors.

**Acceptance Scenarios**:

1. **Given** a developer on macOS, **When** they run `pip install` and access the PDF generation endpoint, **Then** a valid PDF is returned
2. **Given** a developer on Windows, **When** they run `pip install` and access the PDF generation endpoint, **Then** a valid PDF is returned
3. **Given** a developer on Linux (without libpango/libcairo installed), **When** they run `pip install` and access the PDF generation endpoint, **Then** a valid PDF is returned

---

### User Story 2 - User Downloads Reservation PDF (Priority: P1)

A user clicks the "Export PDF" button on the reservations page and downloads a PDF file containing the same reservation data as before.

**Why this priority**: The end-user experience must remain intact. If PDFs break or lose data, the change is unacceptable regardless of platform benefits.

**Independent Test**: Automated test renders the reservation PDF view and asserts the response is a valid PDF with the expected content fields.

**Acceptance Scenarios**:

1. **Given** a class slot with reservations, **When** the user clicks "Export PDF", **Then** a PDF file is downloaded with the correct filename
2. **Given** the PDF is opened, **When** inspected, **Then** it contains the class slot name, date, and reservation list
3. **Given** no reservations exist for a class slot, **When** the user exports the PDF, **Then** a PDF is returned showing the class slot header and a \"No reservations\" message

---

### User Story 3 - Developer Runs PDF Tests Without Special Setup (Priority: P2)

A developer runs the test suite on any OS and all PDF-related tests pass without requiring system library pre-installation.

**Why this priority**: Currently PDF tests fail on macOS/Windows without WeasyPrint system deps, which reduces developer confidence and CI reliability.

**Independent Test**: Developer runs `pytest` on a machine without libpango/libcairo and all PDF tests pass.

**Acceptance Scenarios**:

1. **Given** a macOS development machine, **When** the test suite runs, **Then** all PDF-related tests pass
2. **Given** a Windows development machine, **When** the test suite runs, **Then** all PDF-related tests pass

### Edge Cases

- What happens when PDF generation fails (e.g., out of disk space, memory exhaustion)? System MUST preserve the existing graceful error handling (log the error, display user-friendly message, redirect to the reservations list)
- How does the system handle very large reservation lists that could generate multi-page PDFs? ReportLab MUST handle pagination automatically for lists exceeding one page
- What if ReportLab is not installed (missing dependency)? The system MUST provide a clear import error rather than a cryptic failure
- How are special characters (accents, ñ, symbols in reservation names) handled in the PDF output? The generated PDF MUST display non-ASCII characters correctly

## Requirements

### Functional Requirements

- **FR-001**: System MUST generate reservation PDFs using a pure-Python library that does not require system-level packages
- **FR-002**: System MUST NOT require any system-level packages (libpango, libcairo, libgdk-pixbuf, or similar) to generate PDFs
- **FR-003**: The existing PDF library (which requires system packages) MUST be removed from project dependencies
- **FR-004**: System MUST remove the system dependency installation instructions (libpango, libcairo, etc.) from the Dockerfile
- **FR-005**: Generated PDF MUST contain the same reservation data as currently produced: class slot name, formatted date, and reservation list with reservation details
- **FR-006**: PDF filename MUST follow the existing format: `reservations_{sanitized_slot_name}_{compact_date}.pdf`
- **FR-007**: System MUST preserve the existing error handling: on failure, log the error, display a user-friendly message, and redirect the user to the reservations list
- **FR-008**: System MUST handle non-ASCII characters (Spanish accents, ñ, etc.) correctly in the PDF output
- **FR-009**: System MUST handle multi-page reservation lists with automatic pagination

### Key Entities

- **Reservation PDF**: Generated document output containing class slot information and reservation details for a given date
- **Reservation Data**: Source data (class slot name, date, reservation list) consumed by the PDF generator, unchanged by this feature

## Success Criteria

### Measurable Outcomes

- **SC-001**: Developers can generate PDFs on macOS, Linux, and Windows after installing project dependencies without any additional system package installation
- **SC-002**: All existing PDF-related tests pass on all three target operating systems
- **SC-003**: The generated PDF contains the class slot name, formatted date, and full reservation list — verifiable by opening the PDF
- **SC-004**: PDF generation completes within 10 seconds for reservation lists of up to 100 entries (matching current performance baseline)
- **SC-005**: No regression in non-PDF functionality (all existing non-PDF tests continue to pass)

## Clarifications

### Session 2026-07-12

- Q: How closely should the ReportLab PDF match the current WeasyPrint HTML+CSS visual layout? → A: Same data, similar visual structure — table with borders, appropriate spacing, readable fonts. Pixel-perfect not required.
- Q: What should the PDF look like when there are no reservations? → A: Show class slot header + date with "No reservations" message in the table area.

## Assumptions

- The visual layout of the ReportLab-generated PDF should match the current HTML+CSS layout in visual structure: same data fields, table with borders, appropriate spacing and readable fonts. Pixel-perfect replication is not required.
- ReportLab is available on PyPI and installable via `pip` across all target platforms without system dependencies
- The existing HTML template (`reservation_list_pdf.html`) can be retired once the ReportLab implementation is complete
- Docker image size will decrease after removing WeasyPrint system library packages
- Automatic pagination in ReportLab is sufficient for reservation lists that span multiple pages
