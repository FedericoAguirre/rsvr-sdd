# Data Model: Cardio Equipment Reservation

## Entities

### Client

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| first_name | CharField(100) | required |
| last_name | CharField(100) | required |
| email | EmailField | unique, nullable (if mobile provided) |
| mobile | CharField(20) | unique, nullable (if email provided) |
| is_active | BooleanField | default=True |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

**Validation**: At least one of email or mobile MUST be non-null.
**Index**: email, mobile (unique indexes).

### Equipment

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| name | CharField(100) | required |
| equipment_type | CharField(50) | choices: treadmill, bike, elliptical, rower, other |
| status | CharField(20) | choices: in-service, out-of-service; default: in-service |
| notes | TextField | optional, blank |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |

**Index**: status.

### Class Slot

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| day_of_week | IntegerField | choices: 0=Mon..4=Fri |
| time | TimeField | choices: 17:30, 18:30 |
| is_active | BooleanField | default=True |

**Unique**: (day_of_week, time).
**Note**: Pre-populated with 10 rows (Mon-Fri × 2 times). Admins can
activate/deactivate slots.

### Reservation

| Field | Type | Constraints |
|-------|------|-------------|
| id | AutoField | PK |
| client | ForeignKey(Client) | CASCADE |
| equipment | ForeignKey(Equipment) | PROTECT |
| class_slot | ForeignKey(ClassSlot) | PROTECT |
| date | DateField | required |
| created_by | ForeignKey(User) | SET_NULL, nullable |
| created_at | DateTimeField | auto_now_add |
| updated_at | DateTimeField | auto_now |
| notes | TextField | optional, blank |

**Unique**: (equipment, class_slot, date) — prevents double-booking.
**Index**: (date, class_slot) for schedule views; (client, date) for client
history.
**Constraints**: date must be a weekday (Mon-Fri); equipment.status must be
'in-service' at reservation time.

### User (Django built-in)

Extends `django.contrib.auth.models.User` with groups/permissions:
- **Operator**: can create/view reservations; search clients; view equipment
- **Administrator**: all Operator permissions + manage equipment, class slots

## Relationships

```
Client ──< Reservation >── Equipment
                │
                └── ClassSlot

User (Staff) ──< Reservation (created_by)
```

## State Transitions

**Equipment**:
```
in-service ──→ out-of-service (admin marks unavailable)
out-of-service ──→ in-service (admin marks available)
```

**Reservation**:
```
Created (only state — no cancellation modeled for MVP)
```

## Validation Rules

1. At least one of email or mobile required for Client
2. No duplicate reservation (equipment + class_slot + date unique)
3. Reservation date must be Monday–Friday
4. Reservation time must be 17:30 or 18:30
5. Equipment must be in-service when reserved
6. Equipment status change to out-of-service SHOULD flag existing future
   reservations for review (manual handling papered in quickstart)
