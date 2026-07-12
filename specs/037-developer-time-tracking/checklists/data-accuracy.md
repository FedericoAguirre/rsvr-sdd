# Data Accuracy Requirements Checklist: Developer Time Tracking (CSV Export)

**Purpose**: Validate quality, completeness, and clarity of data accuracy requirements (hours calculation, gap detection, file counting)
**Created**: 2026-07-11
**Feature**: [spec.md](../spec.md)

## Hours Calculation Completeness

- [ ] CHK001 Is the work block detection algorithm fully specified for all group sizes (1, 2, and 3+ commits)? [Completeness, Spec §FR-004/FR-005 — the 2-commit exception is implemented but not explicitly stated in FRs]
- [ ] CHK002 Is the rule for handling commits with identical timestamps specified? [Gap — Spec does not define behavior for concurrent commits]
- [ ] CHK003 Is the single-commit-day hours rule (0 hours) documented as a functional requirement? [Coverage, Spec Edge Case — mentioned in Edge Cases but not in FRs]
- [ ] CHK004 Are the past-midnight session rules specified in the Functional Requirements section? [Completeness, Spec US2 Acceptance #4 — specified in acceptance criteria but not as an FR]
- [ ] CHK005 Is the merge commit hours behavior specified (0 hours, 0 files or excluded)? [Gap — Spec Edge Case lists binary files but does not address merge commits with no changes]

## Hours Calculation Clarity

- [ ] CHK006 Is the gap threshold quantified in seconds rather than "one hour"? [Clarity, Spec §FR-005 — now says "3600 seconds (1 hour)" after clarification]
- [ ] CHK007 Is the timezone basis for gap detection specified (UTC vs local time)? [Clarity, Spec §FR-004 — "gap of one hour" not clarified as UTC or commit-author-timezone]
- [ ] CHK008 Is the 2-commit exception rule explicitly documented in the spec? [Gap — the decision that 2 commits use simple span was made during implementation but not recorded in FRs]
- [ ] CHK009 Is the minimum hours duration for a single-commit block specified? [Clarity, Spec Edge Case — "0 hours for that developer-date (or a minimal duration)" is ambiguous: "or a minimal duration" introduces uncertainty]
- [ ] CHK010 Is the hours rounding/truncation strategy specified? [Gap — FR-003 says "decimal" but does not specify whether hours are rounded, truncated, or displayed to fixed precision]

## File Counting Completeness

- [ ] CHK011 Is the behavior for file renames (same inode, different path) specified? [Clarity, Spec §FR-006 — "distinct files" defined but rename tracking scope is unclear]
- [ ] CHK012 Is the behavior for binary file changes specified as an FR rather than just an Edge Case? [Coverage, Spec Edge Case — listed as edge case but no FR exists]
- [ ] CHK013 Is the behavior for symlink changes specified? [Gap — not addressed in spec]
- [ ] CHK014 Is the handling of deleted-only commits (no created/modified files) specified? [Gap — not addressed in spec]

## File Counting Clarity

- [ ] CHK015 Does FR-006 specify whether "created or modified" includes deletions, renames, or permission changes? [Clarity, Spec §FR-006 — "created or modified" is clear but no mention of deletions or renames]
- [ ] CHK016 Is the counting behavior for submodule changes specified? [Gap — not addressed]

## Gap Detection Consistency

- [ ] CHK017 Do FR-005 (gap threshold) and FR-004 (work block definition) use consistent wording? [Consistency, Spec §FR-004/FR-005 — both now use "3600 seconds (1 hour)" after clarification]
- [ ] CHK018 Is the gap threshold consistent between FR-005 ("3600 seconds or more") and the acceptance criteria descriptions? [Consistency, Spec §FR-005 vs US2 — "no gap >1hr" in acceptance could be read as strictly greater than]
- [ ] CHK019 Are edge case descriptions for "multiple timezones" consistent with the gap detection algorithm? [Consistency, Spec Edge Case — timezone handling for gap detection is unclear]

## Acceptance Criteria Measurability

- [ ] CHK020 Can acceptance criteria for gap detection be objectively tested without implementation knowledge? [Acceptance Criteria, Spec US2 — scenarios 1-3 are well-defined with specific timestamps and expected hours]
- [ ] CHK021 Is SC-003 ("within 1 minute precision") clearly testable across all scenarios? [Measurability, Spec §SC-003 — "1 minute precision" is measurable but does not specify whether this applies per-block or per-day]
- [ ] CHK022 Does the spec define how to construct a controlled test repository to validate accuracy? [Gap — SC-003 references "controlled test repository" but no specific test data requirements]

## Scenario Coverage

- [ ] CHK023 Are requirements specified for the exactly-3600-seconds-gap boundary case? [Coverage, Gap — the >= threshold means a gap of exactly 3600s splits blocks, but no acceptance scenario tests this boundary]
- [ ] CHK024 Are requirements specified for multiple developers on the same date with overlapping work blocks? [Coverage, Gap — each developer is independent but overlapping timestamps could affect date attribution]
- [ ] CHK025 Are requirements specified for repositories where the same developer has multiple author emails? [Coverage, Spec Assumptions — email is unique identifier, so multiple emails = multiple rows, but this is an assumption not an FR]
- [ ] CHK026 Are requirements specified for hours calculation when commits span multiple days? [Coverage, Spec US2 #4 — past-midnight is covered, but multi-day sessions not fully addressed]

## Notes

- Items with [Gap] markers indicate missing requirements — consider adding before finalizing
- Items with [Clarity] markers indicate existing requirements that need more precision
- The spec was recently clarified (Session 2026-07-11 Implementation) for CSV quoting, overwrite behavior, and gap threshold — some items may now be partially addressed
