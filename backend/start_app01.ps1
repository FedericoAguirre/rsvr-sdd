cd D:\Descargas\codigo\rsvr-sdd
Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object { $name, $value = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process') }

# Configuration
$retryInterval = 2
$maxRetryDuration = 30

Write-Host "Checking PostgreSQL readiness..." -ForegroundColor Cyan

# --- Parse connection parameters ---
$pgHost = "localhost"
$pgPort = 5432
$pgDatabase = ""
$pgUser = ""
$pgPassword = ""
$configSource = ""

$DATABASE_URL = [System.Environment]::GetEnvironmentVariable("DATABASE_URL", "Process")
if ($DATABASE_URL) {
    $match = [regex]::Match($DATABASE_URL, "^postgres://(.+):(.+)@(.+):(\d+)/(.+)$")
    if ($match.Success) {
        $pgUser     = $match.Groups[1].Value
        $pgPassword = $match.Groups[2].Value
        $pgHost     = $match.Groups[3].Value
        $pgPort     = [int]$match.Groups[4].Value
        $pgDatabase = $match.Groups[5].Value
        $configSource = "DATABASE_URL"
    }
}

if (-not $configSource) {
    $pgHost = [System.Environment]::GetEnvironmentVariable("POSTGRES_HOST", "Process")
    if (-not $pgHost) { $pgHost = "localhost" }

    $portStr = [System.Environment]::GetEnvironmentVariable("POSTGRES_PORT", "Process")
    if ($portStr) { $pgPort = [int]$portStr }

    $pgDatabase = [System.Environment]::GetEnvironmentVariable("POSTGRES_DB", "Process")
    $pgUser     = [System.Environment]::GetEnvironmentVariable("POSTGRES_USER", "Process")
    $pgPassword = [System.Environment]::GetEnvironmentVariable("POSTGRES_PASSWORD", "Process")

    if ($pgDatabase -and $pgUser -and ($pgPassword -ne $null)) {
        $configSource = "POSTGRES_*"
    }
}

if (-not $configSource) {
    Write-Host "  ✖ Database configuration incomplete. Check DATABASE_URL or POSTGRES_* variables in .env" -ForegroundColor Red
    exit 1
}

# --- Helper functions ---
function Test-PostgresTcp {
    param([string]$TargetHost, [int]$TargetPort)
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $tcp.Connect($TargetHost, $TargetPort)
        $tcp.Close()
        return $true
    } catch {
        return $false
    }
}

function Test-PostgresReady {
    param([string]$TargetHost, [int]$TargetPort, [string]$Database, [string]$User, [string]$Password)

    $tcpOk = Test-PostgresTcp -TargetHost $TargetHost -TargetPort $TargetPort
    if (-not $tcpOk) {
        return @{ Ready = $false; Reason = "tcp-unreachable" }
    }

    $pgIsReady = Get-Command pg_isready -ErrorAction SilentlyContinue
    if ($pgIsReady) {
        $env:PGPASSWORD = $Password
        $output = & pg_isready -h $TargetHost -p $TargetPort -d $Database -U $User 2>&1
        Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
        $exitCode = $LASTEXITCODE
        if ($exitCode -eq 0) {
            return @{ Ready = $true; Reason = "ok" }
        } elseif ($output -match "authentication|password") {
            return @{ Ready = $false; Reason = "auth-failure" }
        } elseif ($output -match "does not exist") {
            return @{ Ready = $false; Reason = "db-not-found" }
        } else {
            return @{ Ready = $false; Reason = "not-accepting" }
        }
    }

    return @{ Ready = $true; Reason = "tcp-only" }
}

# --- Retry loop ---
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
$ready = $false
$finalReason = ""

Write-Host "  Connecting to PostgreSQL at ${pgHost}:${pgPort}..." -ForegroundColor Gray

while ($stopwatch.Elapsed.TotalSeconds -lt $maxRetryDuration) {
    $result = Test-PostgresReady -TargetHost $pgHost -TargetPort $pgPort -Database $pgDatabase -User $pgUser -Password $pgPassword

    if ($result.Ready) {
        $ready = $true
        break
    }

    $finalReason = $result.Reason
    Write-Host "." -NoNewline -ForegroundColor DarkYellow
    Start-Sleep -Seconds $retryInterval
}

$stopwatch.Stop()

# --- Result ---
if ($ready) {
    if ($result.Reason -eq "tcp-only") {
        Write-Host ""
        Write-Host "  ✔ Database ready (TCP check only — pg_isready not found)" -ForegroundColor Yellow
    } else {
        $elapsed = [math]::Floor($stopwatch.Elapsed.TotalSeconds)
        if ($elapsed -eq 0) {
            Write-Host ""
            Write-Host "  ✔ Database ready" -ForegroundColor Green
        } else {
            Write-Host ""
            Write-Host "  ✔ Database ready after ${elapsed} seconds" -ForegroundColor Green
        }
    }

    Write-Host ""
    Write-Host "Starting Django development server..." -ForegroundColor Cyan
    cd backend
    uv run .\manage.py runserver
    exit 0
} else {
    Write-Host ""
    switch ($finalReason) {
        "tcp-unreachable" {
            Write-Host "  ✖ PostgreSQL is not reachable at ${pgHost}:${pgPort}. Ensure the PostgreSQL service is running." -ForegroundColor Red
            exit 2
        }
        "auth-failure" {
            Write-Host "  ✖ PostgreSQL at ${pgHost}:${pgPort} is reachable but authentication failed. Check POSTGRES_USER and POSTGRES_PASSWORD." -ForegroundColor Red
            exit 4
        }
        "db-not-found" {
            Write-Host "  ✖ Database '${pgDatabase}' does not exist on ${pgHost}:${pgPort}. Create it or check POSTGRES_DB." -ForegroundColor Red
            exit 3
        }
        default {
            Write-Host "  ✖ PostgreSQL at ${pgHost}:${pgPort} is not accepting connections. Ensure the PostgreSQL service is running." -ForegroundColor Red
            exit 3
        }
    }
}
