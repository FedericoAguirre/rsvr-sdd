# Quickstart: Cardio Equipment Reservation

## Prerequisites

- Docker and Docker Compose installed
- uv installed (Python package manager)

## Setup

```bash
# 1. Clone and enter the project
git clone <repo-url> && cd rsvr-sdd

# 2. Start services
docker compose up -d

# 3. Create and apply migrations
docker compose exec web python manage.py makemigrations clients equipment classes reservations
docker compose exec web python manage.py migrate

# 4. Seed initial data (class schedule + sample equipment)
docker compose exec web python manage.py seed_data

# 5. Create admin user
docker compose exec web python manage.py createsuperuser

# 6. Open in browser
open http://localhost:8000
```

## Development

```bash
# Run tests
docker compose exec web python -m pytest

# Run linting
docker compose exec web ruff check .

# Create migrations after model changes
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Access Django shell
docker compose exec web python manage.py shell

# View logs
docker compose logs -f
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | postgres://rsvr:rsvr@db:5432/rsvr | PostgreSQL connection |
| DEBUG | True | Django debug mode |
| SECRET_KEY | (auto-generated) | Django secret key |
| ALLOWED_HOSTS | * | Allowed host header values |

## Data Seeding

Run `python manage.py seed_data` to populate:
- 10 class slots (Mon-Fri × 17:30, 18:30)
- 5 sample equipment items (2 treadmills, 2 bikes, 1 elliptical)

## Notes

- Equipment marked "out of service" with future reservations: the quickstart
  flag lists impacted reservations for manual admin review.
- Operator accounts are created via Django admin interface.
- Client accounts do NOT have login access — operators look them up by
  email/mobile.
