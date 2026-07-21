# Data Model: Batch Reservations from Payment

## Entities

### Payment (existing — no changes)
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | PK |
| client | ForeignKey(Client) | The client this payment is for |
| amount | Decimal | Payment amount |
| payment_type | CharField | cash / credit_card / debit_card / transfer / payments_app |
| date | Date | Date the payment was recorded |
| class_slot_count | PositiveIntegerField | Number of block classes paid (= N, the batch size) |

### PaymentReservation (existing — no changes)
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | PK |
| payment | ForeignKey(Payment) | FK to payment |
| reservation | OneToOneField(Reservation) | Unique — each reservation linked to at most one payment |
| **Unique constraint**: payment + reservation |

### Reservation (existing — no changes)
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField | PK |
| client | ForeignKey(Client) | Inherited from payment during batch creation |
| equipment | ForeignKey(Equipment) | Selected by operator in modal |
| class_slot | ForeignKey(ClassSlot) | Selected by operator in modal; DOW must match date's DOW |
| date | Date | Must be within the allowed range and DOW match class_slot |
| status | CharField | reserved / used / unused |
| **Unique constraint**: equipment + class_slot + date |

### BatchReservationForm (new — transient, not a model)
A Django form that validates:
- `equipment` — must be "in service"
- `class_slot` — must be active
- `dates` — list of exactly N Date values where:
  - Each date is within the allowed range (next Monday + 28 days)
  - Each date's DOW matches class_slot's DOW
  - No duplicate dates
  - No conflicts with existing Reservation unique constraints

## Relationships

```
Payment (1) ──< PaymentReservation >── (1) Reservation
                                      │
                                      ├── (1) Equipment
                                      ├── (1) ClassSlot
                                      └── (1) Client  (inherited from Payment)
```

## State Transitions

- **Modal opens** → no reservations created yet
- **Operator selects equipment + class_slot + N dates** → form validated
- **Submit** → N Reservation + N PaymentReservation records created in a transaction
- **Partial conflict** → successfully created records persist; failed dates reported to operator
- **Modal closed** (without creation) → no reservations; operator redirected to payment detail
