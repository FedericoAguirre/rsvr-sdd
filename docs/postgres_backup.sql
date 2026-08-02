# PostgreSQL 19 Automated Full Backup on Windows 11 Home

This manual describes how to configure an automated **full backup** of PostgreSQL 19 running on **Windows 11 Home**.

The backup is automated using:

* PostgreSQL 19
* Windows 11 Home
* PowerShell
* Windows Task Scheduler
* `pg_dumpall` for the full PostgreSQL cluster backup
* Weekly execution
* Monday at 12:00 PM

The procedure creates a scheduled task that executes a PowerShell script automatically.

---

## 1. Backup Architecture

The automation consists of the following components:

```text
Windows Task Scheduler
        |
        | Every Monday at 12:00
        v
PowerShell Script
        |
        | Executes
        v
PostgreSQL 19 pg_dumpall
        |
        | Creates
        v
Compressed Backup File
        |
        v
Backup Directory
```

The scheduled task is responsible only for triggering the PowerShell script.

The PowerShell script is responsible for:

1. Creating the backup directory if it does not exist.
2. Generating a timestamp.
3. Executing `pg_dumpall`.
4. Compressing the backup.
5. Logging the operation.
6. Reporting errors.

---

# 2. Prerequisites

Before configuring the automation, verify that PostgreSQL 19 is installed.

The PostgreSQL installation is typically located at:

```text
C:\Program Files\PostgreSQL\19
```

The PostgreSQL executable directory should be:

```text
C:\Program Files\PostgreSQL\19\bin
```

Verify that the following executable exists:

```text
C:\Program Files\PostgreSQL\19\bin\pg_dumpall.exe
```

Open PowerShell and run:

```powershell
Test-Path "C:\Program Files\PostgreSQL\19\bin\pg_dumpall.exe"
```

Expected result:

```text
True
```

If the result is `False`, locate the actual PostgreSQL installation directory before continuing.

---

# 3. Create the Backup Directory

Create a dedicated directory for backups.

For example:

```text
C:\PostgreSQLBackups
```

Run PowerShell as Administrator and execute:

```powershell
New-Item -ItemType Directory -Path "C:\PostgreSQLBackups" -Force
```

Create a directory for logs:

```powershell
New-Item -ItemType Directory -Path "C:\PostgreSQLBackups\logs" -Force
```

The resulting structure will be:

```text
C:\PostgreSQLBackups
├── logs
├── backups
└── scripts
```

Create the additional directories:

```powershell
New-Item -ItemType Directory -Path "C:\PostgreSQLBackups\backups" -Force
New-Item -ItemType Directory -Path "C:\PostgreSQLBackups\scripts" -Force
```

---

# 4. Configure PostgreSQL Authentication

The PowerShell script needs credentials to connect to PostgreSQL.

The recommended approach for an automated backup is to use a PostgreSQL password file.

On Windows, PostgreSQL uses:

```text
%APPDATA%\postgresql\pgpass.conf
```

For example:

```text
C:\Users\YOUR_USERNAME\AppData\Roaming\postgresql\pgpass.conf
```

Create the directory:

```powershell
New-Item -ItemType Directory `
    -Path "$env:APPDATA\postgresql" `
    -Force
```

Create the file:

```powershell
New-Item -ItemType File `
    -Path "$env:APPDATA\postgresql\pgpass.conf" `
    -Force
```

Edit the file:

```text
localhost:5432:*:postgres:YOUR_POSTGRES_PASSWORD
```

The format is:

```text
hostname:port:database:username:password
```

For example:

```text
localhost:5432:*:postgres:MySecurePassword
```

The `*` means that the password applies to all databases.

Protect the file so that only your Windows user can access it.

Do not commit `pgpass.conf` to Git or store it in a source-code repository.

---

# 5. Test PostgreSQL Connectivity

Before automating the backup, test the connection manually.

Run:

```powershell
& "C:\Program Files\PostgreSQL\19\bin\pg_dumpall.exe" `
    -h localhost `
    -p 5432 `
    -U postgres `
    --globals-only
```

If the command successfully returns PostgreSQL roles and other global objects, authentication is working.

---

# 6. Create the PowerShell Backup Script

Create the following file:

```text
C:\PostgreSQLBackups\scripts\PostgreSQL-FullBackup.ps1
```

Add the following content:

```powershell
# PostgreSQL 19 Full Backup Script
# Windows 11
# Executed by Windows Task Scheduler

$ErrorActionPreference = "Stop"

# PostgreSQL configuration
$PgBin = "C:\Program Files\PostgreSQL\19\bin"
$PgDumpAll = Join-Path $PgBin "pg_dumpall.exe"

$PgHost = "localhost"
$PgPort = "5432"
$PgUser = "postgres"

# Backup configuration
$BackupDirectory = "C:\PostgreSQLBackups\backups"
$LogDirectory = "C:\PostgreSQLBackups\logs"

# Create directories if they do not exist
New-Item -ItemType Directory `
    -Path $BackupDirectory `
    -Force | Out-Null

New-Item -ItemType Directory `
    -Path $LogDirectory `
    -Force | Out-Null

# Generate timestamp
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

# Backup file
$BackupFile = Join-Path `
    $BackupDirectory `
    "postgresql_full_backup_$Timestamp.sql"

# Log file
$LogFile = Join-Path `
    $LogDirectory `
    "backup_$Timestamp.log"

try {

    Add-Content $LogFile "========================================"
    Add-Content $LogFile "PostgreSQL Full Backup"
    Add-Content $LogFile "Started: $(Get-Date)"
    Add-Content $LogFile "========================================"

    # Verify pg_dumpall exists
    if (-not (Test-Path $PgDumpAll)) {
        throw "pg_dumpall.exe was not found at: $PgDumpAll"
    }

    Add-Content $LogFile "Starting PostgreSQL backup..."
    Add-Content $LogFile "Backup file: $BackupFile"

    # Execute pg_dumpall
    & $PgDumpAll `
        -h $PgHost `
        -p $PgPort `
        -U $PgUser `
        --file="$BackupFile" `
        2>> $LogFile

    if ($LASTEXITCODE -ne 0) {
        throw "pg_dumpall failed with exit code $LASTEXITCODE"
    }

    # Verify backup file exists
    if (-not (Test-Path $BackupFile)) {
        throw "Backup file was not created."
    }

    $BackupSize = (Get-Item $BackupFile).Length

    if ($BackupSize -eq 0) {
        throw "Backup file is empty."
    }

    Add-Content $LogFile "Backup completed successfully."
    Add-Content $LogFile "Backup size: $BackupSize bytes"
    Add-Content $LogFile "Finished: $(Get-Date)"

}
catch {

    Add-Content $LogFile "BACKUP FAILED"
    Add-Content $LogFile "Error: $($_.Exception.Message)"
    Add-Content $LogFile "Finished: $(Get-Date)"

    exit 1
}
```

---

# 7. Test the PowerShell Script

Before creating the scheduled task, run the script manually.

Open PowerShell and execute:

```powershell
powershell.exe `
    -ExecutionPolicy Bypass `
    -File "C:\PostgreSQLBackups\scripts\PostgreSQL-FullBackup.ps1"
```

Check the backup directory:

```powershell
Get-ChildItem "C:\PostgreSQLBackups\backups"
```

You should see a file similar to:

```text
postgresql_full_backup_2026-07-30_12-00-00.sql
```

Check the logs:

```powershell
Get-ChildItem "C:\PostgreSQLBackups\logs"
```

Open the latest log:

```powershell
Get-Content `
    (Get-ChildItem "C:\PostgreSQLBackups\logs" |
     Sort-Object LastWriteTime |
     Select-Object -Last 1).FullName
```

The log should indicate:

```text
Backup completed successfully.
```

---

# 8. Create the Windows Scheduled Task

Open **Task Scheduler**.

Press:

```text
Windows + R
```

Enter:

```text
taskschd.msc
```

Press Enter.

---

## 8.1 Create a New Task

In Task Scheduler:

1. Select **Task Scheduler Library**.
2. Click **Create Task**.

Do not use **Create Basic Task**, because the full task configuration provides better control.

---

# 9. Configure the General Tab

Configure:

**Name:**

```text
PostgreSQL 19 Weekly Full Backup
```

**Description:**

```text
Runs a full PostgreSQL 19 backup every Monday at 12:00 PM.
```

Select:

```text
Run whether user is logged on or not
```

Select:

```text
Run with highest privileges
```

For **Configure for**, select:

```text
Windows 11
```

The task should run under the Windows user account that has access to the PostgreSQL `pgpass.conf` file.

---

# 10. Configure the Trigger

Open the **Triggers** tab.

Click:

```text
New...
```

Configure:

**Begin the task:**

```text
On a schedule
```

Select:

```text
Weekly
```

Configure:

```text
Start: 12:00:00 PM
Recur every: 1 week
Monday
```

Ensure:

```text
Enabled
```

is selected.

Click **OK**.

The trigger should now execute every:

```text
Monday at 12:00 PM
```

---

# 11. Configure the Action

Open the **Actions** tab.

Click:

```text
New...
```

Configure:

**Action:**

```text
Start a program
```

**Program/script:**

```text
powershell.exe
```

**Add arguments:**

```text
-NoProfile -ExecutionPolicy Bypass -File "C:\PostgreSQLBackups\scripts\PostgreSQL-FullBackup.ps1"
```

**Start in:**

```text
C:\PostgreSQLBackups\scripts
```

Click **OK**.

---

# 12. Configure Conditions

Open the **Conditions** tab.

For a desktop or laptop computer, consider enabling:

```text
Start the task only if the computer is on AC power
```

If backups must run even when the laptop is operating on battery, disable this option.

You may also enable:

```text
Wake the computer to run this task
```

if you want Windows to wake the computer at 12:00 PM.

Note that Windows must be configured to permit the relevant wake timers.

---

# 13. Configure Settings

Open the **Settings** tab.

Recommended settings:

```text
Allow task to be run on demand
```

Enable:

```text
Run task as soon as possible after a scheduled start is missed
```

Enable:

```text
If the task fails, restart every:
```

For example:

```text
5 minutes
```

Set:

```text
Attempt to restart up to:
3 times
```

You can also enable:

```text
Stop the task if it runs longer than:
2 hours
```

The appropriate timeout depends on the size of your PostgreSQL databases.

Click **OK**.

Windows may ask for the password of the Windows user account running the task.

Enter the password.

---

# 14. Run the Scheduled Task Manually

To test the complete automation:

1. Open **Task Scheduler**.
2. Select **Task Scheduler Library**.
3. Find:

```text
PostgreSQL 19 Weekly Full Backup
```

4. Right-click the task.
5. Select:

```text
Run
```

Wait for the task to finish.

Check the backup directory:

```powershell
Get-ChildItem "C:\PostgreSQLBackups\backups"
```

Check the logs:

```powershell
Get-ChildItem "C:\PostgreSQLBackups\logs"
```

---

# 15. Verify the Backup

A successful backup file should have a non-zero size.

Run:

```powershell
Get-ChildItem "C:\PostgreSQLBackups\backups" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
```

For additional verification, inspect the beginning of the SQL file:

```powershell
Get-Content `
    "C:\PostgreSQLBackups\backups\postgresql_full_backup_YYYY-MM-DD_HH-mm-ss.sql" `
    -TotalCount 20
```

The file should contain PostgreSQL SQL statements and comments generated by `pg_dumpall`.

---

# 16. Restore a Full Backup

A `pg_dumpall` backup is a SQL script.

To restore it, use `psql`.

For example:

```powershell
& "C:\Program Files\PostgreSQL\19\bin\psql.exe" `
    -h localhost `
    -p 5432 `
    -U postgres `
    -f "C:\PostgreSQLBackups\backups\postgresql_full_backup_YYYY-MM-DD_HH-mm-ss.sql"
```

Restoring a full cluster backup should generally be performed on a PostgreSQL instance prepared for the restore operation.

For disaster recovery, test the restore procedure on a separate PostgreSQL installation or machine before relying on the backup.

---

# 17. Recommended Backup Retention

The current script keeps every backup indefinitely.

For long-running automation, implement a retention policy.

For example:

```text
Keep the last 8 weekly backups
```

Add the following PowerShell code to the script after a successful backup:

```powershell
$RetentionCount = 8

$OldBackups = Get-ChildItem `
    -Path $BackupDirectory `
    -Filter "postgresql_full_backup_*.sql" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -Skip $RetentionCount

foreach ($OldBackup in $OldBackups) {

    Remove-Item `
        $OldBackup.FullName `
        -Force

    Add-Content `
        $LogFile `
        "Deleted old backup: $($OldBackup.FullName)"
}
```

This keeps the eight most recent backups.

---

# 18. Recommended Backup Strategy

A backup stored on the same computer as the PostgreSQL server is not sufficient for disaster recovery.

If the computer's disk fails, both the PostgreSQL database and backups may be lost.

A stronger strategy is:

```text
PostgreSQL
    |
    v
Local Weekly Backup
    |
    v
External Backup Location
    |
    +-- External HDD
    |
    +-- NAS
    |
    +-- Cloud Storage
```

At minimum, maintain:

* One local backup.
* One backup on a separate physical device.
* One off-site backup.

The backup process should follow the **3-2-1 backup strategy** where practical:

```text
3 copies of data
2 different storage media
1 copy stored off-site
```

---

# 19. Important Security Considerations

Do not place PostgreSQL passwords directly in the PowerShell script.

Avoid:

```powershell
$Password = "MyPassword"
```

Prefer PostgreSQL's password file:

```text
pgpass.conf
```

Restrict access to the following locations:

```text
C:\Users\YOUR_USERNAME\AppData\Roaming\postgresql\pgpass.conf
```

and:

```text
C:\PostgreSQLBackups
```

The backup SQL file may contain sensitive data, including:

* User information
* Password hashes
* Business data
* Personally identifiable information
* Database structure

Protect backup files with appropriate Windows permissions and, when stored externally, encryption.

---

# 20. Final Configuration

The completed automation should have the following structure:

```text
C:\PostgreSQLBackups
│
├── backups
│   ├── postgresql_full_backup_2026-07-06_12-00-00.sql
│   ├── postgresql_full_backup_2026-07-13_12-00-00.sql
│   ├── postgresql_full_backup_2026-07-20_12-00-00.sql
│   └── postgresql_full_backup_2026-07-27_12-00-00.sql
│
├── logs
│   ├── backup_2026-07-06_12-00-00.log
│   ├── backup_2026-07-13_12-00-00.log
│   ├── backup_2026-07-20_12-00-00.log
│   └── backup_2026-07-27_12-00-00.log
│
└── scripts
    └── PostgreSQL-FullBackup.ps1
```

The Windows Task Scheduler configuration should be:

| Setting          | Value                            |
| ---------------- | -------------------------------- |
| Task Name        | PostgreSQL 19 Weekly Full Backup |
| Operating System | Windows 11 Home                  |
| Database         | PostgreSQL 19                    |
| Backup Utility   | `pg_dumpall.exe`                 |
| Script           | `PostgreSQL-FullBackup.ps1`      |
| Frequency        | Weekly                           |
| Day              | Monday                           |
| Time             | 12:00 PM                         |
| Backup Format    | SQL                              |
| Backup Location  | `C:\PostgreSQLBackups\backups`   |
| Log Location     | `C:\PostgreSQLBackups\logs`      |
| Authentication   | PostgreSQL `pgpass.conf`         |
| Retention        | 8 weekly backups (recommended)   |

---

# 21. Final Validation Checklist

Before considering the backup automation complete, verify:

* [ ] PostgreSQL 19 is installed.
* [ ] `pg_dumpall.exe` exists.
* [ ] `pgpass.conf` is configured.
* [ ] PostgreSQL authentication works without interactive password input.
* [ ] The PowerShell script runs successfully manually.
* [ ] A non-empty `.sql` backup is created.
* [ ] A backup log is generated.
* [ ] The Windows Scheduled Task exists.
* [ ] The trigger is configured for Monday at 12:00 PM.
* [ ] The task can be run manually.
* [ ] The scheduled task completes successfully.
* [ ] The backup can be restored in a test environment.
* [ ] Backup retention is configured.
* [ ] Backups are copied to an additional storage location.

---

## Important Note

The filename of this manual is:

```text
postgres_backup.md
```

The actual PostgreSQL backups generated by the PowerShell automation are:

```text
postgresql_full_backup_YYYY-MM-DD_HH-mm-ss.sql
```

The `.md` extension should be used for this documentation manual, while `.sql` is appropriate for the SQL backup generated by `pg_dumpall`.

