<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan at
`specs/021-send-class-calendar/plan.md`
<!-- SPECKIT END -->

## Session Summary (2026-06-22)

This session is on branch **021-send-class-calendar** — see `specs/021-send-class-calendar/plan.md`.

## Session Summary (2026-06-22)

### Completed
- Added `status_badge_class` and `status_label` template filters in `reservation_extras.py`
- Created `reservation_row.html` partial for HTMX row swap
- Added status badge rendering + inline action buttons ("Used"/"Unused") to reservation list templates
- Modified `reservation_change_status` view to return HTMX partial response with `HX-Trigger`
- Added JSON body fallback for `hx-vals` sent as `application/json`
- 11 tests written, all 102 passing

### CSRF Fix (the bug)
Root cause: `django.template.context_processors.csrf` was **missing** from `TEMPLATES.OPTIONS.context_processors` in settings.py, so `{{ csrf_token }}` rendered as empty. Additionally, HTMX 2.x's `hx-include` scopes CSS selectors to the button's **descendants only** — the CSRF `<input>` was never found.

**Fix**: Added a `<script>` in `base.html` that reads the `csrftoken` cookie and sets `X-CSRFToken` header on all HTMX requests via `htmx:configRequest` event — the standard recommended pattern for HTMX + Django.

### Key Decisions
- All HTMX CSRF handling is now in one place (JS in `base.html`) — no `hx-headers`/`hx-include` on individual buttons
- The view's JSON body fallback was kept as defensive measure for edge cases
