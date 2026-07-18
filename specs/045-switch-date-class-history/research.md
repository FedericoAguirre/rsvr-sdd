# Research: Switch date and class block columns in history

**Created**: 2026-07-16

## Summary

No research required. The feature is a single-file template column reorder with no new dependencies, integrations, or technology choices.

## Decisions

- **Approach**: Reorder `<th>` and `<td>` elements in `client_detail.html` — same pattern as features 043 and 044
- **Rationale**: Minimal change, proven pattern, no side effects
- **Alternatives considered**: CSS-only column reorder via `order` property — rejected because it would not change DOM tab order and adds unnecessary complexity for a static layout

## Dependencies

None. The existing `{% translate %}` tags for "Date", "Class", and "Equipment" are already in place in the project locale.
