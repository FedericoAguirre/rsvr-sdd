# RSVR Sales Demonstration Script

## 1. Feature Overview

**Feature name:** RSVR Sales Demonstration Script
**Document location:** `@docs/sales_script.md`

### User Story

As an RSVR salesperson or application demonstrator, I want a structured demonstration script that accurately reflects the current capabilities and business rules implemented in the RSVR application, so that I can consistently demonstrate the application to prospective users, answer feature-related questions, identify product gaps, and capture new feature requests for the development team.

---

## 2. Objective

Create and maintain a single Markdown document at:

```text
@docs/sales_script.md
```

The document must serve as the **authoritative sales demonstration guide** for the current state of the RSVR application.

The script must allow a salesperson or demonstrator to:

1. Demonstrate the application's currently implemented features in a logical sequence.
2. Explain the relevant business rules associated with each feature.
3. Clearly distinguish implemented functionality from planned, missing, or unavailable functionality.
4. Quickly locate information when a prospective user asks about a specific capability.
5. Capture the information required to define a new feature request.
6. Provide the resulting feature information to the development team as input for a future SDD/Spec Kit specification.

The document must be based on the **actual state of the application code and its implemented behavior**, not on assumptions about intended or future functionality.

---

# 3. Scope

## In Scope

The implementation must create or update:

```text
@docs/sales_script.md
```

The document must contain:

* A demonstration introduction.
* A recommended demonstration flow.
* A catalog of currently implemented features.
* The business rules relevant to each demonstrated feature.
* Navigation or references to the corresponding application areas when practical.
* A clear distinction between:

  * Implemented and working features.
  * Partially implemented features.
  * Known limitations.
  * Missing features.
  * Future or planned features.
* A feature lookup section or structure that allows a salesperson to quickly find a specific capability.
* A structured feature-request questionnaire.
* Guidance for converting a captured feature request into development-ready requirements.

## Out of Scope

This feature does not:

* Implement new application functionality.
* Modify existing application behavior.
* Modify database schemas.
* Modify API contracts.
* Change business rules.
* Create automated sales/demo functionality.
* Create a CRM or sales management system.
* Replace the formal SDD specification process.
* Treat undocumented or unimplemented functionality as available functionality.

---

# 4. Source of Truth

The sales script must reflect the **actual current implementation** of the RSVR application.

Before creating or updating the document, the implementation must inspect the relevant application sources, including, as applicable:

* Application source code.
* URL and routing definitions.
* Views/controllers/handlers.
* Models and database definitions.
* Forms and validation logic.
* Templates and UI components.
* API endpoints.
* Authentication and authorization rules.
* Configuration relevant to user-visible functionality.
* Existing documentation.
* Existing tests.
* Existing specifications, when they describe behavior that is confirmed by the implementation.

### Source-of-truth rule

If documentation and application behavior disagree, the sales script must describe the behavior that is **actually implemented and available**.

If a feature is described in documentation but is not implemented or does not work, it must not be presented as an available feature.

Such functionality should instead be classified as:

* `Not implemented`
* `Partially implemented`
* `Known limitation`
* `Future feature`

as appropriate.

---

# 5. Sales Demonstration Script Structure

The `@docs/sales_script.md` document must be organized so that a demonstrator can follow it during a live product presentation.

The recommended structure is:

```text
# RSVR Sales Demonstration Script

## 1. Purpose and Audience

## 2. Demonstration Preparation

## 3. Recommended Demonstration Flow

### 3.1 Application Overview
### 3.2 Authentication and User Access
### 3.3 Main Navigation
### 3.4 Core Business Workflow
### 3.5 Data Management
### 3.6 Reporting and Visualization
### 3.7 Administration
### 3.8 Other Implemented Features

## 4. Feature Catalog

## 5. Business Rules

## 6. Feature Status and Known Gaps

## 7. Frequently Asked Feature Questions

## 8. New Feature Request Questionnaire

## 9. Feature Request Handoff to Development

## 10. Maintenance and Verification
```

The exact sections may be adjusted according to the actual features discovered in the application.

The document must not contain empty sections that do not apply to the current application.

---

# 6. Feature Demonstration Requirements

Each currently implemented feature included in the demonstration script should provide, when applicable:

| Information         | Description                                 |
| ------------------- | ------------------------------------------- |
| Feature             | Name of the feature                         |
| Purpose             | Business purpose of the feature             |
| User                | User role that can use the feature          |
| Preconditions       | Conditions required before demonstrating it |
| Navigation          | How to reach the feature                    |
| Demonstration steps | Ordered actions to demonstrate the feature  |
| Expected result     | Expected observable application behavior    |
| Business rules      | Rules enforced by the application           |
| Validation          | Relevant validation behavior                |
| Related features    | Other features connected to it              |
| Status              | Current implementation status               |
| Notes               | Important demonstration or business notes   |

The script should prioritize **observable application behavior** over technical implementation details.

Technical details may be included when they are relevant to explaining a feature, limitation, or integration, but the primary purpose is to support a business-oriented product demonstration.

---

# 7. Business Rules

For each relevant feature, the sales script must document the business rules that affect the user's experience.

Examples of business rules include:

* Required fields.
* Optional fields.
* Field validation.
* Allowed values.
* User permissions.
* Role-based access.
* Status transitions.
* Workflow constraints.
* Data dependencies.
* Calculation rules.
* Restrictions.
* Error conditions.
* Duplicate prevention.
* Record lifecycle rules.

Business rules must be derived from the current application implementation.

The sales script must avoid inventing business rules that are not enforced or represented by the current application.

---

# 8. Feature Status Classification

Every feature or capability mentioned in the sales script must have a clearly identifiable status.

The following statuses should be used:

| Status                  | Meaning                                                        |
| ----------------------- | -------------------------------------------------------------- |
| `Implemented`           | Available and working in the current application               |
| `Partially implemented` | Some functionality is available, but the feature is incomplete |
| `Known limitation`      | The functionality exists but has a documented limitation       |
| `Not implemented`       | The capability is not currently available                      |
| `Future feature`        | Identified as a potential future capability                    |

Only features with status `Implemented` should be presented as currently available product capabilities.

Partially implemented or limited functionality must be clearly disclosed during the demonstration.

---

# 9. Feature Lookup

The document must provide a concise feature catalog that allows the salesperson to quickly answer questions such as:

* Does RSVR support this feature?
* Where can I demonstrate it?
* Which user can access it?
* What business rules apply?
* Is it currently implemented?
* Is it a limitation or future feature?

The feature catalog should use a table similar to:

| Feature      | Status      | User/Role | Demonstration Location | Business Area |
| ------------ | ----------- | --------- | ---------------------- | ------------- |
| Feature name | Implemented | Role      | Application location   | Business area |

The catalog must reflect the actual features discovered in the application.

---

# 10. Missing and Future Features

The sales script must explicitly identify functionality that is not currently available when such functionality is known or discovered.

The document should provide a section such as:

```text
## Feature Gaps and Future Features
```

Each entry should contain, when known:

* Feature name.
* Current status.
* Business need.
* Current workaround, if any.
* Relevant notes.
* Potential next step.

The document must clearly distinguish between:

1. A feature that does not exist.
2. A feature that partially exists.
3. A feature that exists but has limitations.
4. A feature that has been proposed but has not yet been approved or specified.

The salesperson must never promise an unavailable feature as part of the current application.

---

# 11. Frequently Asked Feature Questions

The script should include a quick-reference section for common questions that a prospective user may ask during a demonstration.

Each question should have:

* The question.
* A concise answer.
* The feature status.
* A reference to the relevant section of the demonstration script.

Example:

```text
### Does RSVR support [feature]?

Answer:
[Current behavior based on the application implementation.]

Status:
Implemented / Partially implemented / Known limitation / Not implemented / Future feature

See:
[Relevant feature section]
```

The actual questions must be derived from the application's implemented capabilities and likely demonstration scenarios.

---

# 12. New Feature Request Questionnaire

The sales script must provide a concise questionnaire that allows the salesperson to capture enough information about a requested feature before sending it to the development team.

The questionnaire must ask concrete questions covering, at minimum:

1. **What feature is being requested?**
2. **Who needs the feature?**
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

The questionnaire should be concise enough to be used during or immediately after a sales conversation.

---

# 13. Feature Request Handoff

The collected answers must be structured so they can be transformed into a development request.

The script should provide a template similar to:

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

The resulting information should be suitable as an initial input for a future **Spec Kit specification workflow**.

The sales script itself must not be considered the final technical specification.

---

# 14. Demonstration Quality Requirements

The sales script must be:

* Accurate.
* Current.
* Easy to scan during a live demonstration.
* Written in clear business-oriented language.
* Consistent with the application's actual behavior.
* Explicit about limitations.
* Structured for quick feature lookup.
* Useful to both technical and non-technical audiences.
* Maintainable as the application evolves.

The demonstration steps must be written in a deterministic order wherever possible.

A demonstrator following the script should be able to reproduce the expected result without relying on undocumented knowledge.

---

# 15. Verification and Acceptance Criteria

## AC-01 — Current Feature Coverage

**Given** the current RSVR application source code and implementation,

**When** the sales demonstration script is reviewed,

**Then** it must document the relevant currently implemented user-facing features.

---

## AC-02 — Business Rule Coverage

**Given** a documented implemented feature,

**When** the sales script describes that feature,

**Then** the relevant implemented business rules and user-visible validations must be documented.

---

## AC-03 — Demonstration Flow

**Given** the sales demonstration script,

**When** a demonstrator follows the recommended demonstration flow,

**Then** the demonstrator must be able to present the application's implemented functionality in a logical sequence.

---

## AC-04 — Feature Lookup

**Given** a prospective user asks whether RSVR supports a specific capability,

**When** the demonstrator searches the feature catalog,

**Then** the demonstrator must be able to determine the feature's current status and locate the relevant demonstration or explanation.

---

## AC-05 — Feature Status Transparency

**Given** a feature is partially implemented, unavailable, limited, or planned,

**When** the feature is mentioned in the sales script,

**Then** its status must be explicitly identified.

---

## AC-06 — No Unsupported Claims

**Given** the current application implementation,

**When** the sales script is generated or updated,

**Then** it must not present unimplemented or unverified functionality as an available feature.

---

## AC-07 — Feature Gap Identification

**Given** the current application implementation and known product requirements,

**When** the sales script is reviewed,

**Then** missing, partially implemented, limited, or future functionality must be identifiable.

---

## AC-08 — Feature Request Capture

**Given** a prospective user requests a new feature,

**When** the salesperson uses the feature request questionnaire,

**Then** the questionnaire must capture enough concrete information to create an initial development requirement.

---

## AC-09 — Development Handoff

**Given** a completed feature request questionnaire,

**When** the information is handed to the development team,

**Then** the information must be structured so that it can be used as input for a future Spec Kit specification.

---

## AC-10 — Document Location

**Given** the sales demonstration script has been implemented,

**When** the repository is inspected,

**Then** the script must exist at:

```text
@docs/sales_script.md
```

---

## AC-11 — Maintainability

**Given** the RSVR application evolves,

**When** features or business rules change,

**Then** the sales script must provide a clear structure for updating the affected feature, business rule, status, and demonstration steps.

---

# 16. Definition of Done

This feature is complete when:

* [ ] `@docs/sales_script.md` exists.
* [ ] The current application implementation has been reviewed.
* [ ] Current user-facing features are documented.
* [ ] Relevant business rules are documented.
* [ ] A logical demonstration flow is available.
* [ ] A feature catalog is available for quick lookup.
* [ ] Feature statuses are explicitly identified.
* [ ] Known limitations and gaps are documented.
* [ ] Unimplemented functionality is not presented as available.
* [ ] A feature-request questionnaire is included.
* [ ] A feature-request handoff template is included.
* [ ] The resulting document is suitable as input for a future Spec Kit specification.
* [ ] The document has been reviewed for consistency with the actual application behavior.

