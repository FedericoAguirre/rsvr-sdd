# URL Contracts: Cardio Equipment Reservation

## Authentication

| Method | URL | Description |
|--------|-----|-------------|
| GET | /accounts/login/ | Login form |
| POST | /accounts/login/ | Authenticate staff user |
| GET | /accounts/logout/ | Logout |

## Client Management

| Method | URL | Description |
|--------|-----|-------------|
| GET | /clients/search/ | Search clients by email or mobile |
| GET | /clients/<id>/ | Client detail + reservation history |
| GET | /clients/create/ | Create new client |
| POST | /clients/create/ | Submit new client form |

## Equipment Management (Admin)

| Method | URL | Description |
|--------|-----|-------------|
| GET | /equipment/ | Equipment list |
| GET | /equipment/<id>/ | Equipment detail |
| GET | /equipment/create/ | Add new equipment |
| POST | /equipment/create/ | Submit new equipment |
| GET | /equipment/<id>/edit/ | Edit equipment |
| POST | /equipment/<id>/edit/ | Submit equipment edit |

## Class Schedule (Admin)

| Method | URL | Description |
|--------|-----|-------------|
| GET | /classes/ | Class schedule view |
| GET | /classes/<id>/toggle/ | Toggle slot active/inactive |

## Reservations (Operator)

| Method | URL | Description |
|--------|-----|-------------|
| GET | /reservations/ | Reservation dashboard (by date) |
| GET | /reservations/create/ | Create reservation form |
| POST | /reservations/create/ | Submit reservation |
| GET | /reservations/<id>/ | Reservation detail |
| GET | /reservations/?date=YYYY-MM-DD | Filter by date |
| GET | /reservations/?client=<id> | Filter by client |

## Responses

All views return HTML (Django templates with Bootstrap). Errors return
appropriate HTTP status codes with user-friendly error pages:
- 200: Success
- 302: Redirect after POST (PRG pattern)
- 403: Forbidden (unauthorized role)
- 404: Resource not found
