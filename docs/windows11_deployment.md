# Windows 11 Home — Deployment Guide

This guide explains how to deploy the reservation system web application on a **Windows 11 Home** laptop without using containers (Docker, Podman, etc.).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Security Configuration](#security-configuration)
3. [Install PostgreSQL (RDBMS)](#install-postgresql-rdbms)
4. [Install Python Runtime](#install-python-runtime)
5. [Project Setup](#project-setup)
6. [Initialize the Database](#initialize-the-database)
7. [Configure File Uploads Storage](#configure-file-uploads-storage)
8. [Configure Windows Firewall](#configure-windows-firewall)
9. [Run the Web Application](#run-the-web-application)
10. [Start the App After Restart](#start-the-app-after-restart)
11. [Troubleshooting](#troubleshooting)
12. [Links & References](#links--references)

---

## Prerequisites

Before starting, ensure the following:

- **Windows 11 Home** laptop (not Pro, Enterprise, or Server)
- **Administrator access** to install software
- **Stable internet connection** to download prerequisites
- **At least 4 GB of free disk space**
- No Docker or container runtime required

### Software Checklist

| Software | Version | Purpose |
|----------|---------|---------|
| PostgreSQL | 16 or later | Database server |
| Python | 3.12 or later | Application runtime |
| Git | Latest | Version control (optional for cloning) |

---

## Security Configuration

### Windows Defender Antivirus

Windows Defender is enabled by default on Windows 11 Home. You do **not** need to disable it.

If Windows Defender flags the Python or PostgreSQL installer as unrecognized:

1. Click **"More info"** on the SmartScreen prompt
2. Click **"Run anyway"**
3. The installers are signed by their respective vendors (Python Software Foundation, EDB)

### User Account Control (UAC)

UAC prompts are expected during installer execution. Accept them when prompted. You need to be logged in with an account that has **Administrator** privileges.

### Windows Firewall

An inbound firewall rule for the web application port will be created later in this guide (see [Firewall Configuration](#configure-windows-firewall)).

---

## Install PostgreSQL (RDBMS)

1. **Download the installer** from the official EDB website:
   - Go to [https://www.enterprisedb.com/downloads/postgres-postgresql-downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
   - Select the latest **PostgreSQL 16** (or newer) for **Windows x86-64**

2. **Run the installer**:
   - Accept the license agreement
   - Choose installation directory (default: `C:\Program Files\PostgreSQL\16`)
   - Select components: **PostgreSQL Server**, **pgAdmin 4**, **Command Line Tools**
   - Set a password for the `postgres` superuser — **save this password**
   - Port: **5432** (default)
   - Locale: Leave as default or select your region

3. **Verify the installation**:
   ```powershell
   psql --version
   ```
   Expected output: `psql (PostgreSQL) 16.x`

4. **Ensure PostgreSQL service is running**:
   ```powershell
   Get-Service postgresql*
   ```
   The status should show **Running**. If not, start it:
   ```powershell
   Start-Service postgresql*
   ```

---

## Install Python Runtime

1. **Download Python 3.12+** from [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Choose the **Windows installer (64-bit)**

2. **Run the installer**:
   - **IMPORTANT**: Check **"Add Python to PATH"** at the bottom of the installer
   - Click **"Install Now"**
   - If prompted, accept the UAC prompt

3. **Verify the installation**:
   ```powershell
   python --version
   ```
   Expected output: `Python 3.12.x`

4. **Verify pip is available**:
   ```powershell
   pip --version
   ```

---

## Project Setup

### 1. Clone or Copy the Project

Clone the repository:
```powershell
git clone <repository-url> C:\projects\rsvr-sdd
cd C:\projects\rsvr-sdd
```

Or copy the project folder to `C:\projects\rsvr-sdd`.

### 2. Create the `.env` File

Create a file named `.env` in the project root (`C:\projects\rsvr-sdd\.env`).

Use the following template:

```ini
# PostgreSQL connection — change credentials as needed
DATABASE_URL=postgres://postgres:your-password-here@localhost:5432/rsvr

# Django security
SECRET_KEY=generate-a-random-secret-key
DEBUG=False

# Allowed hosts — add your machine's IP for LAN access
ALLOWED_HOSTS=localhost,192.168.x.x

# File uploads directory
MEDIA_ROOT=C:\projects\rsvr-sdd\media
```

**Notes**:
- Replace `your-password-here` with the PostgreSQL `postgres` password you set during installation
- Generate a `SECRET_KEY` by running:
  ```powershell
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- Replace `192.168.x.x` with your laptop's local IP address (run `ipconfig` to find it)
- The `MEDIA_ROOT` directory will be created later in this guide

### 3. Install Dependencies

Navigate to the backend directory and install Python dependencies:

```powershell
cd C:\projects\rsvr-sdd\backend
pip install -e .
pip install waitress
```

> `pip install -e .` installs the project and its dependencies from `pyproject.toml`.  
> `waitress` is the WSGI server used to serve the application on Windows.

Verify dependencies installed correctly:
```powershell
pip list
```

Ensure these packages appear:
- `Django` 5.0+
- `psycopg2-binary`
- `whitenoise`
- `waitress`

---

## Initialize the Database

### 1. Create the Database

Open **pgAdmin 4** (installed with PostgreSQL) or use the command line:

```powershell
psql -U postgres
```

At the `postgres=#` prompt, run:
```sql
CREATE DATABASE rsvr;
\q
```

### 2. Run Migrations

```powershell
cd C:\projects\rsvr-sdd\backend
python manage.py migrate
```

Expected output: A list of applied migrations with `OK` status.

### 3. Verify the Connection

```powershell
python manage.py check
```

If the output is `System check identified no issues (0 silenced).`, the database is connected and working.

---

## Configure File Uploads Storage

1. **Create the media directory**:
   ```powershell
   mkdir C:\projects\rsvr-sdd\media
   ```

2. **Verify write permissions**:
   ```powershell
   echo "test" > C:\projects\rsvr-sdd\media\test.txt
   Remove-Item C:\projects\rsvr-sdd\media\test.txt
   ```

   If no errors appear, the directory is ready for file uploads.

3. The `MEDIA_ROOT` in your `.env` file should point to this directory. It is already configured in the template above.

---

## Configure Windows Firewall

To make the web application accessible to other devices on your local network, create an inbound firewall rule:

```powershell
netsh advfirewall firewall add rule name="RSVR Web App" dir=in action=allow protocol=TCP localport=8000
```

This opens port **8000** for inbound TCP connections.

**To verify the rule**:
```powershell
netsh advfirewall firewall show rule name="RSVR Web App"
```

**To remove the rule later** (if needed):
```powershell
netsh advfirewall firewall delete rule name="RSVR Web App"
```

> **Security note**: Only open this port when you need LAN access. Close it when not in use.

---

## Run the Web Application

### Start the Server

```powershell
cd C:\projects\rsvr-sdd\backend
waitress-serve --host=0.0.0.0 --port=8000 config.wsgi:application
```

- `--host=0.0.0.0` makes the app available on all network interfaces
- `--port=8000` sets the port
- `config.wsgi:application` points to the Django WSGI application

Expected output:
```
INFO:waitress:Serving on http://0.0.0.0:8000
```

### Verify in Browser

1. **On the same machine**: Open [http://localhost:8000](http://localhost:8000) — the application should load
2. **From another device on the same network**: Open `http://<YOUR_IP>:8000` (replace `<YOUR_IP>` with the laptop's IP address)

### Stop the Server

Press `Ctrl + C` in the terminal where `waitress-serve` is running.

---

## Start the App After Restart

If the laptop is restarted or shut down, follow these steps to restore the web application.

All three options below use the same core PowerShell command that loads environment variables from `.env` and starts the application:

```powershell
Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object { $name, $value = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process') }; uv run .\manage.py runserver
```

> **Security**: The `.env` file contains database credentials and the Django `SECRET_KEY`. Restrict access with:
> ```powershell
> icacls .env /inheritance:r /grant "Administrators:R"
> ```
> Task Scheduler stores the command in plain text — any user with read access to the task can see the credentials. Consider using Windows Credential Manager for additional security.

### Option 1: Manual Start (Quick)

Open a PowerShell terminal and run:

```powershell
cd D:\Descargas\codigo\rsvr-sdd
Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object { $name, $value = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process') }; uv run .\manage.py runserver
```

Press **Ctrl + C** to stop the server.

### Option 2: Use a Launcher Script

Create a file named `start_app.ps1` in `D:\Descargas\codigo\rsvr-sdd`:

```powershell
Set-Location D:\Descargas\codigo\rsvr-sdd
Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object { $name, $value = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process') }; uv run .\manage.py runserver
```

PowerShell blocks `.ps1` scripts by default. To run the script, use one of these methods:

- **Permanent (recommended)**: Run this once to allow local scripts:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```
  Then right-click `start_app.ps1` and select **"Run with PowerShell"**.

- **One-time bypass**: Use the `-ExecutionPolicy` flag (no policy change):
  ```powershell
  powershell -ExecutionPolicy Bypass -File D:\Descargas\codigo\rsvr-sdd\start_app.ps1
  ```

Press **Ctrl + C** to stop the server.

### Option 3: Auto-Start Using Task Scheduler

For automatic startup when Windows boots:

1. Press **Win + R**, type `taskschd.msc`, and press Enter
2. Click **"Create Basic Task"** on the right panel
3. **Name**: `RSVR Web App`
4. **Trigger**: **"When the computer starts"** (or **"When I log on"** for user-specific)
5. **Action**: **"Start a program"**
   - **Program/script**: `powershell.exe`
   - **Arguments**:
     ```
     -Command "cd D:\Descargas\codigo\rsvr-sdd; Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object { $name, $value = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process') }; uv run .\manage.py runserver"
     ```
6. Click **Finish**

The application will now start automatically on every boot. To verify:

1. Restart the laptop
2. Open [http://localhost:8000](http://localhost:8000) in a browser
3. The application should load without manual intervention

> **Note**: The PostgreSQL service should already be set to **Automatic** startup (default when installed via the EDB installer). Verify with:
> ```powershell
> Get-Service postgresql*
> ```

---

## Troubleshooting

### Port 8000 Already in Use

```powershell
netstat -ano | findstr :8000
```

Find the PID column and terminate the process:
```powershell
taskkill /PID <PID> /F
```

### PostgreSQL Connection Refused

1. Check if PostgreSQL service is running:
   ```powershell
   Get-Service postgresql*
   ```
2. If stopped, start it:
   ```powershell
   Start-Service postgresql*
   ```
3. Verify the `.env` `DATABASE_URL` has the correct password

### Python Not Recognized

If `python` is not recognized as a command:
1. Open **System Properties** → **Advanced** → **Environment Variables**
2. Under **System variables**, find `Path`, click **Edit**
3. Add these entries (adjust for your Python version):
   - `C:\Users\<YourUser>\AppData\Local\Programs\Python\Python312\`
   - `C:\Users\<YourUser>\AppData\Local\Programs\Python\Python312\Scripts\`
4. Click **OK** and restart the terminal

### Migration Fails

```powershell
python manage.py migrate --run-syncdb
```

If this fails, check the `DATABASE_URL` in `.env` and ensure PostgreSQL is running.

### Firewall Rule Already Exists

If creating the firewall rule returns an error, the rule may already exist. Verify with:
```powershell
netsh advfirewall firewall show rule name="RSVR Web App"
```

### File Upload Fails

Ensure the `media` directory exists and the `MEDIA_ROOT` in `.env` points to the correct path:
```powershell
echo %MEDIA_ROOT%
```

---

## Links & References

### Software Downloads

| Software | Download Link |
|----------|---------------|
| PostgreSQL (EDB) | [https://www.enterprisedb.com/downloads/postgres-postgresql-downloads](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) |
| Python | [https://www.python.org/downloads/](https://www.python.org/downloads/) |
| Git for Windows | [https://git-scm.com/download/win](https://git-scm.com/download/win) |

### Documentation

| Topic | Link |
|-------|------|
| Django settings | [https://docs.djangoproject.com/en/5.0/ref/settings/](https://docs.djangoproject.com/en/5.0/ref/settings/) |
| Waitress documentation | [https://docs.pylonsproject.org/projects/waitress/en/stable/](https://docs.pylonsproject.org/projects/waitress/en/stable/) |
| PostgreSQL Windows install | [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/) |
| Windows Task Scheduler | [https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page](https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page) |
| Netsh firewall commands | [https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/) |
