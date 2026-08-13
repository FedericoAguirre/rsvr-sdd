# Data Model: Payment Receipt Export

## Existing Entities

### Payment

- `id`: unique primary key; fallback filename reference when `reference` is empty.
- `client`: required relationship to the receipt client.
- `amount`: total monetary amount.
- `payment_type`: translated display value for the payment method.
- `payment_identifier`: existing stable payment identifier used as the receipt reference in the current application.
- `date`: payment date, displayed according to the active locale; reservation rows use `DD/MM/YYYY` as required.
- `class_slot_count`: number of class slots purchased.
- `reference`: optional external reference; use this when populated for the filename reference, otherwise use `id`.
- `is_deleted`: existing soft-delete state; receipt retrieval must use the same visibility rule as the payment detail view.

### Client

- `first_name`, `last_name`: display name and filename source.
- Relationship: one client has many payments and reservations; the receipt uses the payment’s client only.

### PaymentReservation

- `payment`: relationship to one Payment.
- `reservation`: one-to-one relationship to one Reservation.
- Relationship: this join identifies exactly the reservations included in a receipt.

### Reservation

- `class_slot`: class-slot label/time shown in the table.
- `date`: class date shown as `DD/MM/YYYY`.
- `equipment`: equipment name or a localized empty value when unavailable.
- `status`: translated reservation status.
- Relationship: each included reservation is linked to the selected payment through PaymentReservation.

## Derived Receipt Projection

The receipt module should construct a non-persistent projection with:

- localized field labels and empty-state text
- client display name
- amount display value
- translated payment type
- localized payment date
- class-slot count
- payment reference for display
- sanitized filename client component and reference component
- ordered reservation rows: class slot, date, equipment, status
- `has_reservations` flag

## Validation and Invariants

- The projection is created for one requested payment only.
- Reservation rows come only from `payment.payment_reservations` and are ordered consistently by reservation date and class-slot time.
- A zero-row projection is valid and renders the localized no-reservations message.
- Filename output begins with `payment_`, ends with `.pdf`, preserves accented letters, replaces spaces/unsafe characters with underscores, and uses payment ID if the optional reference is missing.
- No schema migration or new persistent entity is required.
