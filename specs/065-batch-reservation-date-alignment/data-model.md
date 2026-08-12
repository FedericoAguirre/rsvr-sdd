# Data Model: Batch Reservation Date Alignment

## Existing Domain Entities

### Payment

The payment record supplies the selected payment date and class-slot count used by the existing batch reservation window.

Relevant attributes:

- `date`: calendar date used as the payment-day candidate.
- `class_slot_count`: number of dates the user must select.
- `client`: reservation owner whose existing reservations constrain the window.
- `created_at`: timestamp used by the existing same-day cutoff rule.

### Reservation

An existing or newly created reservation for a client and calendar date.

Relevant attributes:

- `date`: exact calendar date selected by the user.
- `client`: owner used when finding reserved dates and conflicts.
- `class_slot`: active class slot whose weekday must match `date.weekday()`.

### ClassSlot

An active weekday/time combination available for reservation.

Relevant attributes:

- `day_of_week`: Monday-based weekday position from `0` through `6`.
- `time`: class time selected in the modal.
- `is_active`: whether the slot can be selected.

## Presentation View Model

The existing batch-data response is transformed in the browser into calendar-week display rows. This is not persisted data.

```text
BatchDateGrid
├── weekStart: ISO date for Monday
└── cells[0..4]
    ├── date: ISO date or empty
    ├── weekday: Monday-based position 0..4
    ├── reserved: boolean
    └── selectable: boolean
```

Rules:

1. `weekStart` is the Monday on or before the date being rendered.
2. A date is placed at `cells[date.weekday()]`, not at the next sequential array position.
3. Weekend dates remain outside the five-column weekday grid, matching current behavior.
4. Leading empty cells are rendered when the eligible range starts after Monday.
5. The button's `data-date` remains the original ISO date and is the value submitted.

## Validation and Relationships

- The existing payment-to-client relationship determines reserved dates returned by the batch-data endpoint.
- The selected class-slot time must have an active slot on each selected date's weekday.
- The existing form remains responsible for date parsing, count, duplicate, window, cutoff, and class-slot validation.
- No schema, field, relationship, or migration changes are required.
