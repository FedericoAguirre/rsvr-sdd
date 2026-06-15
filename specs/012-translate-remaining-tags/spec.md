# Feature Specification: Translate Remaining Tags into Spanish

**Feature Branch**: `012-translate-remaining-tags`

**Created**: 2026-06-15

**Status**: Draft

**Input**: User description: "Translate remaining English tags in clients/search: First, Previous, Created, Yes" (from `ai/features/todos/04a_translate_english_tags.md`)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Complete client search localization with remaining Spanish tags (Priority: P1)

As a Spanish-speaking user of the client search feature, I want the pagination controls, column headers, and status indicators to be in Spanish, so that the entire search interface is consistently localized.

**Why this priority**: This is a single endpoint with 4 remaining English tags. They complete the localization work started in feature 011, making the clients/search page fully Spanish.

**Independent Test**: Can be fully tested by navigating to the clients/search page and verifying that "First", "Previous", "Created", and "Yes" appear in their Spanish equivalents.

**Acceptance Scenarios**:

1. **Given** the clients/search page with paginated results, **When** viewing the pagination controls, **Then** the first-page button reads "Primero" instead of "First"
2. **Given** the clients/search page with paginated results, **When** viewing the pagination controls, **Then** the previous-page button reads "Anterior" instead of "Previous"
3. **Given** the clients/search page with a list of clients, **When** viewing the table headers, **Then** the creation date column header reads "Creado" instead of "Created"
4. **Given** the clients/search page with active/inactive clients, **When** viewing the status column, **Then** the active indicator shows "Sí" instead of "Yes"

---

### Edge Cases

- What if "First" or "Previous" are already translated in the PO file from a different context? Ensure the new translation is consistent with existing pagination terminology (e.g., "Next" → "Siguiente", "Last" → "Último" from feature 011).
- What if "Yes" appears in contexts other than the active status column? The `yesno` filter string "Yes,No" should be translated as a single unit.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The pagination "First" button on clients/search MUST display "Primero" in Spanish
- **FR-002**: The pagination "Previous" button on clients/search MUST display "Anterior" in Spanish
- **FR-003**: The "Created" column header on clients/search MUST display "Creado" in Spanish
- **FR-004**: The active status indicator "Yes" on clients/search MUST display "Sí" in Spanish
- **FR-005**: All translations MUST be added to the project's i18n/locale system, consistent with existing entries
- **FR-006**: Existing pagination translations ("Next" → "Siguiente", "Last" → "Último") MUST NOT be affected

### Key Entities *(include if feature involves data)*

- **Translation Entry**: A single translatable string and its Spanish equivalent, stored in the locale system (`.po`/`.mo` files) with a unique message ID

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 4 specified English tags are no longer visible on the clients/search page — only Spanish equivalents are shown
- **SC-002**: The i18n files compile without errors after adding the new translations
- **SC-003**: Existing pagination translations remain intact and functional

## Assumptions

- The `_search_results.html` template already uses `{% translate %}` for "First", "Previous", "Created", and the `yesno` filter for "Yes,No" — no template changes needed
- The PO file already exists and only needs new entries added
- "Created" as a column header is different from the existing "Created at" entry and needs its own translation
- The `yesno` filter string is `"Yes,No"` and should be translated as a single msgid entry
