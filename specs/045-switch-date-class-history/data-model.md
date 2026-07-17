# Data Model: Switch date and class block columns in history

**Created**: 2026-07-16

## Overview

No new entities, attributes, or relationships are introduced. This feature is a presentation-layer change only.

## Existing Entities (unaffected)

| Entity | Notes |
|--------|-------|
| Client | No changes |
| Reservation | No changes |
| ClassSlot | No changes |
| Equipment | No changes |

## Data Flow

No data transformation, validation, or persistence changes. The existing queryset feeding the reservation history table is unmodified — only the column rendering order in the template changes.
