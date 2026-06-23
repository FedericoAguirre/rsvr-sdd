# Research: Remove Status Buttons from Reservation List

**Phase**: 0 (Outline & Research)
**Date**: 2026-06-22

## Summary

No research required. This feature is a pure UI removal with no technical unknowns:

- **Technology**: Django templates — deletion is trivial
- **Dependencies**: None affected
- **Integration**: No new integrations
- **Performance**: Removal-only, no regression possible
- **Security**: No security impact (buttons were UI-only, back-end view is preserved for detail page)

## Decisions

| Unknown | Decision | Rationale |
|---------|----------|-----------|
| How to handle view import | No change needed | `reservation_change_status` view is preserved for the detail page's forms |
| How to handle JS/CSS | No change needed | The `htmx:configRequest` event handler in `base.html` and Bootstrap are unaffected |
| Test strategy | Update existing tests | Remove assertions that check for button presence; verify detail-page tests still pass |
