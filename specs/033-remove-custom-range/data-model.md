# Data Model: Remove Custom Range

**No changes to data model.** This feature removes the `range` grouping option from the reports page. The `range` case in the `PaymentReportView` is a pure code path that queries the same data model with the same aggregation as `day` grouping. No schema changes, model changes, or new fields are required.
