# Research: RSVR Sales Demonstration Script

**Date**: 2026-08-01
**Spec**: `specs/057-sales-demonstration-script/spec.md`

## Purpose

Establish the authoritative, implementation-grounded inventory of RSVR features, business rules, navigation, and statuses that will be transcribed into `docs/sales_script.md`, plus the feature-request handoff format aligned to Spec Kit input.

## Method

Inspected the current application source (read-only) as the source of truth:
- `backend/config/urls.py` — top-level route catalog
- Per-app `urls.py`, `views.py`, `models.py`, `templates/` for each app (clients, reservations, classes, equipment, payments)
- `backend/templates/base.html` — authenticated navigation/menu structure
- `backend/locale/es/LC_MESSAGES/django.po` — canonical Spanish UI labels
- `docs/` and `README.md` — existing documentation to reconcile
- Recent spec history under `specs/` — to classify future/planned functionality

## Decisions

### Decision 1: Feature inventory (source: routes + views + templates)

**Decision**: The implemented feature catalog is derived from the Django route table and view/template inventory. Confirmed reachable, user-facing feature areas:

| # | Feature Area | Key Capabilities | Route(s) |
|---|--------------|------------------|----------|
| 1 | Authentication & user access | Login/logout (Django auth), session-based; admin at `/admin/` | `accounts/`, `admin/` |
| 2 | Clients | Search by name, create, detail, CSV upload (bulk import) with template download, per-client calendar | `clients/...` |
| 3 | Reservations | List (by slot/date), calendar view, PDF export of list, create (with auto-date for slot), detail, status change (reserved/used/unused), duplicate-prevention rule | `reservations/...` |
| 4 | Class schedule | Weekly schedule view, per-slot toggle active/inactive | `classes/...` |
| 5 | Equipment | List, detail, create, edit; types (climber/treadmill/bike/elliptical/rower/other), status (in-service/out-of-service) | `equipment/...` |
| 6 | Payments | List + search, create (incl. from reservation), detail, edit, delete (soft), associate reservations, client payment history, batch creation (multi-slot, weekly date groups), batch data, payment calendar, reports, CSV export (superuser), evidence upload, payment types (CASH/CC/DC/TRANSF/PAPP) | `payments/...` |

**Rationale**: Routes and views are the ground truth for what is implemented and reachable; the catalog must not invent features.

**Alternatives considered**: Relying on README/feature-list docs alone — rejected because docs can lag behind implementation and violate the source-of-truth rule.

### Decision 2: Business rules matrix (source: models + validation)

**Decision**: Business rules documented in the sales script are extracted from model constraints, `clean()` validation, unique constraints, and form/view logic:

- **Client**: at least one of email or mobile required (`Client.clean`); email and mobile unique; ordering by last name/first name.
- **Reservation**: unique per (equipment, class_slot, date) → duplicate reservation blocked; status choices reserved/used/unused (default reserved); equipment and class_slot `PROTECT` on delete; date is a required field; auto-date for selected slot in create flow.
- **ClassSlot**: day choices Mon–Fri (0–4), time choices 17:30/18:30; unique (day, time); `is_active` toggles availability; inactive slot cannot be reserved (toggle behavior).
- **Equipment**: equipment_type choices (climber/treadmill/bike/elliptical/rower/other); status choices in-service/out-of-service (default in-service); name required.
- **Payment**: amount decimal(10,2) required; payment_type choices (CASH/CC/DC/TRANSF/PAPP); `payment_identifier` unique; date required; `class_slot_count` positive small int required; evidence image optional; soft-delete via `is_deleted`/`deleted_at` (records retained, hidden from active lists); created_by required.
- **PaymentReservation**: links payments to reservations (many-to-many via explicit linking model) — only linked reservations count toward a payment; unassociated reservations appear in the client history filtered list.

**Rationale**: Model constraints and `clean()` are the enforceable, user-visible business rules; documentation must not invent rules not enforced.

**Alternatives considered**: Documenting rules from prose specs alone — rejected; several documented rules have changed in code.

### Decision 3: Feature status classification

**Decision**: Every feature/capability in the script is tagged with one of: `Implemented`, `Partially implemented`, `Known limitation`, `Not implemented`, `Future feature`. Derived statuses at plan time:

- All routes above = `Implemented`.
- CSV client upload, batch payments, payment export, PDF reservation list = `Implemented` (recently shipped features 016/048/056/039 etc.).
- Payment reports = `Implemented` but restricted to superusers (`UserPassesTestMixin`) → note role restriction as business rule.
- Known limitations to surface: equipment/class-slot deletion is `PROTECT`-constrained (must resolve reservations first); payment evidence stored as uploaded image only; report graph series are stacked daily/weekly/monthly (features 032/034/035).
- Windows deployment is documented in `docs/windows11_deployment.md` (feature 028) — deployment platform is a documented operational capability, not a user-facing demo feature.

**Rationale**: Status must be assigned by inspecting implementation; the sales script must never present unimplemented/unverified functionality as available (AC-06).

**Alternatives considered**: Treating everything not in code as "future feature" — rejected; requires classification granularity for partial/limited cases.

### Decision 4: Navigation and Spanish UI labels

**Decision**: The demonstration flow follows the authenticated `base.html` navbar: **Clients → Payments → Reservations → Equipment → Schedule → Reports (superuser) → Admin → Logout**. Canonical Spanish labels are taken from `django.po` (e.g., "Clientes", "Pagos", "Reservaciones", "Equipos", "Horario", "Reportes", "Admin", "Cerrar sesión"). The home route (`/`) redirects to `clients:client-search`.

**Rationale**: The nav order is the actual user flow; using `django.po` labels keeps the script consistent with the live UI.

**Alternatives considered**: Inventing an English-only navigation mapping — rejected; inconsistent with the Spanish UI shown during demos.

### Decision 5: Existing documentation reconciliation

**Decision**: `docs/windows11_deployment.md` (deployment) and `README.md` (setup) are referenced in the script's maintenance section but are **not** sources for demo feature content (they describe deployment, not user-facing behavior). The source-of-truth rule applies: where any doc conflicts with implementation, the script describes actual behavior.

**Rationale**: Deployment guides are operational, not sales-demonstration content.

**Alternatives considered**: Including deployment steps in the demo flow — rejected; out of scope for a feature demonstration.

### Decision 6: Feature-request handoff format

**Decision**: The handoff template mirrors the Spec Kit `spec-template.md` structure (Feature Name, Requester, User Role, Business Problem, Business Goal, User Need, Expected Behavior, Business Rules, Data Requirements, Acceptance Criteria, Examples, Priority, Required Date, Related RSVR Features, Open Questions, Development Notes). This makes captured requests directly consumable as input to `/speckit.specify`.

**Rationale**: Aligns with spec AC-09 (development handoff suitable as Spec Kit input).

**Alternatives considered**: A free-form notes template — rejected; too unstructured to feed the specification workflow.

## Open Items

- None requiring clarification. All spec unknowns resolved by source inspection.
