# Contracts: Reservation Status

## Overview

This feature adds a new URL endpoint for changing reservation status and modifies the response context of existing views to include status information.

## Existing Endpoints (Modified)

All existing reservation endpoints now include `status` in their response context:

| Method | URL Pattern | View | Changes |
|--------|-------------|------|---------|
| GET | `/reservations/` | `reservation_list` | Status displayed in list table |
| GET | `/reservations/list/` | `reservation_list_by_slot` | Status displayed in list table |
| GET | `/reservations/list/pdf/` | `reservation_list_pdf` | Status column in PDF export |
| GET | `/reservations/<pk>/` | `reservation_detail` | Status displayed + action buttons |

## New Endpoint

| Method | URL Pattern | View Name | Description |
|--------|-------------|-----------|-------------|
| POST | `/reservations/<pk>/status/` | `reservation-change-status` | Change reservation status |

### POST Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | yes | New status value: `reserved`, `used`, or `unused` |

### Response

- **Success**: Redirects to reservation detail page with a success message
- **Error (invalid status)**: Redirects back with an error message
- **Error (unauthenticated)**: 302 redirect to login page
- **Error (not staff)**: 403 Forbidden

## Authentication & Authorization

All endpoints require an authenticated user with `is_staff=True` (Operator or Administrator role).
