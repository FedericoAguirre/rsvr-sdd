# Feature Specification: Spanish Labels Translation

**Feature Branch**: `003-labels-to-spanish`

**Created**: 2026-03-19

**Status**: Draft

**Input**: User description: "I want to translate the application labels into Spanish and keep the code written in English"

## User Scenarios & Testing

### User Story 1 - Navigate the application in Spanish (Priority: P1)

A Spanish-speaking gym staff member opens the application and sees all navigation elements, page titles, and headings in Spanish, allowing them to understand and navigate the system without English proficiency.

**Why this priority**: Navigation is the entry point to every feature — without Spanish labels, a Spanish-speaking user cannot effectively use the application at all.

**Independent Test**: Can be fully tested by loading each page and verifying that the browser title, navbar brand, nav links, and page headings display in Spanish, and delivers the value of basic application orientation in the user's language.

**Acceptance Scenarios**:

1. **Given** a staff member loads any page, **When** the page renders, **Then** the navbar brand displays "Reserva de Cardio" and nav links display as "reservaciones", "Clientes", "Equipos", "Horario", "Admin", "Cerrar sesión"
2. **Given** a staff member navigates to the equipment list, **When** the page loads, **Then** the page title and heading display as "Equipos"
3. **Given** a staff member navigates to the reservations list, **When** the page loads, **Then** the page title and heading display as "Reservaciones"
4. **Given** a staff member navigates to the client search, **When** the page loads, **Then** the page title and heading display as "Buscar Clientes"
5. **Given** a staff member navigates to the class schedule, **When** the page loads, **Then** the page title and heading display as "Horario de Clases"

---

### User Story 2 - Manage equipment inventory in Spanish (Priority: P1)

A Spanish-speaking staff member uses the equipment management pages (list, detail, add, edit) with all labels, form fields, buttons, and status indicators displayed in Spanish.

**Why this priority**: Equipment management is a core workflow of the application — all CRUD interactions must be understandable in Spanish.

**Independent Test**: Can be fully tested by creating, viewing, editing, and listing equipment items and verifying all labels, buttons, table headers, and form fields display in Spanish, and delivers the value of complete equipment management in the user's language.

**Acceptance Scenarios**:

1. **Given** a staff member views the equipment list, **When** the page renders, **Then** table headers display "Nombre", "Tipo", "Estado"
2. **Given** a staff member views the equipment list, **When** the page renders, **Then** action buttons display "Ver", "Editar", "Agregar Equipo"
3. **Given** a staff member views the equipment detail page, **When** the page renders, **Then** labels display "Tipo", "Estado", "Notas"
4. **Given** a staff member opens the add equipment form, **When** the page renders, **Then** the heading displays "Agregar Equipo" and the submit button displays "Guardar"
5. **Given** a staff member views equipment type choices, **When** the field renders, **Then** options display as "Cinta de correr", "Bicicleta estacionaria", "Elíptica", "Máquina de remo", "Otro"
6. **Given** a staff member views equipment status, **When** the field renders, **Then** options display as "En servicio", "Fuera de servicio"

---

### User Story 3 - Manage reservations in Spanish (Priority: P1)

A Spanish-speaking staff member handles reservation creation, listing, and detail views with all labels, form fields, messages, and empty states in Spanish.

**Why this priority**: Reservation management is the primary purpose of the application and must be accessible in the user's language.

**Independent Test**: Can be fully tested by creating, listing, and viewing reservations and verifying all labels, buttons, table headers, form fields, success messages, and empty states display in Spanish, and delivers the value of complete reservation management in Spanish.

**Acceptance Scenarios**:

1. **Given** a staff member views the reservations list, **When** the page renders, **Then** table headers display "Fecha", "Cliente", "Clase", "Equipo"
2. **Given** the reservations list is empty, **When** the page renders, **Then** the empty state displays "No se encontraron reservaciones."
3. **Given** a staff member creates a new reservation, **When** the form renders, **Then** the heading displays "Nueva Reserva" and the submit button displays "Crear Reserva"
4. **Given** a staff member views a reservation detail, **When** the page renders, **Then** labels display "Cliente", "Equipo", "Clase", "Fecha", "Creado por", "Notas"
5. **Given** a staff member creates a reservation, **When** the request succeeds, **Then** the success message displays "Reserva creada."
6. **Given** a staff member views the reservation list, **When** the page renders, **Then** the filter button displays "Filtrar"

---

### User Story 4 - Search and manage clients in Spanish (Priority: P2)

A Spanish-speaking staff member searches for clients, views client details, and creates new clients with all labels in Spanish.

**Why this priority**: Client management is important but primarily involves searching existing records, which is partially functional even with English labels.

**Independent Test**: Can be fully tested by searching, viewing, and creating clients and verifying all labels, form fields, button text, table headers, and empty states display in Spanish.

**Acceptance Scenarios**:

1. **Given** a staff member opens the client search page, **When** the page renders, **Then** the heading displays "Buscar Clientes" and the submit button displays "Buscar"
2. **Given** a staff member views search results, **When** the page renders, **Then** table headers display "Nombre", "Correo electrónico", "Móvil"
3. **Given** no clients match a search, **When** the page renders, **Then** the empty state displays "No se encontraron clientes."
4. **Given** a staff member opens the new client form, **When** the page renders, **Then** the heading displays "Nuevo Cliente" and the submit button displays "Guardar"
5. **Given** a staff member creates a new client, **When** the request succeeds, **Then** the success message displays "Cliente {client} creado."
6. **Given** a staff member views a client detail page, **When** the page renders, **Then** labels display "Correo electrónico", "Móvil", "Historial de reservaciones"
7. **Given** a staff member views a client with no reservations, **When** the page renders, **Then** the empty state displays "Sin reservaciones aún."

---

### User Story 5 - View class schedule in Spanish (Priority: P2)

A Spanish-speaking staff member views the weekly class schedule with days, times, statuses, and action buttons in Spanish.

**Why this priority**: The class schedule is a daily reference tool — Spanish labels improve comprehension but the schedule is still usable with English labels and numeric times.

**Independent Test**: Can be fully tested by loading the class schedule page and verifying that table headers, day names, status badges, and toggle buttons display in Spanish.

**Acceptance Scenarios**:

1. **Given** a staff member views the class schedule, **When** the page renders, **Then** table headers display "Día", "Hora", "Estado"
2. **Given** a staff member views the class schedule, **When** the page renders, **Then** day names display as "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"
3. **Given** a staff member views the class schedule, **When** an active slot renders, **Then** the status badge displays "Activo" and the toggle button displays "Desactivar"
4. **Given** a staff member views the class schedule, **When** an inactive slot renders, **Then** the status badge displays "Inactivo" and the toggle button displays "Activar"
5. **Given** a staff member activates a class slot, **When** the request succeeds, **Then** the success message displays "Bloque de clase {slot} activado."
6. **Given** a staff member deactivates a class slot, **When** the request succeeds, **Then** the success message displays "Bloque de clase {slot} desactivado."

---

### Edge Cases

- What happens when a translation is missing for a specific string? Django falls back to the English source string, preserving application functionality
- How does the system handle dynamic content embedded in strings (e.g., `"Reservation #{{ pk }}"`)? The Spanish translation template retains the variable placeholder and translates only the surrounding text
- How are model `__str__` representations handled when used in templates and admin? They are translated via `gettext` in the model's `__str__` method, ensuring consistency everywhere the model is displayed
- What happens when new features are added with English labels? Untranslated strings automatically fall back to English via Django's i18n fallback mechanism, no application errors occur
- How does seed data output behave? CLI management command messages are translated to Spanish since the seed data is used by Spanish-speaking developers/staff

## Requirements

### Functional Requirements

- **FR-001**: System MUST use Django's built-in internationalization (i18n) framework (`gettext` / `gettext_lazy`) to implement all translations
- **FR-002**: All navigation elements (navbar brand, nav links, logout button) MUST display in Spanish
- **FR-003**: All page titles (`<title>`) and page headings (`<h1>`) MUST display in Spanish
- **FR-004**: All form labels, submit button text, and cancel/back links MUST display in Spanish
- **FR-005**: All table headers and column labels across all pages MUST display in Spanish
- **FR-006**: Model choice field labels (equipment types, equipment status, day of week) MUST display in Spanish
- **FR-007**: All success messages and flash notifications MUST display in Spanish
- **FR-008**: All empty state messages ("No reservations found", "No clients found", etc.) MUST display in Spanish
- **FR-009**: All action button text (View, Edit, Save, Cancel, Back, Search, Filter, etc.) MUST display in Spanish
- **FR-010**: Equipment detail labels (Type, Status, Notes) MUST display in Spanish
- **FR-011**: Reservation detail labels and the page title MUST display in Spanish
- **FR-012**: Client search form label and placeholder MUST display in Spanish
- **FR-013**: Client detail labels and reservation history heading MUST display in Spanish
- **FR-014**: Class schedule status badges (Active/Inactive) and toggle buttons (Activate/Deactivate) MUST display in Spanish
- **FR-015**: HTML `lang` attribute MUST be set to `es`
- **FR-016**: Model `__str__` representations that contain user-facing text MUST be translated and display in Spanish
- **FR-017**: Date/time formats in the user interface MUST follow Spanish locale conventions (dd/mm/yyyy)
- **FR-018**: Source code (variable names, function names, class names, comments, docstrings) MUST remain in English
- **FR-019**: Django admin interface MAY remain in English (uses Django's built-in admin translations)
- **FR-020**: Locale files (.po/.mo) MUST be compiled and included in the deployment so translations work in production
- **FR-021**: Translation files MUST be organized per Django conventions under a `locale/` directory with the appropriate language code

### Key Entities

- **Translation Entry**: A single key-value mapping between an English source string and its Spanish equivalent, stored in a `.po` file
- **Locale Directory**: The filesystem directory (`locale/es/LC_MESSAGES/`) containing compiled translation files for the Spanish language
- **Message File (`.po`)**: The human-readable source file containing all translation entries for the application

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of existing user-facing strings in the main application (templates + Python views + models + forms, excluding Django admin) are translated to Spanish and display correctly
- **SC-002**: Application navigation, form submission, and all CRUD operations function identically before and after translation, with zero functional regressions
- **SC-003**: Any untranslated string gracefully falls back to English via Django's i18n fallback mechanism, with no application errors or blank labels
- **SC-004**: New translations can be added by editing `.po` files and running the compile step, without modifying any Python or template source code
- **SC-005**: The application has been tested on every page/view (equipment list, equipment detail, equipment form, reservation list, reservation form, reservation detail, client search, client detail, client form, class schedule) and all visible text is verified in Spanish
- **SC-006**: Date and time values displayed in the UI follow dd/mm/yyyy convention, consistent with Spanish locale expectations

## Assumptions

- Target language is Spanish (es) — Latin American Spanish (es-mx) conventions are used where regional variants exist, but the locale code `es` covers the broadest audience
- The Django admin interface is excluded from translation; Django's built-in admin translations provide Spanish where available
- All existing user-facing strings will be translated in one pass; no incremental/staged rollout
- The Django i18n framework will be configured with `LocaleMiddleware`, `LOCALE_PATHS`, and `LANGUAGES` settings properly enabled
- The `USE_I18N = True` setting already exists and will be supplemented with the additional configuration needed
- Seed data CLI output messages will be translated; this is internal tooling but benefits Spanish-speaking operators
- The `html` `lang` attribute will be updated from `en` to `es` in the base template
- Django's `$ django-admin makemessages` and `$ django-admin compilemessages` commands will be used to manage translation files
