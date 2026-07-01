# Research: Windows 11 Home Deployment

## Decision 1: WSGI Server for Windows

**Decision**: Waitress  
**Rationale**: Waitress is a pure-Python WSGI server that runs natively on Windows without requiring C extensions or POSIX-specific features. Unlike Gunicorn (POSIX-only) or uWSGI (complex C compilation on Windows), Waitress installs via pip and works out of the box. It supports HTTPS, multi-threading, and binding to specific IPs/hosts.  
**Alternatives considered**: Gunicorn (POSIX-only, incompatible), uWSGI (requires compilation tools, over-engineered for single-laptop deployment), Django's `runserver` (development only, not production-safe).

## Decision 2: PostgreSQL Installation on Windows 11 Home

**Decision**: Official EDB PostgreSQL installer (Windows GUI).  
**Rationale**: The EDB installer provides a one-click installation including pgAdmin, automatic Windows PATH configuration, and optional installation as a Windows service. It's the officially recommended method and handles port configuration, data directory setup, and password management.  
**Alternatives considered**: Chocolatey package (`choco install postgresql`), manual ZIP extraction — both less reliable for non-technical users.

## Decision 3: Post-Reboot Startup Mechanism

**Decision**: Windows Task Scheduler (run on startup/logon) + batch/powershell launcher script.  
**Rationale**: Windows 11 Home does not include IIS Manager or native service management for arbitrary executables. Task Scheduler provides a reliable "At startup" trigger that runs a script to start PostgreSQL (if not already a service) and launch the web app via Waitress. A `.bat` or `.ps1` launcher script in the project root simplifies manual restarts too.  
**Alternatives considered**: NSSM (Non-Sucking Service Manager) — would work but requires download of third-party tool; Windows Startup folder — less reliable, runs in user session only.

## Decision 4: Port Publishing / Firewall

**Decision**: Windows Defender Firewall rule via `netsh advfirewall` command.  
**Rationale**: Windows Defender Firewall is built-in and blocks inbound connections by default. Adding a rule for the web app port (e.g., 8000) via `netsh` allows LAN access. No third-party tools needed.  
**Alternatives considered**: Disabling firewall entirely (unsafe), port forwarding via router (over-engineered for local dev).

## Decision 5: File Uploads Local Storage

**Decision**: Dedicated directory within the project root (e.g., `media/`), with instructions to create it and verify write permissions.  
**Rationale**: Simple, predictable, no extra configuration. The .env file references the path. Windows does not have POSIX-style permissions issues as long as the user owns the directory.  
**Alternatives considered**: Windows-specific folder (e.g., `%APPDATA%`) — less discoverable.

## Decision 6: Required Python Version

**Decision**: Python 3.12+ (latest stable as of 2026).  
**Rationale**: The project uses modern Python features; 3.12 provides performance improvements and is the latest stable line.  
**Alternatives considered**: Python 3.11 — still maintained, but 3.12 is preferred for longevity.

## Decision 7: .env File Configuration

**Decision**: Template .env file with all required variables, documented inline comments.  
**Rationale**: Users need clear guidance on each variable. Template approach reduces configuration errors.
