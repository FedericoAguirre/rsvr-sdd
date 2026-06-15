# Feature Specification: Translate English Tags into Spanish

**Feature Branch**: `011-translate-english-tags`

**Created**: 2026-06-15

**Status**: Draft

**Input**: User description: "Translate English tags into Spanish" (from `ai/features/todos/04_translate_english_tags.md`)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Spanish-speaking clients can search with fully localized UI (Priority: P1)

As a Spanish-speaking user of the client search feature, I want all labels, placeholders, messages, and navigation buttons on the search page to be in Spanish, so that I can use the search functionality naturally without needing to understand English.

**Why this priority**: The client search is a primary user-facing feature. English text in this flow creates a poor experience for Spanish-speaking users and is the most visible of the two endpoints.

**Independent Test**: Can be fully tested by navigating to the clients/search page and verifying that all 7 specified English strings appear in Spanish instead, without any English text remaining.

**Acceptance Scenarios**:

1. **Given** the clients/search page is loaded, **When** the search is idle, **Then** the placeholder text reads "Empiece a escribir para buscar clientes..." instead of "Start typing to search clients..."
2. **Given** the clients/search page, **When** a search is in progress, **Then** the loading indicator reads "Búsqueda..." instead of "Searching..."
3. **Given** the clients/search page, **When** the user clicks the search input, **Then** the placeholder reads "Buscar clientes..." instead of "Search clients..."
4. **Given** the clients/search page with active filters, **When** filters are displayed, **Then** the label reads "Filtrado por" instead of "Filtered by"
5. **Given** the clients/search page with no matching results, **When** the search completes, **Then** the message reads "Cliente NO ENCONTRADO" instead of "Client NOT FOUND"
6. **Given** the clients/search page with paginated results, **When** viewing the first page, **Then** the navigation button reads "Siguiente" instead of "Next"
7. **Given** the clients/search page on the last page of results, **When** viewing results, **Then** the navigation button reads "Último" instead of "Last"

---

### User Story 2 - Equipment admin page uses consistent Spanish terminology (Priority: P2)

As an admin user managing equipment, I want the equipment management page to use the Spanish word "equipo" consistently, so that all labels on the page are in the same language.

**Why this priority**: This endpoint already has mostly Spanish text; only the word "equipment" needs translation. The impact is smaller but still necessary for consistency.

**Independent Test**: Can be fully tested by navigating to admin/equipment/equipment/ and verifying that the word "equipment"/"EQUIPMENT" is replaced with "equipo"/"EQUIPO" in the two specified strings.

**Acceptance Scenarios**:

1. **Given** the equipment list page is loaded, **When** viewing the page, **Then** the modification prompt reads "Seleccione equipo a modificar" instead of "Seleccione equipment a modificar"
2. **Given** the equipment creation form, **When** viewing the page title or button, **Then** the label reads "AÑADIR EQUIPO" instead of "AÑADIR EQUIPMENT"

---

### Edge Cases

- What happens if a translated string is already present in the i18n files but with a different translation? Existing translations should be updated, not duplicated.
- What if some tags are dynamically generated via JavaScript and not covered by the standard i18n template tags? These require special handling to ensure they are still translated.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The clients/search page MUST display translated Spanish text for all 7 specified English tags
- **FR-002**: The admin/equipment/equipment/ page MUST display translated Spanish text for the 2 specified English tags
- **FR-003**: All translations MUST be added to the project's i18n/locale system so they can be managed centrally
- **FR-004**: Existing translations in the locale files MUST NOT be duplicated or corrupted when adding the new translations
- **FR-005**: Tags that appear in static templates MUST use the standard i18n mechanism consistent with the project's existing approach

### Key Entities *(include if feature involves data)*

- **Translation Entry**: A single translatable string and its Spanish equivalent, stored in the locale system (`.po`/`.mo` files) with a unique message ID
- **Locale File**: The container for all translation entries for the Spanish language, version-controlled and compiled for runtime use

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 9 specified English tags are no longer visible on their respective pages — only Spanish equivalents are shown
- **SC-002**: The i18n files compile without errors after adding the new translations
- **SC-003**: Existing functionality on both pages is unaffected — only text labels change
- **SC-004**: A reviewer can confirm the translations are accurate and contextually appropriate

## Assumptions

- The project already uses an internationalization (i18n) system for Spanish translations
- The translations are added to existing locale files rather than creating new ones
- "Filtered by" is a static label displayed before the filter criteria, not a format string with dynamic content
- The template files for both pages already exist and only need i18n marker updates, not structural changes
- The existing search, pagination, and equipment management functionality remains unchanged
