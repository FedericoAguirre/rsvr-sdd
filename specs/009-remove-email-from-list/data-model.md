# Data Model: Remove Email from Client Column

**Feature**: [spec.md](./spec.md)

## No Schema Changes

This feature modifies only the presentation layer. No database migrations, model changes, or new entities are required.

## Existing Entities (unchanged)

| Entity | Key Fields | Usage |
|--------|------------|-------|
| `Client` | `first_name`, `last_name`, `email`, `mobile` | Displayed in reservations list — only `first_name` and `last_name` will be rendered |
| `Reservation` | `client` (FK), `equipment` (FK), `class_slot` (FK), `date` | Template iterates `reservations` queryset |
