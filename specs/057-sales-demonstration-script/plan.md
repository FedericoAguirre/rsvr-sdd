# Implementation Plan: RSVR Sales Demonstration Script

**Branch**: `057-sales-demonstration-script` | **Date**: 2026-08-01 | **Spec**: `specs/057-sales-demonstration-script/spec.md`

**Input**: Feature specification from `specs/057-sales-demonstration-script/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

The primary requirement is to produce a single Markdown document at `docs/sales_script.md` that serves as the authoritative sales demonstration guide for the current state of the RSVR application. The document must reflect the **actually implemented** user-facing features and business rules (source-of-truth rule), distinguish implemented from planned/unavailable functionality, provide a feature catalog and FAQ for quick lookup, and include a feature-request questionnaire and handoff template suitable as input for a future Spec Kit specification. This is a **documentation-only** deliverable — no application source code, models, URLs, or business rules are modified.

## Technical Context

**Language/Version**: N/A (Markdown document) — app source is Django 5.0.x / Python 3.12 for reference only

**Primary Dependencies**: None new. Document authored in Markdown (GFM). No library dependencies.

**Storage**: N/A — deliverable is a repository file at `docs/sales_script.md`

**Testing**: Manual verification per quickstart scenarios (documentation artifact). Existing pytest suite must remain unchanged and passing.

**Target Platform**: Repository documentation consumed by sales staff; readable in any Markdown viewer (GitHub, IDE)

**Project Type**: Documentation artifact within a Django web application repo

**Performance Goals**: N/A — static document; lookup should return answers quickly (SC-003: under 1 minute)

**Constraints**: 
- The document MUST reflect actual implemented behavior — it is grounded by inspecting the current app (URLs, models, views, templates, tests)
- No application functionality, schemas, API contracts, or business rules may be changed
- All user-visible feature content must be consistent with the source-of-truth rule; unimplemented features must be classified, not promoted
- The exact section structure may be adapted to discovered features; empty/inapplicable sections must be removed

**Scale/Scope**: Single Markdown document covering ~5 application areas (clients, reservations, classes, equipment, payments) plus admin/auth

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| **I. Code Quality** | All code must pass automated linting. No dead/commented-out code. | ✅ Pass — no application code changed; only a Markdown doc added. Existing `make lint` must remain clean (run to confirm no-op). |
| **II. Testing Standards (NON-NEGOTIABLE)** | TDD mandatory; tests written first. Integration tests for boundary-crossing changes. | ✅ Pass — no code or library contracts change, so no new unit/integration tests are applicable. Existing suite (`make test`) must remain green. Validation is via quickstart manual scenarios. |
| **III. UX Consistency** | i18n NON-NEGOTIABLE for user-visible strings; user-facing docs updated in same PR. | ⚠️ PASS — Constitution Principle III requires user-facing documentation updated in the same PR. The feature itself **is** documentation. The doc is the sales-facing artifact; feature/status text should be consistent with the app's Spanish UI where naming matters, but the doc is written in business-oriented language (English, per repo docs like `windows11_deployment.md`). No app strings added, so no `django.po` changes required. |
| **IV. Performance** | Measurable performance criteria defined before implementation. | ✅ Pass — static document, no runtime performance impact. |
| **V. External Documentation** | Every library API call informed by current fetched docs (Context7). | ✅ Pass — no library APIs used. No Context7 lookups required. |

**Violation Justification**: None required — no violations.

## Project Structure

### Documentation (this feature)

```text
specs/057-sales-demonstration-script/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command — NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
docs/
└── sales_script.md                    # CREATED — the sales demonstration script deliverable

backend/
├── apps/
│   ├── clients/                       # REFERENCE ONLY — feature/business-rule source
│   ├── reservations/                  # REFERENCE ONLY
│   ├── classes/                       # REFERENCE ONLY
│   ├── equipment/                     # REFERENCE ONLY
│   └── payments/                      # REFERENCE ONLY
├── config/urls.py                     # REFERENCE ONLY — route catalog
├── locale/es/LC_MESSAGES/django.po    # REFERENCE ONLY — Spanish UI terms
└── tests/                             # REFERENCE ONLY — confirms implemented behavior
```

**Structure Decision**: Single documentation deliverable under `docs/`. All application directories under `backend/` are read-only sources of truth for deriving feature content; no files there are modified.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations requiring justification.

---

## Phase 0: Outline & Research

### Research Tasks

| Unknown / Dependency | Research Question | Context |
|----------------------|-------------------|---------|
| Implemented feature inventory | Which user-facing features are actually implemented and reachable in the current app? | Derive from `config/urls.py`, each app's `urls.py`, views, and templates |
| Business rules per area | What business rules and validations are enforced (required fields, uniqueness, status transitions, payment associations)? | Inspect models (unique constraints, choices, `clean()`), forms, views |
| Feature status classification | Which capabilities are fully implemented vs partial/limited/missing/future? | Cross-check recent spec history, feature statuses in templates, known gaps |
| UI navigation & Spanish labels | How does a demonstrator navigate the app (menu structure) and what are the canonical Spanish UI labels? | Inspect `base.html`, templates, `django.po` |
| Existing documentation to reconcile | What existing docs (deployment guide, README) describe behavior, and does any contradict implementation? | `docs/windows11_deployment.md`, `README.md` |
| Feature-request handoff format | What structure makes a captured request suitable as Spec Kit input? | Existing spec template structure (`.specify/templates/spec-template.md`) |

### Expected Decisions from Research

1. **Feature catalog table**: definitive list of implemented features with status, user role, demonstration location, and business area
2. **Business rules matrix**: authoritative per-feature business rules grounded in models/forms/views
3. **Demonstration flow order**: logical sequence (overview → auth → navigation → core workflow → data management → reporting → admin)
4. **FAQ set**: likely demonstration questions with answers + status + references
5. **Handoff template**: feature-request template aligned to Spec Kit spec input

---

## Phase 1: Design & Contracts

### Data Model

No application data model changes — the feature is a static document. The document's internal structure and the read-only domain entities it references are documented in `data-model.md` (including reservation status transitions and validation-rule sources).

### Interface Contracts

The deliverable's **document contract** (its required sections and rules) is specified in `contracts/sales-script-contract.md`. It defines:

- Required top-level sections and their purpose
- The feature catalog table columns and status vocabulary
- The business-rules documentation format
- The feature-request questionnaire (12 questions) and handoff template fields
- The source-of-truth rule and maintenance/verification guidance
- Invariants mapping to spec acceptance criteria

### Quickstart Validation Scenarios

See `quickstart.md` for the end-to-end validation guide covering:
1. Document exists at `docs/sales_script.md` with all mandatory sections
2. Feature catalog matches the actual implemented routes/features (no unsupported claims)
3. Business rules match model/validation logic
4. Lookup: each cataloged feature reachable in under 1 minute
5. Demonstration flow reproducible against the live app
6. Existing suite `make test` still passes (no regressions from doc-only change)
