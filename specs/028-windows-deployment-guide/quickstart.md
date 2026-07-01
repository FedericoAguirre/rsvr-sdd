# Quickstart: Windows 11 Home Deployment

## Prerequisites

- Windows 11 Home laptop with admin access
- Internet connection
- No Docker/containers required

## Installation Steps

1. **Install Python 3.12+** from [python.org](https://python.org)
2. **Install PostgreSQL 16+** from [EDB installer](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
3. **Clone the project** and `cd` into it
4. **Create `.env`** from template with database URL, secret key, media path
5. **Install dependencies**: `pip install -r requirements.txt`
6. **Create database** and run migrations
7. **Run**: `waitress-serve --host=0.0.0.0 --port=8000 project.wsgi:application`

## Post-Reboot

Run the launcher script or use Task Scheduler to auto-start on boot.

## Firewall

```powershell
netsh advfirewall firewall add rule name="Web App" dir=in action=allow protocol=TCP localport=8000
```

## Links

- Full guide: [docs/windows11_deployment.md](../../docs/windows11_deployment.md)
