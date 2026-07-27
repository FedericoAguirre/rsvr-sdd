# AI development data collection

## User story

As a software quality auditor, I want to get a data table, so that I can identify bottlenecks and inefficiencies in the AI-assisted SDLC process.

## Inputs

- `ai/features/done/` — completed feature files
- `specs/features/specs.md` and related spec files
- `ai/sessions/` — session logs

## Output

A CSV file with the following columns:

- `feature`
- `complexity`
- `minutes`
- `model`
- `start_timestamp`
- `end_timestamp`
- `specs_quality`
- `iterations`

## Column definitions

**Feature**. The title (`#`) in the file from the `ai/features/done` folder.

**Complexity**. The feature implementation complexity, measured in story points: 1, 2, 3, 5, or 8.
- **1**: Simple requests resolved with only a `/speckit.specify` command, a quick direct prompt, or a single task.
- **2**: Similar to 1, but specs needed 1–2 clarifications.
- **3**: Feature needed multiple clarifications and tasks, plus a review after implementation.
- **5**: Feature needed clarifications, multiple tasks, and 2+ reviews.
- **8**: Same as 5, but also included bug fixes or multiple specification adjustments.

**Minutes**. The minutes taken to implement the feature, from the first `/speckit.specify` command to the PR or merge command.

**Model**. The AI model used. Found in `ai/sessions/` from the corresponding feature file.

**Start timestamp**. The timestamp when `/speckit.specify` was issued.

**End timestamp**. The timestamp when the feature was sent for PR or merged to main.

**Specs quality**. How useful the specs were, rated 1–5:
- **1**: Only description
- **2**: 1 + acceptance criteria
- **3**: 2 + constraints
- **4**: 3 + examples
- **5**: 4 + other elements not included above.

**Iterations**. The number of `/speckit.specify` calls or AI calls after `/speckit.implement`.

## Acceptance criteria

Given I am a software quality auditor, when I request the data table, then I receive a valid CSV file with the specified columns.

Given the `ai/features/done` folder contains feature files, when the CSV is generated, then each feature appears as a row with data from specs, session logs, and feature files.

Given the CSV is generated, when I inspect it, then every row has all required columns filled (`feature`, `complexity`, `minutes`, `model`, `start_timestamp`, `end_timestamp`, `specs_quality`, `iterations`).

Given column definitions are documented, when reading a value, then it follows the definition rules (e.g., complexity is 1, 2, 3, 5, or 8; specs_quality is 1–5).

## Definition of Done

- A management command exists that generates the CSV from existing data sources (`ai/features/done/`, `specs/`, `ai/sessions/`).
- CSV generation works on real project data and all columns are populated correctly.
- Tests pass for the management command.
- Code is reviewed and merged to main.
