# ClassPrice

## Summary

Implement a versioned price tracking system for classes that maintains complete audit history, prevents deletion, and enables administrators to monitor all price changes with full attribution and timestamps.

## User Story

As an administrator, I want to track class price changes so I can see the last price, when it was changed, and when it became inactive.

## Acceptance Criteria

### Price Version Management
- When a new price is entered into the system, the previous price record is marked as inactive (no longer current)
- A change date is automatically recorded when a price transitions to inactive
- A new price record is created with the current date and marked as the active price

### Attribution & Audit Trail
- The system records the user who entered or changed each price
- Every price record includes creation metadata (who, when)
- Every price record includes change metadata (who, when) when superseded

### Display & Ordering
- On the class prices view page, all prices are displayed in descending order (most recent first)
- The currently active price is clearly indicated with a flag or visual indicator

### Data Integrity
- Class prices cannot be deleted from the database
- All historical price records remain immutable and queryable
- The system enforces referential integrity between active and inactive price records

## Definitions

### Class Price Record
A versioned data structure containing:
- Price amount (decimal value)
- Effective date (when this price version became active)
- Change date (when this price was superseded or marked inactive)
- Current flag (boolean indicating if this is the active price)
- Created by (user ID or username of who entered this price)
- Created at (timestamp of record creation)
- Updated at (timestamp of last modification, tracking when marked inactive)

### Current Price
The single price record marked with `current = true` for any given class at any point in time. Only one current price can exist per class.

### Inactive Price
Any price record marked with `current = false`. These records are permanently retained and queryable for historical and audit purposes.

### Audit Trail
The complete immutable history of all price records for a class, including who made each change and when.

## Implementation Constraints

### Data Model Requirements
- Create or extend a `class_prices` table with versioning support
- Include columns for: `id`, `class_id`, `price`, `current`, `created_by`, `created_at`, `changed_at`, `updated_at`
- Ensure the table has appropriate indexes on `class_id` and `current` for query performance
- Add a unique constraint to ensure only one active price per class at a time

### Business Logic
- Price creation must be an atomic transaction:
  1. Mark existing current price as inactive and set `changed_at`
  2. Create new price record with `current = true`
  3. Record the user performing the action
- Price updates must never allow modification of historical records
- Deletion attempts must fail with a clear error message

### Display Logic
- Query active and inactive prices separately or with appropriate filtering
- Sort results by `created_at` in descending order for historical view
- Include user attribution in all price displays
- Highlight or badge the current price in UI

## Out of Scope

- Price forecasting or predictive analytics
- Bulk price uploads (initial implementation)
- Scheduled price changes (future enhancement)
- Price change notifications to students or instructors

## Related Considerations

### Future Enhancements
- Audit log export functionality
- Price change notifications
- Reason/note field for price changes
- Approval workflow for price changes
- Price change impact analysis (affected classes, revenue projections)

### Security & Permissions
- Only authorized administrators can change class prices
- All price changes are logged for compliance and audit purposes
- Historical access should be restricted by role and permissions
