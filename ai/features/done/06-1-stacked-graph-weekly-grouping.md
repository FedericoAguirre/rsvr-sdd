# 6-1. Create the stacked graph for weekly grouping

## User story

As an administrator, I want to view payment data as a stacked bar chart grouped by ISO week, so that I can visualize weekly payment trends across different payment types at a glance.

## Acceptance criteria

Given I am on the payment reports page with weekly grouping selected, When the chart renders, Then each bar represents an ISO week with stacked segments for each payment type.

Given the chart displays data for multiple weeks, When I hover over a bar segment, Then I see a tooltip showing the payment type, total amount, and count for that week and type.

Given there are payments of different types on the same week, When the chart renders, Then each payment type is represented by a distinct color in the stacked bar. The week is labeled with the Monday date in YYYYMMDD format.

Given I select a "Start date", When the query runs, Then the real start date is the closest backwards Monday (the Monday of that week, or the same day if it is already Monday).

Given I select an "End date", When the query runs, Then the real end date is the closest forward Sunday (the Sunday of that week, or the same day if it is already Sunday).

Given I select a Start date and End date that span partial weeks, When the chart renders, Then only full ISO weeks within the adjusted range are shown.

Given the data contains no payments for a particular week, When the chart renders, Then that week is omitted from the x-axis rather than showing an empty bar.

Given the stack is rendered, When the chart renders, Then that stack shows the total amount on top of it.

Given I view the chart on different screen sizes, When the chart renders, Then it remains responsive and readable without horizontal scrolling.

## Definition of Done

- Chart.js stacked bar chart implemented in payment_reports.html for weekly grouping
- Start date adjusted to closest backwards Monday (inclusive)
- End date adjusted to closest forward Sunday (inclusive)
- X-axis displays Monday dates in YYYYMMDD format for each ISO week
- Y-axis displays payment amounts
- Each payment type shown as a distinct colored segment in stacked bars
- Tooltips display payment type, total amount, and count
- Weekly totals are shown on the stack tops
- Y-axis shows divisory lines
- Empty weeks are excluded from the chart
- Chart is responsive and works on mobile/desktop
- Existing tests pass for report data structure
