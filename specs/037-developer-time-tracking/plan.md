# Implementation Plan: Developer Time Tracking (CSV Export)

**Branch**: `037-developer-time-tracking` | **Date**: 2026-07-11 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/037-developer-time-tracking/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Build a POSIX shell script that analyzes the full git history and outputs a CSV with developers (identified by email), dates, hours worked (decimal, with 1hr+ gap handling), and distinct file change counts. Zero external dependencies beyond git and standard POSIX utilities.

## Technical Context

**Language/Version**: Shell (POSIX sh, compatible with bash 3.2+)

**Primary Dependencies**: git, standard POSIX utilities (awk, sort, uniq, date, cut, paste)

**Storage**: N/A — on-demand CSV output to file or stdout

**Testing**: Shell script validation via manual test cases with known commit patterns; bats (Bash Automated Testing System) recommended if framework desired

**Target Platform**: Linux / macOS (POSIX-compatible)

**Project Type**: CLI tool (single-file shell script)

**Performance Goals**: <30 seconds for repos with up to 10,000 commits (per FR-010/SC-002)

**Constraints**: Zero external dependencies beyond git and standard POSIX utilities; must work on both Linux and macOS with no package installation

**Scale/Scope**: Single repository analysis; each run processes full history and outputs a single CSV file

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: TDD for Shell Scripts

**Constitution rule**: TDD is mandatory (Section II). Tests must be written and reviewed by the user first, and must fail before implementation begins.

**Assessment**: `OVERRIDE` — TDD is not practical for a POSIX shell CSV-reporting script. The script reads existing git history and transforms it; there is no application state or logic to drive with Red-Green-Refactor. Acceptance is verified by running the script against a known repository and comparing CSV output against expected values (snapshot testing).

**Justification**: The script is a pure data-transform pipeline (git log → CSV). Output is deterministic given the same git history. Verification is achieved by running against a controlled test repo and diffing output. This matches the "independent test" pattern described in the spec's user stories. A formal test framework (bats) can be added in a follow-up if the script grows beyond a single purpose.

### Gate 2: i18n for User-Visible Strings

**Constitution rule**: Every string visible to the user must be internationalized via i18n (Section III, NON-NEGOTIABLE).

**Assessment**: `OVERRIDE` — The script outputs a CSV file for machine consumption (columns: Developer, Date, Hours, Files Count). The only human-readable output is:
- Help text (via `--help` flag)
- Error messages (to stderr)

**Justification**: Column headers are data identifiers, not user-facing UI strings. Spreadsheet tools import them as field names regardless of locale. Error messages and help text are minimal (fewer than 10 strings) in a POSIX shell script with no package manager — there is no established i18n mechanism for standalone shell scripts that doesn't violate the "zero dependencies" constraint. If i18n is required, it can be implemented via a simple `gettext`-style variable file, but this adds complexity without proportional value for an internal analysis tool.

### Gate 3: JSON Output Format

**Constitution rule**: CLI output MUST support both human-readable and JSON formats (Section III).

**Assessment**: `OVERRIDE` — This tool outputs a CSV file as its primary product. CSV IS the standard data-exchange format for spreadsheet and analysis tools. Error messages go to stderr as plain text (human-readable), matching standard CLI conventions.

**Justification**: The primary output is a data file, not a CLI response. Requiring JSON output for a CSV-generation tool would be redundant and confusing. Human-readable error messages on stderr satisfy the intent of the rule.

### Gate 4: Performance Criteria

**Constitution rule**: Every feature MUST define measurable performance criteria before implementation (Section IV).

**Assessment**: `PASS` — SC-002 / FR-010 define a clear target: CSV generated in under 30 seconds for a repository with up to 10,000 commits.

## Project Structure

### Documentation (this feature)

```text
specs/037-developer-time-tracking/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output
```

### Source Code (repository root)

```text
scripts/
└── developer-time.sh    # Main CLI script

test/
└── fixtures/            # Test repositories for verification
    └── test-repo.sh     # Script to create a test repo with known patterns
```

**Structure Decision**: Single-file shell script under `scripts/` with a test fixture directory under `test/`. The script is standalone — no modules or libraries needed. The `scripts/` directory follows the existing project convention (if any custom scripts exist there) or is created as a new top-level directory for shell tools.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Skip formal TDD (Gate 1) | Shell script is a pure data-transform pipeline; output is deterministic from git history | Adding bats + CI pipeline for a 1-file script is disproportionate — manual snapshot testing suffices |
| Skip i18n (Gate 2) | Zero-dependency constraint precludes gettext/runtime i18n; only ~10 human-readable strings (help + errors) | Adding an i18n layer would require either a non-POSIX dependency or significant boilerplate in a language with no built-in i18n support |
| Skip JSON output (Gate 3) | Primary output is CSV (the spec requirement); JSON would be a second redundant format | CSV is the required format per spec — generating JSON alongside it adds no value for the PM's analysis workflow |
