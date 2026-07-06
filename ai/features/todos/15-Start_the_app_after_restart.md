# Change the start the app after restart docs section

As a developer, I want to update the "Start the App After Restart" in the @docs/windows11_deployment.md file.

I want to change the "### Option 3: Auto-Start Using Task Scheduler" section to make use of Powershell and the task scheduler to:

1. Execute the next .env loader script:

```powershell
Get-Content .env | Where-Object { $_ -match '=' -and $_ -notmatch '^#' } | ForEach-Object { $name, $value = $_ -split '=', 2; [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), 'Process') }
```

2. Autoload the Django server using uv, with the command:

```powershell
uv run .\manage.py runserver
```

Consider that the project is located at the ```D:\Descargas\codigo\rsvr-sdd``` folder.

Update the powershell commands as needed to resolve the relative routes.

Add or update a testing method for this new approach.