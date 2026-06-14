# Research: Add Climber Equipment Type

## Decisions

### New EQUIPMENT_TYPES option position

- **Decision**: Insert `("climber", _("Climber"))` as the **first** entry in the list
- **Rationale**: Django ModelForm renders the first choice as the default selected value in a Select widget when no initial value is provided. Placing "climber" first satisfies FR-002 (default selection).
- **Alternatives considered**:
  - Append at end with separate `default="climber"` on the model field — not needed since Django already uses the first choice as default
  - Keep alphabetical order — would not position "climber" first

### Db value for the new type

- **Decision**: `"climber"`
- **Rationale**: Matches existing naming convention (all lowercase, single word: "treadmill", "bike", "elliptical", "rower", "other")
- **Alternatives considered**: `"escaladora"` — rejected because the db value should be English for consistency with existing choices; the display label uses `_("Climber")` which gets translated to "Escaladora" via Django i18n

### Seed equipment naming

- **Decision**: E01–E30 (zero-padded to 2 digits)
- **Rationale**: Sequential format is clear for Operators, supports sorting by name (E01 < E02 < ... < E30)
- **Alternatives considered**:
  - C01–C30 — the "C" prefix is redundant since type is already "climber"
  - Esc01–Esc30 — verbose and inconsistent with gym naming conventions
  - Unpadded E1–E30 — text sorting would break (E10 < E2)

### Migration reversibility

- **Decision**: Reverse operation deletes climber equipment with names starting with "E"
- **Rationale**: Allows clean rollback without affecting other equipment records; matches the pattern used in `0002_seed_test_clients.py` for clients

## No unresolved items

All technical decisions were straightforward — no NEEDS CLARIFICATION markers were required.
