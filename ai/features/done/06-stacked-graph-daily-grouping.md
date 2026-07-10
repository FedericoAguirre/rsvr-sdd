# 6. Create the stacked graph for daily grouping

## User story

As an administrator, I want to view payment data as a stacked bar chart grouped by day, so that I can visualize daily payment trends across different payment types at a glance.

## Acceptance criteria

Given I am on the payment reports page with daily grouping selected, When the chart renders, Then each bar represents a single day with stacked segments for each payment type.

Given the chart displays data for multiple days, When I hover over a bar segment, Then I see a tooltip showing the payment type, total amount, and count for that day and type.

Given there are payments of different types on the same day, When the chart renders, Then each payment type is represented by a distinct color in the stacked bar. The day is labeled as YYYYMMDD.

Given the data contains no payments for a particular day, When the chart renders, Then that day is omitted from the x-axis rather than showing an empty bar.

Given the stack is rendered, When the chart renders, Then that stack shows the total amount on top of it.

Given I view the chart on different screen sizes, When the chart renders, Then it remains responsive and readable without horizontal scrolling.

## Definition of Done

- Chart.js stacked bar chart implemented in payment_reports.html
- X-axis displays dates (days as YYYYMMDD), Y-axis displays payment amounts
- Each payment type shown as a distinct colored segment in stacked bars
- Tooltips display payment type, total amount, and count
- Daily totals are shown on the stack tops
- Y-axis shows divisory lines
- Empty days are excluded from the chart
- Chart is responsive and works on mobile/desktop
- Existing tests pass for report data structure
