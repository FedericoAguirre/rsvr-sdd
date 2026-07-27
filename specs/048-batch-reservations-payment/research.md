# Research: Batch Reservations from Payment

## Decisions

### Modal Trigger
- **Decision**: Batch modal opens after successful payment creation via HTMX or JS-triggered modal on the same page
- **Rationale**: Existing project uses Django templates with Bootstrap; modal pattern fits existing UX
- **Alternatives considered**: Redirect to a separate batch page (too much context switching)

### Unique Constraint Handling
- **Decision**: Partial failure with per-date feedback; successfully created reservations are persisted, conflicts are reported
- **Rationale**: Minimizes data loss; operator can retry only the failed dates
- **Alternatives considered**: Full rollback (wasteful), pre-check all conflicts before creation (more complex)

### Client Assignment
- **Decision**: Each batch reservation inherits the client FK from the payment
- **Rationale**: The payment already has a client relationship; all reservations for block classes belong to that client
- **Alternatives considered**: Operator selects client in modal (unnecessary step)

### Date Range Calculation
- **Decision**: Start = next Monday after payment date; End = start + 28 days (~4 weeks); only DOW-matching dates shown based on selected class slot
- **Rationale**: Matches clarified requirement from spec and user story constraints
- **Alternatives considered**: Fixed calendar months, rolling 4-week window from today

### UI Interaction
- **Decision**: Class slot selection filters calendar to matching DOWs; operator ticks N dates from those shown; counter shows N/max progress
- **Rationale**: Enforces FR-004 (exactly N dates) and FR-014 (DOW matching) in a single flow
- **Alternatives considered**: Multi-select without DOW filtering (would create invalid reservations)
