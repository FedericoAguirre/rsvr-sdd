# Contract: RSVR Sales Script Document (`docs/sales_script.md`)

**Date**: 2026-08-01
**Spec**: `specs/057-sales-demonstration-script/spec.md`

## Purpose

This contract defines the required structure, content rules, and quality gates for the deliverable sales demonstration script at `docs/sales_script.md`. It is a **document contract**, not an application interface — the deliverable is a static Markdown document consumed by sales staff and Markdown renderers.

## Required Sections

The document MUST contain the following top-level sections (section numbering may be adjusted to match discovered features; empty or inapplicable sections MUST be removed):

1. **Purpose and Audience** — who uses the script and how.
2. **Demonstration Preparation** — preconditions (accounts, demo data, seed command `make seed`), environment notes.
3. **Recommended Demonstration Flow** — ordered flow with subsections: Application Overview; Authentication and User Access; Main Navigation; Core Business Workflow; Data Management; Reporting and Visualization; Administration; Other Implemented Features.
4. **Feature Catalog** — lookup table (see Feature Catalog contract below).
5. **Business Rules** — per-feature rules derived from the application implementation.
6. **Feature Status and Known Gaps** — status classification and gaps/future features.
7. **Frequently Asked Feature Questions** — each: question, concise answer, status, section reference.
8. **New Feature Request Questionnaire** — 12 mandatory questions (see Questionnaire contract).
9. **Feature Request Handoff** — development-ready template.
10. **Maintenance and Verification** — how to update the script as the app evolves.

## Feature Catalog Contract

The feature catalog MUST be a table with these columns:

| Feature | Status | User/Role | Demonstration Location | Business Area |
|---------|--------|-----------|------------------------|----------------|

- **Status** values restricted to: `Implemented`, `Partially implemented`, `Known limitation`, `Not implemented`, `Future feature`.
- **Demonstration Location** MUST reference a real route or page in the application (e.g., "Clients → Search", `/reservations/calendar/`).
- The catalog MUST match the actually implemented routes and views (source of truth = `backend/config/urls.py` + app `urls.py`/views). No feature may appear as `Implemented` unless it is reachable and functional in the current app.

## Business Rules Contract

For each demonstrated feature, business rules MUST be documented in plain business language covering (as applicable): required/optional fields, validation, allowed values, user permissions, role-based access, status transitions, workflow constraints, data dependencies, calculation rules, restrictions, error conditions, duplicate prevention, and record lifecycle rules.

Rules MUST be derived from the application implementation (models, `clean()`, forms, views). The script MUST NOT invent rules not enforced by the application.

## Status Vocabulary

| Status | Meaning |
|--------|---------|
| `Implemented` | Available and working in the current application |
| `Partially implemented` | Some functionality available, feature incomplete |
| `Known limitation` | Exists but has a documented limitation |
| `Not implemented` | Not currently available |
| `Future feature` | Potential future capability |

Only `Implemented` features may be presented as available product capabilities. Partially implemented or limited functionality MUST be disclosed during the demonstration.

## Source-of-Truth Rule

If documentation and application behavior disagree, the script MUST describe the behavior actually implemented and available. Functionality described in docs but not implemented/working MUST be classified as `Not implemented`, `Partially implemented`, `Known limitation`, or `Future feature` — never presented as available.

## Questionnaire Contract (12 questions)

1. What feature is being requested?
2. Who needs the feature?
3. What problem or business need does it solve?
4. What is the expected behavior?
5. What should the user be able to do?
6. What information or data is involved?
7. What business rules or restrictions are expected?
8. What is the expected result?
9. Are there examples or real-world scenarios?
10. Is the feature required by a specific date or milestone?
11. Is the feature mandatory or optional?
12. Are there related existing RSVR features?

## Handoff Template Contract

The handoff template MUST include these fields (aligned to Spec Kit spec input): Feature Name, Requester, User Role, Business Problem, Business Goal, User Need, Expected Behavior, Business Rules, Data Requirements, Acceptance Criteria, Examples, Priority, Required Date, Related RSVR Features, Open Questions, Development Notes.

## Invariants

- The document MUST exist at `docs/sales_script.md` (AC-10).
- Every feature/status entry MUST be verifiable against the application implementation (AC-01, AC-02, AC-06).
- No unimplemented/unverified functionality may be presented as available (AC-06).
- Missing/partial/limited/future functionality MUST be identifiable (AC-07).
- The questionnaire MUST capture enough info to create an initial development requirement (AC-08).
- The handoff MUST be structured as Spec Kit input (AC-09).
- The document MUST have a clear structure for updating features, business rules, statuses, and demo steps as the app evolves (AC-11).
