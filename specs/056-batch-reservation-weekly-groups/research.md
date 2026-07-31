# Research: Batch Reservation Weekly Date Groups

## Overview

Research findings for organizing the batch reservation modal date display into weekly groups. Three technology choices were evaluated.

---

## Decision 1: Grid Layout Approach

**Decision**: Plain CSS `display: grid; grid-template-columns: repeat(5, 1fr);`

**Rationale**:
- Bootstrap's built-in CSS Grid system (`.grid`, `--bs-columns`) requires Sass recompilation with `$enable-cssgrid: true` — not available with CDN Bootstrap
- Bootstrap's flexbox grid (`.row > .col-*`) lacks a native 5-column class (only `.row-cols-5` works at the row level but doesn't align column headers with data cells)
- Plain CSS Grid gives exact control over 5 equal columns with day headers and date buttons aligned
- Inline `<style>` block in `payment_detail.html` avoids external CSS files and keeps the change scoped

**Alternatives considered**:
| Alternative | Rejected because |
|-------------|-----------------|
| Bootstrap CSS Grid (`.grid`, `--bs-columns`) | Requires Sass recompilation; not available via CDN |
| Bootstrap `.row-cols-5` | Aligns children but doesn't solve header+data alignment across multiple rows |
| Flexbox with `flex: 0 0 20%` | Requires manual calc per child; harder to maintain alignment |

---

## Decision 2: Modal Scrolling

**Decision**: Use Bootstrap's `.modal-dialog-scrollable` on the existing `.modal-dialog` element in `_batch_modal.html`

**Rationale**:
- The modal already uses `modal-lg`; adding `modal-dialog-scrollable` enables internal scrolling of the `.modal-body` without double scrollbars
- The grid of 4 weeks × 5 buttons plus headers may exceed the modal's available height on smaller viewports

**Implementation**: Change `<div class="modal-dialog modal-lg">` to `<div class="modal-dialog modal-lg modal-dialog-scrollable">`

---

## Decision 3: Date Format in Buttons

**Decision**: Change from `"L - 2026/01/15"` to `"15/1"` (short day/month format, no leading zero for month)

**Rationale**:
- Day-of-week is now conveyed by the column header (Lun, Mar, etc.) — no need to repeat the single-letter abbreviation in each button
- Short format reduces button width, allowing the 5-column grid to fit comfortably in the modal
- Consistent with the spec's goal of clean, scannable date display

**Alternatives considered**:
- Keep `"L - 2026/01/15"` — redundant with column headers; too wide for 5-column grid
- Full date `"15/01/2026"` — too wide for 5 columns

---

## Decision 4: Day Abbreviations

**Decision**: Use 3-letter Spanish abbreviations: Lun, Mar, Mié, Jue, Vie, Sáb, Dom

**Rationale**:
- Current `DAY_ABBRS` uses single letters: ["L", "M", "X", "J", "V", "S", "D"] — ambiguous (e.g., "M" could be Monday or Wednesday)
- 3-letter abbreviations are the standard Spanish short form
- Must use `{% translate %}` via Django `json_script` filter for i18n compliance

**Implementation**: Pass day abbreviations through Django template:
```html
{{ DAY_ABBRS|json_script:"dayAbrrs" }}
```
Then read from `JSON.parse(document.getElementById("dayAbrrs").textContent)` in JS.

---

## Decision 5: Week Separation

**Decision**: Use an `<hr>` between week groups with visual spacing via CSS

**Rationale**:
- Simple, semantic HTML element
- Can be styled with reduced opacity, margin, and no border
- No additional wrapper elements needed

---

## Decision 6: Responsive Behavior

**Decision**: Maintain 5-column grid on all breakpoints; allow modal content to scroll vertically on smaller screens

**Rationale**:
- The 5-column layout with short date labels ("15/1") fits within the modal's padding at 375px width
- `.modal-dialog-scrollable` handles vertical overflow on any viewport height
- No CSS `@media` overrides needed for the grid itself — only the modal container needs responsive adjustment

---

## References

- Bootstrap 5.3 Modal: `.modal-dialog-scrollable` for internal content scrolling
- Bootstrap 5.3 CSS Grid: Requires Sass recompilation (`$enable-cssgrid: true`) — not available via CDN
- Bootstrap 5.3 Grid inside modals: Nest `.container-fluid` in `.modal-body` for standard grid classes
