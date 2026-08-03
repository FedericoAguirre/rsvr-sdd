# Feature Specification: Add ClassPrice Sub-Option Under "Horario" Menu

**Feature Branch**: `061-add-classprice-menu`

**Created**: 2026-08-02

**Status**: Draft

**Input**: User description: "As an operator I want to access to the ClassPrice webpage using the 'Horario' option in the menu. I want that option be shared with the ClassSlots too. So when clicking the Horario option there appears actual one plus the Precio (ClassPrice) one."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access ClassPrice via Horario Dropdown (Priority: P1)

As an operator with class management permissions, I want the "Horario" menu item to show a dropdown with two options — "Horario de Clases" (the existing schedule) and "Precios" (class price management) — so that I can navigate to both pages from a single menu entry.

**Why this priority**: This is the primary user need. ClassPrice currently has no menu entry; operators must know or bookmark the URL. Adding it under the "Horario" dropdown makes it discoverable.

**Independent Test**: Log in as a user with `classes.view_classslot` permission. Click "Horario" in the nav — a dropdown appears with two links: "Horario de Clases" and "Precios". Clicking each navigates to the correct page.

**Acceptance Scenarios**:

1. **Given** I am logged in with `classes.view_classslot` permission, **When** I click "Horario" in the navigation bar, **Then** a dropdown menu appears with options "Horario de Clases" and "Precios".
2. **Given** the dropdown is open, **When** I click "Horario de Clases", **Then** I navigate to the class schedule page (`/classes/`).
3. **Given** the dropdown is open, **When** I click "Precios", **Then** I navigate to the class price list page (`/classes/prices/`).

---

### User Story 2 - Menu Hides When No Permission (Priority: P2)

As a user without `classes.view_classslot` permission, I want the "Horario" menu item to remain hidden entirely, so that I don't see a menu option I can't use.

**Why this priority**: Existing behavior — the "Horario" item is already gated on `classes.view_classslot`. This must not regress.

**Independent Test**: Log in as a user without `classes.view_classslot` permission. The "Horario" menu item is not visible at all.

**Acceptance Scenarios**:

1. **Given** I am logged in without `classes.view_classslot` permission, **When** the page renders, **Then** the "Horario" menu item is not present in the navigation bar.

---

### Edge Cases

- What happens when the "Horario" dropdown is used on a mobile viewport? The dropdown must function correctly in the responsive nav (Bootstrap collapse).
- What happens with existing URL access? Direct access to `/classes/prices/` or `/classes/` continues to work regardless of the menu change.
- What happens if the ClassPrice page has no data? The menu link still works — the price list page handles the empty state (shows no prices with an "Add price" button for admins).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The "Horario" navigation item MUST become a dropdown menu containing two links: "Horario de Clases" (label: "Class Schedule") and "Precios" (label: "Class prices").
- **FR-002**: The "Horario de Clases" link MUST navigate to the existing class schedule page (`classes:class-schedule`, `/classes/`).
- **FR-003**: The "Precios" link MUST navigate to the existing class price list page (`classes:price-list`, `/classes/prices/`).
- **FR-004**: The entire "Horario" dropdown MUST remain gated on the `classes.view_classslot` permission — users without this permission see no "Horario" menu at all.
- **FR-005**: The dropdown MUST be styled consistently with the existing "Reportes" dropdown in the navigation bar.
- **FR-006**: Both dropdown links MUST use the internationalization system to render their labels in Spanish (and any future languages).
- **FR-007**: The dropdown MUST function correctly on both desktop and mobile viewports using Bootstrap's responsive navigation.

### Key Entities

- **ClassSlot**: Existing schedule entity (unchanged). The schedule page shows a table of class slots by day and time.
- **ClassPrice**: Existing price entity (unchanged). The price list page shows current and historical prices with an admin-only "Add price" button.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An operator can reach the ClassPrice page in one click from the "Horario" dropdown (vs. typing or bookmarking the URL).
- **SC-002**: The "Horario" menu item with the "Precios" option is context-appropriate — clicking either link navigates directly to the expected page with no intermediate steps.
- **SC-003**: All existing tests for class price and schedule views continue to pass.
- **SC-004**: The dropdown renders identically in style and behavior to the existing "Reportes" dropdown (Bootstrap nav dropdown pattern).
- **SC-005**: User-visible strings ("Class Schedule" and "Class prices") appear translated to Spanish when the locale is set to `es`.

## Assumptions

- The `class_schedule` view and `ClassPricesView` already work correctly and are accessible at their current URLs (`/classes/` and `/classes/prices/`).
- The existing "Reportes" dropdown pattern in `base.html` is the correct model for the new "Horario" dropdown (same Bootstrap classes, same structure).
- Operators who can view the schedule can also view class prices. There is no need for a separate permission gate on the "Precios" link — both links share the same `classes.view_classslot` permission.
- The change is purely a template/navigation update; no view, URL, model, or migration changes are needed.
- Spanish i18n translations for the dropdown labels already exist in the `.po` file (`"Class Schedule"` → `"Horario de Clases"`, `"Class prices"` → `"Precios de clase"`).

## Out of Scope

- No changes to the ClassPrice model, views, or forms.
- No changes to the ClassSlot schedule page or its template.
- No new permissions or access control logic.
- No changes to other menu items.
