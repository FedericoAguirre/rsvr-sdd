# Implementation Plan: Batch Reservation Weekly Date Groups

**Branch**: `056-batch-reservation-weekly-groups` | **Date**: 2026-07-30 | **Spec**: `specs/056-batch-reservation-weekly-groups/spec.md`

**Input**: Feature specification from `specs/056-batch-reservation-weekly-groups/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

The batch reservation modal (`payment_detail.html?batch_modal=1`) currently renders 20 date buttons in a single `d-flex flex-wrap gap-2` row. This rework groups dates into 4 weekly rows (5 columns, Mon–Fri) with day-of-week headers, CSS grid layout, and 3-letter Spanish day abbreviations. Only the frontend JS rendering function `renderBatchForm()` and CSS need changes — no backend Python, models, tests, or URLs are modified.

## Technical Context

**Language/Version**: Python 3.12, Django 5.0.x

**Primary Dependencies**: Django 5.0.x, Bootstrap 5.3 (CDN)

**Storage**: PostgreSQL 16 (no changes)

**Testing**: pytest + pytest-django (existing batch tests must continue passing)

**Target Platform**: Linux server (Docker)

**Project Type**: Web application (Django templates + Bootstrap 5 + vanilla JS)

**Performance Goals**: N/A — visual-only change to client-side rendering

**Constraints**: 
- The date rendering is done by JS `renderBatchForm()` in `payment_detail.html`, not a Django template — all layout changes must happen in JS string concatenation
- The `toggleDate()` selection logic and `submitBatch()` submission must remain unchanged
- `DAY_ABBRS` changes from single-letter (`["L","M","X","J","V","S","D"]`) to 3-letter Spanish abbreviations (`["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]`)
- i18n: day labels must use `{% translate %}` via Django template-to-JS bridge (e.g., `data-*` attributes or `json_script` filter)

**Scale/Scope**: Single modal template; small business, <50 concurrent operators

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| **I. Code Quality** | All code must pass automated linting before merge. No dead/commented-out code. | ✅ Pass — only JS string changes; existing lint rules apply |
| **II. Testing Standards (NON-NEGOTIABLE)** | TDD mandatory. Tests must be written by user FIRST and fail before implementation. | 🔴 GATE — TDD requires failing tests before code. Existing batch tests (`test_payments_batch.py`) cover the modal data/submission flow. No existing test covers the weekly grid visual layout. A new test or user-defined acceptance test is needed. |
| **III. UX Consistency** | i18n NON-NEGOTIABLE — all user-visible strings must be internationalized. | ✅ Pass — day abbreviations must use `{% translate %}`. The 3-letter labels must be registered in `django.po` before the JS is written. |
| **IV. Performance** | Performance criteria defined before implementation. | ✅ Pass — no performance-sensitive code changed |
| **V. External Documentation** | Every library API call must be informed by current fetched docs. | ✅ Pass — Bootstrap 5.3 docs for grid/modal layout will be fetched via Context7 |

**Violation Justification**: None required — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/056-batch-reservation-weekly-groups/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command — NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── apps/payments/
│   └── templates/payments/
│       ├── payment_detail.html       # MODIFIED — JS renderBatchForm() + CSS <style> block
│       └── _batch_modal.html         # UNCHANGED — modal shell only
├── locale/es/LC_MESSAGES/
│   └── django.po                     # MODIFIED — add day-label translations
└── tests/
    └── test_payments_batch.py        # UNCHANGED — backend tests unaffected
```

**Structure Decision**: Single Django app (`payments`) — all changes isolated to one template file and one locale file.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations requiring justification.

---

## Phase 0: Outline & Research

### Research Tasks

| Unknown / Dependency | Research Question | Context |
|----------------------|-------------------|---------|
| Bootstrap 5.3 Grid Layout | What's the best approach for a 5-column CSS Grid within a Bootstrap modal using `grid-template-columns: repeat(5, 1fr)`? | The weekly grid needs 5 equal columns — use CSS Grid or Bootstrap's `.row-cols-5` |
| Bootstrap 5.3 Modal Body Scroll | How to prevent double scrollbars when modal body plus grid content exceeds available height? | The grid has 4 rows; want single scrollbar on modal |
| Bootstrap 5.3 `d-flex` / `gap` vs CSS Grid | Should we use CSS Grid (`.d-grid` with `grid-template-columns`) or Bootstrap's grid system (`.row-cols-5`) for the 5-column week layout? | Need 5 equal columns with day headers aligned |

### Expected Decisions from Research

1. **Layout approach**: CSS Grid (`.d-grid` with `grid-template-columns: repeat(5, 1fr)`) vs Bootstrap `.row > .col-*` pattern
2. **Day header alignment**: How to align column headers with date buttons
3. **Responsive breakpoints**: How the 5-column grid collapses on mobile/tablet

---

## Phase 1: Design & Contracts

### Data Model

No backend data model changes — the feature modifies only the client-side rendering of already-fetched date data.

### Interface Contracts

**UI Contract**: The batch modal dates div (`#dateList`) changes from a single flex-wrap row to a weekly grid structure:

```text
Current:
  <div id="dateList" class="d-flex flex-wrap gap-2">
    <button ...>L - 2026/01/15</button>... (20 buttons in one row)
  </div>

New:
  <div id="dateList" class="batch-date-grid">
    <!-- Week 1 -->
    <div class="week-header">
      <span class="day-label">Lun</span><span class="day-label">Mar</span>...
    </div>
    <div class="week-row">
      <button ...>15/1</button><button ...>16/1</button>...
    </div>
    <!-- Week 2...N -->
    <hr class="week-separator">
    <div class="week-header">...</div>
    <div class="week-row">...</div>
  </div>
```

**Invariants**:
- Button `data-date` and `data-dow` attributes preserved unchanged
- `toggleDate()` function operates identically
- `submitBatch()` receives the same date format
- Day abbreviations are localized (Spanish `django.po` entry added)

### Quickstart Validation Scenarios

See `quickstart.md` for the end-to-end validation guide covering:
1. Desktop: 4 rows × 5 columns with day headers, no double scrollbar
2. Selection: click toggles active state, count updates
3. Responsive: no horizontal overflow on mobile
4. Existing tests: `test_payments_batch.py` passes unchanged
