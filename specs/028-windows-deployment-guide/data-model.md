# Data Model: Windows Deployment Guide

## Deployment Guide Document Structure

The `docs/windows11_deployment.md` file follows this section structure:

| Section | Content | References |
|---------|---------|------------|
| Prerequisites | Software checklist, admin rights, internet connection | FR-002 |
| Security Configuration | Windows Defender exclusions, firewall rules, UAC | FR-002 |
| RDBMS Installation | PostgreSQL download, installer walkthrough, service verification | FR-003 |
| Python Runtime | Python installer, PATH configuration, version verification | FR-004 |
| Project Setup | Clone repo, create `.env`, install dependencies | FR-004, FR-005 |
| Database Initialization | Create database, run migrations, verify connection | FR-003 |
| File Uploads Storage | Create `media/` directory, set ownership, configure path | FR-009 |
| Firewall Configuration | Inbound port rule creation via `netsh` | FR-007 |
| Running the App | Waitress server command, binding, testing in browser | FR-006 |
| Startup on Boot | Task Scheduler setup, launcher script | FR-008 |
| Troubleshooting | Common errors, port conflicts, permission issues | Edge Cases |
| Links | Official downloads, documentation references | FR-010 |

## Key Configuration Variables (`.env`)

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgres://user:pass@localhost:5432/dbname` |
| `SECRET_KEY` | Django secret key | Generated via `python -c "..."` |
| `MEDIA_ROOT` | File uploads directory | `C:\projects\rsvr-sdd\media` |
| `ALLOWED_HOSTS` | Host/domain whitelist | `localhost,192.168.1.100` |
| `DEBUG` | Debug mode toggle | `False` (production) / `True` (development) |

## Files Touched

| File | Action | Purpose |
|------|--------|---------|
| `docs/windows11_deployment.md` | Create | Deployment guide content |
| `README.md` | Edit | Add link to deployment guide |
