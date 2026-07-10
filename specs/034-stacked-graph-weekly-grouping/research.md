# Research: Stacked Graph Weekly Grouping

**Phase 0 — all Technical Context items already resolved from existing daily chart implementation.**

## Decisions

### Date Snapping Logic

- **Decision**: Use Python `datetime.date.weekday()` (Monday=0, Sunday=6) in `PaymentReportView.get_context_data()`. Before building the query, snap `start` to closest preceding Monday (`start -= timedelta(days=start.weekday())`) and `end` to closest following Sunday (`end += timedelta(days=6 - end.weekday())`).
- **Rationale**: Pure Python approach — no extra DB calls, no SQL dependency. Matches existing view pattern.
- **Alternatives considered**: PostgreSQL `date_trunc('week', date)` on the input dates, but that would require raw SQL; Python approach is cleaner and more testable.

### Chart.js Weekly Config

- **Decision**: Reuse the existing stacked bar config from the daily grouping. The x-axis `type: 'category'` switches to weekly labels in YYYYMMDD format. Tooltip formatting stays identical (payment type, total, count). Datasets structure is identical — just different date granularity.
- **Rationale**: No new Chart.js features needed. Category axis with weekly labels works with the same `report_data` JSON structure from the backend.
- **Alternatives considered**: Time axis with `time.unit: 'week'` would require the `chartjs-adapter` plugin — rejected per zero-new-libraries constraint.

### i18n for Error Message

- **Decision**: Add new i18n key for "Failed to load chart data." following the existing convention in the Django locale files.
- **Rationale**: Mandated by constitution's i18n requirement.
- **Alternatives considered**: Reusing an existing generic error key — none match the chart-specific context.

### Backend Query for Week Grouping

- **Decision**: Keep the existing `qs.extra(select={"week": "date_trunc('week', date)::date"})` approach. PostgreSQL `date_trunc('week', ...)` returns ISO weeks starting on Monday — compatible with the feature requirements.
- **Rationale**: Already working, no change needed. Date snapping happens before the query runs.
- **Alternatives considered**: Using `TruncWeek` from `django.db.models.functions` — extra() works fine and is already deployed.
