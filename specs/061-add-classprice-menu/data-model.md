# Data Model: Add ClassPrice Sub-Option Under "Horario" Menu

No data model changes. This feature is a navigation template update only.

## Affected Entities (Unchanged)

| Entity | Purpose | Notes |
|--------|---------|-------|
| ClassSlot | Weekly class schedule | Accessed via `/classes/` (schedule page). Unchanged. |
| ClassPrice | Versioned price records | Accessed via `/classes/prices/` (price list). Unchanged. |
| Permission (`view_classslot`) | Permission gate for class navigation | Used to control visibility of the "Horario" dropdown. Unchanged. |

## Navigation Structure (Changed)

**Before**:
```
Horario → [flat link] → /classes/ (schedule)
```

**After**:
```
Horario ─┬─ Horario de Clases → /classes/ (schedule)
         └─ Precios           → /classes/prices/ (price list)
```

No database migration, no model field changes, no URL changes.
