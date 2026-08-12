# Research: Batch Reservation Date Alignment

## Decision: Group dates by calendar week and weekday position

- **Decision**: Build each rendered week from a Monday-based calendar bucket, placing each valid weekday date at its `isoDow` position and leaving leading/trailing positions empty when the range does not cover them.
- **Rationale**: The current renderer filters weekends and then slices the remaining dates into groups of five. If the range starts on Tuesday, the first Tuesday becomes the first item in a row headed by Monday, creating the reported misalignment. Calendar-week grouping preserves the date's actual weekday without changing the date value.
- **Alternatives considered**: Keep sequential five-item slicing; rejected because it fails whenever the range starts midweek or contains filtered dates. Add a new backend endpoint or precomputed grid; rejected because the existing `date_range` data already contains enough information and the defect is presentation-only.

## Decision: Preserve the existing batch reservation contract

- **Decision**: Keep `date_range.start`, `date_range.end`, `class_slots`, `reserved_dates`, and the batch-create `dates` payload unchanged.
- **Rationale**: The backend already calculates the eligible start date, end date, payment-day cutoff, class-slot availability, and exact-date validation. Changing the contract would increase scope without addressing the rendering defect.
- **Alternatives considered**: Add weekday metadata or server-rendered calendar cells; rejected unless frontend tests prove the existing ISO date values are insufficient.

## Decision: Use the existing translated weekday labels

- **Decision**: Continue deriving weekday headers from the existing translated `dayAbbrs` JSON element and use numeric Monday-based positions internally.
- **Rationale**: The project already provides localized weekday labels and the backend uses Python's Monday=`0` convention. Reusing both avoids new strings and locale inconsistencies.
- **Alternatives considered**: Add new translation keys or derive labels from browser locale; rejected because this would duplicate existing i18n behavior.

## Decision: Test both boundary alignment and unchanged submission values

- **Decision**: Add regression coverage for ranges starting on each non-Monday weekday and verify the selected date values remain exact ISO dates.
- **Rationale**: Correct visual placement alone is insufficient if selection changes the submitted date. The test must cover both the row/column position and the payload contract.
- **Alternatives considered**: Test only Monday starts; rejected because Monday starts do not expose the defect.
