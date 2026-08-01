# Quickstart Validation: RSVR Sales Demonstration Script

**Date**: 2026-08-01
**Spec**: `specs/057-sales-demonstration-script/spec.md`
**Contract**: `contracts/sales-script-contract.md`
**Data model**: `data-model.md`

## Purpose

Runnable validation scenarios proving the sales demonstration script document is complete, accurate, and consistent with the actual application. This is a **documentation-only** feature — validation is manual/static review plus confirmation the existing automated suite remains green.

## Prerequisites

- A checkout of the repository on branch `057-sales-demonstration-script`.
- A running application instance with seeded demo data for behavior spot-checks (`make db-up`, `make migrate`, `make seed`, `make serve` → http://localhost:8000).
- Python test tooling installed (`uv` per the constitution; run tests with `make test`).

## Scenario 1 — Document Exists and Is Complete

**Given** the repository on the feature branch,
**When** I inspect `docs/sales_script.md`,
**Then**:

- [ ] The file exists at `docs/sales_script.md`
- [ ] It contains all 10 required sections from the document contract
- [ ] No section that does not apply to the current application is present as an empty placeholder

## Scenario 2 — No Unsupported Claims (AC-06)

**Given** the feature catalog table in the script and the application routes in `backend/config/urls.py` and each app's `urls.py`,
**When** I cross-check every catalog row marked `Implemented`,
**Then**:

- [ ] Each `Implemented` feature corresponds to a real reachable route/view
- [ ] No `Implemented` row lacks a corresponding implementation
- [ ] Features that do not exist, are partial, limited, or future are NOT marked `Implemented`

## Scenario 3 — Business Rules Match Implementation (AC-02)

**Given** the Business Rules section and the application models/validations,
**When** I spot-check rules against `backend/apps/*/models.py` (unique constraints, `clean()`, choices) and views,
**Then**:

- [ ] Client creation rule (email or mobile required) matches `Client.clean`
- [ ] Duplicate reservation prevention matches `unique_together (equipment, class_slot, date)`
- [ ] Payment identifier uniqueness matches the model `unique=True`
- [ ] Reservation status choices (reserved/used/unused) match the model choices
- [ ] No documented rule is contradicted by the implementation

## Scenario 4 — Feature Lookup Speed (SC-003)

**Given** a live demo instance and the script open,
**When** a question is asked about any cataloged feature,
**Then**:

- [ ] The demonstrator can locate the feature's status and demonstration location in under 1 minute
- [ ] The FAQ entry (if the question is listed) provides a concise answer with status and section reference

## Scenario 5 — Demonstration Flow Reproducible (SC-001, AC-03)

**Given** the recommended demonstration flow and a running seeded instance,
**When** a demonstrator follows the flow section by section,
**Then**:

- [ ] Each step produces the documented expected result without undocumented knowledge
- [ ] Navigation matches the actual `base.html` menu (Clients → Payments → Reservations → Equipment → Schedule → Reports → Admin)

## Scenario 6 — Questionnaire and Handoff (AC-08, AC-09)

**Given** a hypothetical new feature request,
**When** I complete the questionnaire and transfer answers to the handoff template,
**Then**:

- [ ] The questionnaire covers all 12 mandatory questions
- [ ] The completed handoff template can be used as initial input for a Spec Kit specification

## Scenario 7 — No Regression in Application

**Given** the documentation-only change,
**When** I run the automated test suite,
**Then**:

- [ ] `make test` passes (no failures introduced)
- [ ] `make lint` passes (no code files changed)

## Expected Outcomes

All checkboxes above must be marked. Any failure indicates the script does not yet satisfy the acceptance criteria and must be corrected before `/speckit.tasks`.
