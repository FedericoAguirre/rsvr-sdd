# Feature Specification: Remove ClassPrice-ClassSlot Association

**Feature Branch**: `059-remove-classslot-association`

**Created**: 2026-08-02

**Status**: Draft

**Input**: User description: "Remove the ClassSlot association from the ClassPrice, because they not related by business rules yet. Adjust all the assets as needed"

## User Scenarios & Testing *(mandatory)*

**Note**: This is a refactoring feature that removes a premature data association. There are no new user-facing capabilities; the goal is to correct the data model so it matches current business rules, and ensure all existing functionality continues to work in the decoupled form.

### User Story 1 - Price Records Are Decoupled From Class Slots (Priority: P1)

As a system administrator, when the ClassPrice model is adjusted to remove the `class_slot` association, all existing price management functionality must continue to work correctly in a decoupled form, so that price records exist as standalone entities until the business relationship between classes and prices is formally established.

**Why this priority**: The current `ClassPrice` model has a `class_slot` ForeignKey that does not reflect an actual business relationship. Keeping it would force premature coupling and create a misleading data model. Removing it ensures the model is correct for the current domain state.

**Independent Test**: After the change, the `ClassPrice` model has no `class_slot` field. All existing tests for price creation, versioning, history, and deletion prevention pass. The admin interface for ClassPrice works (read-only, no delete). No orphaned references to `class_slot` exist anywhere in the codebase.

**Acceptance Scenarios**:

1. **Given** the `ClassPrice` model, **When** the `class_slot` field is removed, **Then** the model has no `class_slot` attribute and no migration references it.
2. **Given** the existing price management code, **When** the `class_slot` association is removed, **Then** all views, templates, forms, URLs, and tests are updated to function without a class-slot context and no errors occur.
3. **Given** a price record that was previously associated with a class slot, **When** the association is removed, **Then** the price record retains its versioning and audit fields (`price`, `current`, `created_by`, `created_at`, `changed_at`, `changed_by`, `updated_at`) and can be managed standalone.

---

### Edge Cases

- What happens to the filtered `UniqueConstraint` on `class_slot` + `current=True`? The constraint is removed since there is no longer a per-class current price concept. The single-current guarantee must be re-evaluated — with standalone prices, "current" may become a manual flag or be removed entirely.
- What happens to the `ClassPricesView` and `ClassPriceCreateView` that took a `class_slot` pk from the URL? These must be reworked to list/create all prices without a class context.
- What happens to the "Prices" link added to the schedule page? It must be removed since prices are no longer per-class.
- What happens to the migration that created `ClassPrice` with `class_slot`? A new migration must remove the `class_slot` field, and the filtered unique constraint must be dropped.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `ClassPrice` model MUST NOT have a `class_slot` ForeignKey field.
- **FR-002**: The `ClassPrice` model MUST retain its versioning fields: `price`, `current`, `created_by`, `created_at`, `changed_at`, `changed_by`, `updated_at`.
- **FR-003**: The `ClassPrice` model MUST retain its deletion prevention (overridden `delete()`, queryset `delete()` raise, admin `has_delete_permission=False`).
- **FR-004**: A database migration MUST exist to remove the `class_slot` field and its associated filtered unique constraint.
- **FR-005**: The `ClassPriceAdmin` MUST be updated to remove `class_slot` from any form/layout/admin display.
- **FR-006**: The `enter_price` service method MUST be reworked to not require a `class_slot` parameter — it must operate on standalone prices with no per-class current constraint.
- **FR-007**: Views, forms, templates, and URLs that referenced `class_slot` MUST be updated or removed so no runtime errors occur.
- **FR-008**: The "Prices" link on the schedule page MUST be removed since prices are no longer tied to class slots.
- **FR-009**: All tests MUST pass after the removal with no references to `class_slot` in ClassPrice.
- **FR-010**: All new or remaining user-visible strings MUST be internationalized (i18n) and verified in Spanish per Constitution Principle III.

### Key Entities *(include if feature involves data)*

- **ClassPrice**: A versioned price record with `price` (Decimal), `current` (Boolean), `created_by`/`changed_by` (FK to User), `created_at`/`changed_at`/`updated_at` (DateTime). No longer associated with any class slot. Price records are immutable in their amount after creation and cannot be deleted.
- **ClassSlot**: The existing weekly class schedule block. No longer referenced by `ClassPrice`.
- **User**: The administrator who creates or retires a price. Referenced via `created_by` and `changed_by`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The `ClassPrice` model has zero ForeignKey relationships to `ClassSlot` — verifiable by introspection.
- **SC-002**: All existing tests (321) pass after the change with no failures or errors.
- **SC-003**: The database migration applies cleanly and removes the `class_slot` column and the `unique_current_classprice_per_slot` constraint.
- **SC-004**: No reference to `class_slot` in any `ClassPrice`-related code path (models, views, forms, templates, URLs, admin) remains.
- **SC-005**: All new and remaining user-visible strings in the updated code are internationalized and have verified Spanish translations.

## Assumptions

- The `ClassPrice` entity is retained as a standalone price record for future use; it is not deleted entirely.
- The `current` flag semantics are retained (marking the active price), but without a per-class constraint, multiple current prices may exist across the system.
- The `enter_price` service is reworked to create standalone current prices without atomic retire-and-swap of a per-class previous price.
- Spanish i18n translations are the project's target language for all user-facing strings.
- The existing test suite provides regression coverage for the deletion prevention feature.

## Out of Scope

- No new user-facing pricing features are added; this is a model refactoring only.
- No changes to the `ClassSlot`, `Payment`, `Reservation`, or `Client` models.
- No changes to the production data beyond the migration to drop the `class_slot` column.

## Future Enhancements

- Re-establish the ClassPrice-ClassSlot relationship once the business rules formally define it.
- Re-introduce the per-class single-current price constraint when the association returns.
- Add price categorization or naming when prices become standalone entities with distinct identities.
