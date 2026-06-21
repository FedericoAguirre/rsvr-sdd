# Feature Specification: CSV Client Upload

**Feature Branch**: `016-csv-client-upload`

**Created**: 2026-06-21

**Status**: Draft

**Input**: User description: "Upload or update client data using a CSV file with first_name, last_name, email, and mobile columns"

## User Scenarios & Testing

### User Story 1 - Upload CSV to create and update clients (Priority: P1)

An Operator uploads a CSV file containing client data. The system reads the file, matches records against existing clients by name or email/mobile, creates new clients for unmatched records, updates fields for matched records, and reports the results.

**Why this priority**: Core feature — without the upload and processing workflow, the feature has no value.

**Independent Test**: Can be tested by uploading a CSV with a mix of new clients and updates to existing clients, then verifying the correct number of creations and updates in the results report.

**Acceptance Scenarios**:

1. **Given** a CSV file with valid headers (first_name, last_name, email, mobile) and data rows, **When** the Operator uploads it, **Then** all records are processed and a summary report is displayed
2. **Given** a CSV row with first_name and last_name matching an existing client (case-insensitive), **When** the file is processed, **Then** that client's email and/or mobile are updated with the CSV values
3. **Given** a CSV row where the email matches an existing client's email (case-insensitive), **When** the file is processed, **Then** that client's first_name, last_name, and mobile are updated with the CSV values
4. **Given** a CSV row where the mobile matches an existing client's mobile, **When** the file is processed, **Then** that client's first_name, last_name, and email are updated with the CSV values
5. **Given** a CSV row whose name, email, and mobile do not match any existing client, **When** the file is processed, **Then** a new client is created with the provided data and set to active status

---

### User Story 2 - CSV validation and error feedback (Priority: P1)

The system validates the CSV file before and during processing, providing clear error messages for invalid files or rows that cannot be processed.

**Why this priority**: Without validation, Operators may lose data or create inconsistent records without realizing it.

**Independent Test**: Can be tested by uploading a CSV with missing required columns or invalid data and verifying an appropriate error message is shown.

**Acceptance Scenarios**:

1. **Given** a CSV file missing the first_name or last_name column, **When** the Operator uploads it, **Then** an error message is displayed indicating the missing required column
2. **Given** a CSV row missing both email and mobile, **When** the file is processed, **Then** that row is skipped and counted as an error in the summary
3. **Given** a CSV file with data cleansing issues (extra spaces, empty strings), **When** the file is processed, **Then** the data is trimmed and normalized before matching

---

### User Story 3 - View processing results (Priority: P2)

After processing, the Operator sees a summary showing how many records were processed, created, updated, and any errors encountered.

**Why this priority**: Feedback is important for confidence but the processing works without it.

**Independent Test**: Can be tested by uploading a file and verifying that the summary displays correct counts matching the file contents.

**Acceptance Scenarios**:

1. **Given** a CSV file with 10 rows (3 new, 5 updates, 2 errors), **When** processing completes, **Then** the summary shows "10 records processed, 3 created, 5 updated, 2 errors"
2. **Given** a CSV file with all new records, **When** processing completes, **Then** the summary shows all records as created

---

### User Story 4 - Download CSV template (Priority: P3)

The Operator can download a sample CSV template to ensure the correct column format when preparing their data.

**Why this priority**: Nice-to-have convenience — Operators can prepare their own CSVs by following the documented format.

**Independent Test**: Can be tested by clicking the download template button and verifying the downloaded CSV has the correct headers and one example row.

**Acceptance Scenarios**:

1. **Given** the Operator is on the upload page, **When** they click "Download Template", **Then** a CSV file with headers (first_name, last_name, email, mobile) and a sample row is downloaded

### Edge Cases

- What happens when a CSV row matches an existing client by both name and email (different clients)? Name match takes priority.
- What happens when the CSV file is empty? An error message is shown.
- What happens when the CSV uses a different encoding? The system handles UTF-8 with BOM gracefully, and rows with encoding issues are reported as errors.
- What happens when a row has duplicate within the same CSV file? Each row is processed independently in order; later rows may overwrite earlier updates to the same client.
- What happens when the CSV file has extra columns beyond the four defined ones? Extra columns are ignored.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST provide a page where Operators can upload a CSV file for client data import
- **FR-002**: The CSV file MUST have a header row with columns: first_name, last_name, email, mobile (in that order)
- **FR-003**: The first_name and last_name columns are REQUIRED — every row must have values for both
- **FR-004**: Every row MUST have at least one of email or mobile (one is required, both are acceptable)
- **FR-005**: The system MUST attempt to match each CSV row to an existing client by first_name + last_name (case-insensitive). If matched, update email and/or mobile with CSV values
- **FR-006**: If name matching does not find an existing client, the system MUST attempt to match by email (case-insensitive). If matched, update first_name, last_name, and mobile
- **FR-007**: If neither name nor email matches, the system MUST attempt to match by mobile. If matched, update first_name, last_name, and email
- **FR-008**: If no match is found by name, email, or mobile, the system MUST create a new client record with the CSV values and set is_active to True
- **FR-009**: The system MUST perform basic data cleansing before processing: trim whitespace from all fields, normalize empty strings to null for optional fields
- **FR-010**: The system MUST validate the CSV header before processing and reject the file if required columns are missing
- **FR-011**: The system MUST validate that at least one of email or mobile is present in each row; rows missing both MUST be skipped and counted as errors
- **FR-012**: After processing all rows, the system MUST display a summary: total records processed, clients created, clients updated, errors
- **FR-013**: Newly created clients MUST have the created_at date set to the current timestamp
- **FR-014**: Updated clients MUST have the updated_at timestamp refreshed to the current timestamp
- **FR-015**: The system MUST provide a downloadable CSV template with the correct headers and a sample row

### Key Entities

- **Client**: The entity being created or updated. Key attributes: first_name, last_name, email, mobile, is_active, created_at, updated_at.
- **CSV File**: The input file with columns first_name, last_name, email, mobile.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An Operator can upload a CSV with up to 1,000 rows and receive processing results within 10 seconds
- **SC-002**: All matching scenarios (by name, by email, by mobile, no match) produce correct results as verified by checking the client database after processing
- **SC-003**: Invalid CSVs (missing headers, blank rows, missing fields) are rejected with a clear error message before any processing begins
- **SC-004**: The summary report accurately reflects the number of records processed, created, updated, and errors
- **SC-005**: Existing client data that is not included in the CSV update is preserved unchanged

## Assumptions

- The CSV file uses UTF-8 encoding (recommended) or other common encodings that can be detected automatically
- The CSV file size is reasonable for a web upload (up to 5 MB, corresponding to roughly 10,000+ rows)
- Duplicate name matches (multiple clients with the same first_name + last_name) are handled by matching the first found client
- Extra columns beyond the four defined headers are silently ignored
- The existing Operator role has permission to create and update clients
- The client model already has first_name, last_name, email, mobile, is_active, created_at, updated_at fields
