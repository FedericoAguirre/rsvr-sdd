# CLI Requirements Checklist: Developer Time Tracking (CSV Export)

**Purpose**: Validate completeness, clarity, and consistency of CLI tool requirements before code review
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)

## CLI Contract Completeness

- [ ] CHK001 Are all CLI arguments (`-o`, `--help`) and their behavior explicitly specified? [Completeness, Spec §FR-001, FR-008, FR-011]
- [ ] CHK002 Are all exit codes documented with their meaning? [Completeness, Spec §FR-012]
- [ ] CHK003 Is the behavior for unrecognized flags specified? [Completeness, Gap — Spec does not define behavior for unknown flags beyond "Error: Unknown option"]
- [ ] CHK004 Is the behavior for supplying `-o` without a path argument specified? [Completeness, Spec §FR-011]
- [ ] CHK005 Are the output path default and overwrite behavior specified? [Clarity, Spec §FR-011 — "developer-time.csv" default defined, but overwrite behavior not specified]

## Data Accuracy Requirements

- [ ] CHK006 Is the work block detection threshold explicitly quantified in seconds? [Clarity, Spec §FR-004 — "gap of one hour or more" = 3600 seconds implied but not stated]
- [ ] CHK007 Is the hours calculation precision specified (number of decimal places)? [Clarity, Spec §FR-003 — decimal format specified but precision not defined]
- [ ] CHK008 Is the file counting behavior for renamed files specified? [Clarity, Spec §FR-006 — "distinct files" defined but rename tracking unclear]
- [ ] CHK009 Is the behavior for binary file changes specified? [Coverage, Spec Edge Case — listed as edge case but no FR defines behavior]
- [ ] CHK010 Is the timezone handling for commit timestamps explicitly specified? [Clarity, Spec §FR-004 — "gap of one hour" not clarified as UTC or local time]
- [ ] CHK011 Is the past-midnight commit day attribution rule specified as a requirement? [Completeness, Spec — mentioned in US2 acceptance but not as an FR]

## Output Format Requirements

- [ ] CHK012 Is the CSV header casing explicitly specified? [Clarity, Spec §FR-003 — "Files Count" vs "Files Count" defined but case could be ambiguous]
- [ ] CHK013 Is the CSV delimiter specified (comma vs semicolon)? [Clarity, Spec §FR-003 — comma delimiter implied but not stated]
- [ ] CHK014 Is the CSV quoting behavior for special characters specified? [Gap, Spec §FR-003 — no quoting strategy documented]
- [ ] CHK015 Is the row sort order within the CSV specified? [Completeness, Spec — date then developer sort not explicitly defined in FRs]
- [ ] CHK016 Is the output encoding specified? [Gap — UTF-8 assumed but not stated]

## Error Handling Requirements

- [ ] CHK017 Is the error message format specified (consistency)? [Clarity, Spec §FR-012 — "Error:" prefix implied but not formalized]
- [ ] CHK018 Are error messages for all failure modes specified (no git repo, no commits, bad args, git failures)? [Completeness, Spec §FR-009/FR-012]
- [ ] CHK019 Is the behavior when the output path is not writable specified? [Gap — permission denied scenario not covered]
- [ ] CHK020 Are distinct exit codes defined for different error categories? [Clarity, Spec §FR-012 — exit codes 1 and 2 defined, but other failure modes not mapped]

## Edge Case Coverage

- [ ] CHK021 Is the single-commit scenario explicitly handled in requirements? [Coverage, Spec Edge Case — "0 hours" for single commit defined as edge case but not an FR]
- [ ] CHK022 Is the empty repository behavior fully specified (headers only vs message)? [Completeness, Spec §FR-009 — "headers only or a clear message" is ambiguous]
- [ ] CHK023 Are requirements for handling author name collisions (same email, different names) specified? [Gap — not addressed]
- [ ] CHK024 Are requirements for non-ASCII characters in file paths or author names specified? [Gap — not addressed]
- [ ] CHK025 Is the behavior for merge commits with no file changes specified? [Gap — listed as Edge Case but no FR defines 0-hour rows]
- [ ] CHK026 Are performance targets for large repositories quantified? [Clarity, Spec §FR-010 — "30 seconds for 10,000 commits" is clear]

## Cross-Platform Requirements

- [ ] CHK027 Are platform-specific considerations for awk/GNU date differences specified? [Completeness, Assumptions — macOS/Linux mentioned in Assumptions but not as FRs]
- [ ] CHK028 Is the minimum supported shell version specified? [Clarity, Plan §Tech — "bash 3.2+" in plan but not in spec]
- [ ] CHK029 Are requirements for Windows/WSL support specified or explicitly excluded? [Clarity, Spec Assumptions — "acceptable but not a primary target" is vague]

## Dependency & Constraints

- [ ] CHK030 Are all required system utilities explicitly listed? [Completeness, Spec §FR-007 — "sh/awk/sed/git" but not exhaustive]
- [ ] CHK031 Is the zero-dependency constraint testable? [Acceptance Criteria, Spec §FR-007 — "only standard shell commands" is clear]

## Ambiguities & Conflicts

- [ ] CHK032 Is the definition of "gap of one hour" unambiguous — is it >= 1 hour or > 1 hour? [Ambiguity, Spec §FR-005 — "one hour or more" used in text vs spec acceptance scenario]
- [ ] CHK033 Is the handling of multiple commits with the exact same timestamp specified? [Gap — not addressed in spec]
- [ ] CHK034 Are the requirements for `--help` output format (stdout vs stderr) consistent? [Consistency, Spec §FR-008 — help to stdout in acceptance, but usage() writes to stdout only]

## Notes

- Items with [Gap] markers indicate requirements not fully specified — consider updating the spec before final review
- Items with [Ambiguity] markers indicate requirements that could be interpreted in multiple ways
- Items with [Clarity] markers indicate requirements that exist but need more precision
