# RSVR Sales Demonstration Script

**Purpose**: A structured guide to demonstrate the current, implemented capabilities of the RSVR application to prospective users. It reflects the **actual state of the application code and its implemented behavior** — it does not describe planned, missing, or unverified functionality as available.

**Audience**: Salespersons and application demonstrators who present RSVR to prospective users and capture new feature requests.

**Source of truth**: This document is derived from the RSVR application implementation (routes, views, models, forms, templates, and tests). If this document and the application ever disagree, the application behavior is authoritative.

---

## 1. Purpose and Audience

The RSVR Sales Demonstration Script supports a consistent, accurate, business-oriented product demonstration. It allows a demonstrator to:

1. Present the application's currently implemented features in a logical sequence.
2. Explain the business rules associated with each feature.
3. Clearly distinguish implemented functionality from partial, limited, missing, or planned functionality.
4. Quickly locate information when a prospective user asks about a specific capability.
5. Capture the information needed to define a new feature request.
6. Provide that captured information to the development team as input for a future specification.

The script prioritizes **observable application behavior** over technical implementation details. Technical details are included only when they help explain a feature, limitation, or integration.

---

## 2. Demonstration Preparation

Before starting a demonstration, confirm the following:

| Precondition | Details |
|--------------|---------|
| Application running | Start the environment with `make db-up`, then `make migrate`, `make seed`, and `make serve` (app at http://localhost:8000). |
| Demo data | Seed representative data with `make seed` (class slots, equipment, and clients). |
| User account | Log in with a user account that has the access levels you intend to show (see Section 3.2). |
| Demo calendar | Ensure today's date and class schedule align with the flows you plan to show (reservations, calendar, batch creation). |
| Navigation map | Review Section 3.3 (Main Navigation) so the menu structure is familiar. |

Verify the account role you will use (Operator vs Administrator vs superuser) because some features, such as payment reports, are restricted to Administrators/superusers.

---

## 3. Recommended Demonstration Flow

Follow the flow in order for a complete demonstration. Each subsection is optional and can be skipped depending on the audience's interests.

### 3.1 Application Overview

Start at the application home page. An authenticated user is redirected to the **Clients** search page. Briefly explain:

- RSVR manages cardio/class equipment reservations for clients.
- It covers the full client lifecycle: clients, reservations, class schedule, equipment, and payments.
- The interface is in Spanish and is designed for daily operation by staff.

### 3.2 Authentication and User Access

- Show the login page at `/accounts/login/`. Access requires a username and password (session-based authentication).
- After login, the top navigation bar appears.
- Demonstrate the **Admin** link to the Django administration site (restricted to users with staff/admin permissions).
- Show **Logout** (labeled "Cerrar sesión") and log back in.
- Note: There are two seeded user groups — **Operators** and **Administrators** — plus superusers. Some features (e.g., payment reports) are available only to Administrators and superusers.

### 3.3 Main Navigation

The navigation menu appears for authenticated users, in this order:

1. **Clients** (`/clients/search/`) — client search and management.
2. **Payments** (`/payments/`) — payment list, search, and history.
3. **Reservations** (`/reservations/`) — reservation list.
4. **Equipment** (`/equipment/`) — equipment catalog (shown if the user has equipment view permission).
5. **Schedule** (`/classes/`) — class schedule (shown if the user has class schedule view permission).
6. **Reports** (dropdown) — payment reports (shown only to superusers).
7. **Admin** — Django administration site.
8. **Logout**.

The home page (`/`) redirects to the Clients search page.

### 3.4 Core Business Workflow (Reservations)

Walk through the reservation lifecycle:

1. **Create a reservation**: Go to **Reservations → New Reservation** (`/reservations/create/`). Select a client, an equipment, a class slot, and a date. The form auto-suggests the next date for the selected class slot based on today's date. Add optional notes and save.
2. **Duplicate prevention**: Attempting to reserve the same equipment for the same class slot on the same date that is already `Reserved` is blocked with an "already reserved" message.
3. **Reservation list**: View all reservations at `/reservations/`. Filter by class slot and date, and by status.
4. **Reservation detail**: Open a reservation to see full details.
5. **Change status**: A reservation can be marked as **Used** (marcar como Usado), **Not used** (marcar como No usado), or back to **Reserved**. This is done from the reservation detail page.
6. **Export PDF**: From the reservation list, generate a PDF of reservations for a selected class and date.
7. **Download calendar**: Export reservations in a date range as an `.ics` calendar file (also available per client from the client detail page).

### 3.5 Data Management

#### Clients

- **Search**: From **Clients**, search by name, mobile, or email (results appear as you type). Paginated results.
- **Create**: Add a new client with first name, last name, email, and/or mobile. At least one of email or mobile is required.
- **Client detail**: View a client's reservations and payment history.
- **CSV upload**: Bulk import clients from a CSV file (`/clients/upload/`). Download the template first; only `.csv` files up to 5 MB are accepted. The upload reports created, updated, and error rows.
- **Client calendar**: From the client detail page, download the client's reservations for a date range as an `.ics` file.

#### Equipment

- **List**: Browse all equipment at `/equipment/`, ordered by name.
- **Detail**: View equipment details.
- **Create / Edit**: Add or edit equipment with a name, type (Escaladora/Climber, Cinta de correr/Treadmill, Bicicleta estacionaria/Stationary Bike, Elíptica/Elliptical, Máquina de remo/Rowing Machine, Otro/Other), status (En servicio/In Service, Fuera de servicio/Out of Service), and notes.
- Only equipment **In Service** can be selected when creating reservations.

### 3.6 Reporting and Visualization

- **Payment reports** (Administrators and superusers only): Go to **Reports → Payments** (`/payments/reports/`). View aggregated payment totals grouped by day, week, or month, with a date range filter, rendered as charts.
- **Payment export** (Administrators and superusers only): Export payments for a date range to an Excel file (`/payments/reports/export/`), containing identifier, client, amount, type, date, and class count.
- **Reservation PDF export**: Generate a printable PDF of a class/date reservation list.

### 3.7 Administration

- **Django Admin** (`/admin/`): Manage users, groups, clients, equipment, class slots, reservations, and payments with the standard Django admin interface.
- **Class schedule toggling** (`/classes/`): View the weekly class schedule and activate/deactivate class slots. Inactive slots are no longer available when creating reservations.

### 3.8 Other Implemented Features

- **Payments (client history)**: From the client detail or payments page, view a client's payment history and their **unassociated reservations** (reservations not yet linked to a payment).
- **Payment association**: Associate reservations with a payment from the payment detail page.
- **Batch reservation creation**: From a payment detail page, create multiple reservations at once (up to 20) for a selected equipment and class slot across a generated date range, respecting the payment's class slot count.
- **Payment calendar export**: Download a payment's associated reservations as an `.ics` file.
- **Payment evidence**: Upload an image (JPEG/PNG, max 5 MB) as payment evidence.

---

## 4. Feature Catalog

The table below lists the currently implemented user-facing features. Use it for quick lookup during a demonstration.

| Feature | Status | User/Role | Demonstration Location | Business Area |
|---------|--------|-----------|------------------------|----------------|
| Login / Logout | Implemented | All authenticated users | `/accounts/login/`, navigation menu | Authentication |
| Django Admin | Implemented | Staff/superuser | `/admin/` | Administration |
| Client search | Implemented | All authenticated users | Clients → Search (`/clients/search/`) | Clients |
| Client create | Implemented | All authenticated users | Clients → New Client (`/clients/create/`) | Clients |
| Client CSV upload | Implemented | All authenticated users | `/clients/upload/` | Clients |
| Client calendar (.ics) | Implemented | All authenticated users | Client detail → Download Calendar | Clients |
| Reservation create | Implemented | All authenticated users | Reservations → New Reservation (`/reservations/create/`) | Reservations |
| Reservation list / filter | Implemented | All authenticated users | `/reservations/` | Reservations |
| Reservation status change | Implemented | All authenticated users | Reservation detail | Reservations |
| Reservation PDF export | Implemented | All authenticated users | Reservations → PDF | Reservations |
| Reservation calendar (.ics) | Implemented | All authenticated users | Reservations → Calendar | Reservations |
| Class schedule | Implemented | Users with schedule permission | `/classes/` | Classes |
| Class slot activate/deactivate | Implemented | Users with schedule permission | `/classes/` | Classes |
| Equipment list | Implemented | Users with equipment permission | `/equipment/` | Equipment |
| Equipment create / edit | Implemented | Users with equipment permission | `/equipment/create/`, `/equipment/<pk>/edit/` | Equipment |
| Payment list / search | Implemented | All authenticated users | Payments (`/payments/`) | Payments |
| Payment create | Implemented | All authenticated users | Payments → New Payment | Payments |
| Payment edit (partial) | Implemented | All authenticated users | Payment detail → Edit | Payments |
| Payment soft delete | Implemented | All authenticated users | Payment detail → Delete | Payments |
| Payment detail | Implemented | All authenticated users | `/payments/<pk>/` | Payments |
| Payment association | Implemented | All authenticated users | Payment detail → Associate | Payments |
| Client payment history | Implemented | All authenticated users | `/payments/client/<id>/` | Payments |
| Unassociated reservations list | Implemented | All authenticated users | Client payment history | Payments |
| Batch reservation creation | Implemented | All authenticated users | Payment detail → batch modal | Payments |
| Payment calendar (.ics) | Implemented | All authenticated users | Payment detail → Calendar | Payments |
| Payment evidence upload | Implemented | All authenticated users | Payment create/edit form | Payments |
| Payment reports | Implemented | Administrators and superusers | Reports → Payments | Payments |
| Payment export (Excel) | Implemented | Administrators and superusers | Reports → Export | Payments |

---

## 5. Business Rules

Business rules are derived from the current application implementation.

### Clients

| Rule | Detail |
|------|--------|
| Required contact | At least one of email or mobile is required when creating a client. |
| Unique email | Email must be unique among clients (if provided). |
| Unique mobile | Mobile must be unique among clients (if provided). |
| Ordering | Clients are listed ordered by last name, then first name. |
| CSV format | Uploaded files must be `.csv`, up to 5 MB, with columns `first_name, last_name, email, mobile`. |

### Reservations

| Rule | Detail |
|------|--------|
| Duplicate prevention | A reservation for the same equipment + class slot + date that is `Reserved` is blocked. |
| Status values | `reserved` (default), `used`, `unused`. |
| Status transitions | `reserved → used`, `reserved → unused`, and back to `reserved` via the status-change action. |
| Equipment availability | Only equipment **In Service** can be selected when creating a reservation. |
| Slot availability | Only **active** class slots can be selected when creating a reservation. |
| Automatic date | When creating a reservation, the form suggests the next occurrence date for the selected class slot. |
| Delete protection | Equipment and class slots referenced by reservations cannot be deleted while reservations exist (they must be handled before removal). |
| Batch limit | Batch creation supports at most 20 reservations at a time; exactly the payment's class slot count must be selected; dates must be within the allowed range. |

### Class Schedule

| Rule | Detail |
|------|--------|
| Days | Slots exist for Monday through Friday. |
| Times | Slots are defined at 17:30 and 18:30. |
| Uniqueness | A day/time combination is unique. |
| Activation | Deactivating a slot makes it unavailable for new reservations; the schedule page toggles this. |

### Equipment

| Rule | Detail |
|------|--------|
| Types | Climber, Treadmill, Stationary Bike, Elliptical, Rowing Machine, Other. |
| Status | `in-service` (default) or `out-of-service`. |
| Reservation eligibility | Only `in-service` equipment can be used for new reservations. |

### Payments

| Rule | Detail |
|------|--------|
| Payment types | Cash (Efectivo), Credit Card, Debit Card, Electronic Transfer, Payments App. |
| Amount | Required, positive, up to two decimal places. |
| Identifier | Unique; if left empty, it is auto-generated. |
| Class slot count | Required, between 1 and 20. |
| Date | Required; defaults to today on creation. |
| Evidence | Optional image, JPEG or PNG, max 5 MB. |
| Edit restrictions | On edit, only reference, notes, and evidence can be changed; core payment fields are locked. |
| Soft delete | Deleting a payment sets it as deleted (`is_deleted`); deleted payments no longer appear in active lists but are retained. |
| Association limit | A payment cannot be associated with more reservations than its class slot count. |
| Report access | Payment reports and exports are restricted to Administrators and superusers. |

---

## 6. Feature Status and Known Gaps

### Status vocabulary

| Status | Meaning |
|--------|---------|
| `Implemented` | Available and working in the current application |
| `Partially implemented` | Some functionality is available, but the feature is incomplete |
| `Known limitation` | The functionality exists but has a documented limitation |
| `Not implemented` | The capability is not currently available |
| `Future feature` | Identified as a potential future capability |

### Implemented

All features listed in the Feature Catalog (Section 4) are `Implemented`. They are available in the current application and can be demonstrated.

### Known limitations

- **Payment edit**: Only reference, notes, and evidence can be changed after creation; amount, type, identifier, date, and class slot count are locked.
- **Equipment / class slot deletion**: Referenced equipment and class slots cannot be removed while reservations exist (protected). Administrators must manage reservations first.
- **Payment reports scope**: Reports and exports are limited to Administrators and superusers; other users cannot view them.

### Not implemented / Future features

The following are not currently available and must not be presented as implemented:

- **Client self-service portal**: No client-facing self-service or online booking.
- **Payment gateways**: No online/real-time payment processing integration.
- **Notifications**: No email/SMS notification system for clients.
- **Mobile application**: No dedicated mobile app.
- **Multi-language UI toggling at runtime**: The interface is Spanish-only.

---

## 7. Frequently Asked Feature Questions

### Does RSVR support searching clients?

**Answer**: Yes. The Clients page supports live search by name, mobile, or email with paginated results.

**Status**: Implemented

**See**: Section 3.5 (Data Management) and Section 4 (Feature Catalog).

---

### Can RSVR prevent double bookings?

**Answer**: Yes. A reservation for the same equipment, class slot, and date that is already `Reserved` is blocked with an "already reserved" message.

**Status**: Implemented

**See**: Section 5 (Business Rules, Reservations).

---

### Can reservations change status after they are made?

**Answer**: Yes. Reservations can be marked as Used, Not used, or back to Reserved from the reservation detail page.

**Status**: Implemented

**See**: Section 3.4 (Core Business Workflow).

---

### Can clients be imported in bulk?

**Answer**: Yes. Staff can upload a CSV file (up to 5 MB) to create or update clients in bulk; the template can be downloaded first.

**Status**: Implemented

**See**: Section 3.5 (Data Management).

---

### Can the system generate a printable class list?

**Answer**: Yes. A PDF of reservations for a selected class and date can be generated from the Reservations page.

**Status**: Implemented

**See**: Section 3.4 (Core Business Workflow).

---

### Can payments be linked to reservations?

**Answer**: Yes. Reservations can be associated with a payment, either individually or in batch, and unassociated reservations are shown for follow-up.

**Status**: Implemented

**See**: Section 3.8 (Other Implemented Features).

---

### Can the administrator view payment reports?

**Answer**: Yes. Administrators and superusers can view aggregated payment reports grouped by day, week, or month and export them to Excel.

**Status**: Implemented (restricted to Administrators and superusers)

**See**: Section 3.6 (Reporting and Visualization).

---

### Does RSVR offer online payments?

**Answer**: No. Payments are recorded manually in the system; there is no online payment gateway integration.

**Status**: Not implemented / Future feature

**See**: Section 6 (Feature Status and Known Gaps).

---

### Does RSVR notify clients automatically?

**Answer**: No. There is no email/SMS notification system for clients.

**Status**: Not implemented / Future feature

**See**: Section 6 (Feature Status and Known Gaps).

---

## 8. New Feature Request Questionnaire

Use this questionnaire to capture a feature request during or immediately after a sales conversation.

1. **What feature is being requested?**
2. **Who needs the feature?** (person, role, organization)
3. **What problem or business need does it solve?**
4. **What is the expected behavior?**
5. **What should the user be able to do?**
6. **What information or data is involved?**
7. **What business rules or restrictions are expected?**
8. **What is the expected result?**
9. **Are there examples or real-world scenarios?**
10. **Is the feature required by a specific date or milestone?**
11. **Is the feature mandatory or optional?**
12. **Are there related existing RSVR features?**

Record the answers directly into the Feature Request Handoff template (Section 9).

---

## 9. Feature Request Handoff

After collecting the questionnaire answers, transfer them into this template. The completed template is suitable as an initial input for a future specification workflow (Spec Kit).

```markdown
# Feature Request

## Feature Name
[Feature name]

## Requester
[Person or organization]

## User Role
[Role]

## Business Problem
[Problem being solved]

## Business Goal
[Expected business outcome]

## User Need
[What the user needs to accomplish]

## Expected Behavior
[Description of expected functionality]

## Business Rules
[Known rules and constraints]

## Data Requirements
[Required data and information]

## Acceptance Criteria
[Expected outcomes]

## Examples
[Concrete scenarios]

## Priority
[Priority]

## Required Date
[Date, if applicable]

## Related RSVR Features
[Related functionality]

## Open Questions
[Questions requiring clarification]

## Development Notes
[For development team use]
```

### Guidance: turning a captured request into development-ready requirements

1. Ensure every field above is filled; leave open questions explicit instead of guessing.
2. Confirm the **business problem** and **goal** describe user value, not a specific technical solution.
3. Restate **expected behavior** as observable actions with clear outcomes (what the user does and what the system does in response).
4. List **business rules** precisely (required fields, allowed values, restrictions, statuses).
5. Define **acceptance criteria** as testable statements of the form "Given … When … Then …".
6. Note related existing RSVR features so the development team can reuse current patterns.
7. Send the completed template to the development team as input for a specification; this sales script is not the final technical specification.

---

## 10. Maintenance and Verification

The sales script must always reflect the **actual implementation**. Update it whenever application features or business rules change:

1. **Track changes**: When a feature ships or a business rule changes, update the affected entries in the Feature Catalog (Section 4) and Business Rules (Section 5).
2. **Update statuses**: Move new features to `Implemented` only after they are verified working; classify partial/limited/missing functionality accordingly (Section 6).
3. **Verify against the app**: Re-run the demonstration flow (Section 3) against a current seeded instance and confirm the documented expected results still match.
4. **Keep FAQ current**: Add or update FAQ entries when new capabilities are commonly asked about (Section 7).
5. **Remove empty sections**: If a section no longer applies to the application, remove it rather than leaving it empty.
6. **Source-of-truth rule**: If documentation and the application disagree, this script describes the behavior actually implemented and available.
