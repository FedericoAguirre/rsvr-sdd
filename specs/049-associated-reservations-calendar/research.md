# Research: Associated Reservations Calendar Download

## Decisions

### ICS Generation Approach
- **Decision**: Reuse the existing `_generate_ics()` function from `apps/clients/views.py` (built for feature 021)
- **Rationale**: The function already handles VEVENT creation, timezone setup (America/Denver), and ICS formatting. Extracting to a shared utility avoids duplication.
- **Alternatives considered**: Rewrite from scratch in the payments app (duplication risk), inline generation in view (worse testability)

### Payment Identifier in Events
- **Decision**: Include the payment identifier as a "Pago" field in each VEVENT's DESCRIPTION, alongside client name, class slot, date, and equipment
- **Rationale**: FR-003 and FR-004 require the payment identifier in each event; appending to the existing DESCRIPTION text is the simplest approach
- **Alternatives considered**: Adding a separate X-CUSTOM field (less compatible with calendar apps), using SUMMARY prefix (clutters the event title)

### Filename Generation
- **Decision**: Format `<client_name>_<payment_identifier>_<first_date_YYYYMMDD>_<last_date_YYYYMMDD>.ics` with client name in snake_case
- **Rationale**: Matches FR-005 spec exactly; snake_case ensures ASCII-safe filenames
- **Alternatives considered**: Using hyphens instead of underscores (less consistent with existing 021 pattern `cal_<name>_<start>_<end>.ics`)

### Empty State Handling
- **Decision**: Show a user-facing message when the payment has no associated reservations; no file is generated
- **Rationale**: Consistent with US2 and the existing 021 pattern for empty ranges
- **Alternatives considered**: Generate an empty ICS file (confusing to users), redirect with error flash (existing pattern in 021)

### View Type
- **Decision**: Create a simple function-based view or a View subclass (not DetailView) that returns the ICS file as an attachment
- **Rationale**: No template rendering needed; the view directly returns an HttpResponse with `Content-Disposition: attachment`
- **Alternatives considered**: TemplateView (unnecessary), DetailView (adds template overhead)

### Button Placement
- **Decision**: Place "Descargar calendario" in the header actions area of the payment detail template, alongside "Asociar" and "Editar"
- **Rationale**: Consistent with the 021 pattern where the download button is in the action area; visible regardless of whether reservations exist
- **Alternatives considered**: Inside the reservations card header (hidden when no reservations), bottom of page (less discoverable)

### Timezone
- **Decision**: Use existing `America/Denver` VTIMEZONE from `_generate_ics()`
- **Rationale**: Already established and tested in the 021 feature; consistent across the application
- **Alternatives considered**: UTC-only (loses local time context), user-configurable (over-engineered for current scope)
