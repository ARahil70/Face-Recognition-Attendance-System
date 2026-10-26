$ErrorActionPreference = 'Stop'
$unregisterOptions = @{
    TaskName    = 'CampusFlow Attendance'
    Confirm     = $false
    ErrorAction = 'SilentlyContinue'
}
Unregister-ScheduledTask @unregisterOptions

Write-Host 'CampusFlow auto-start has been removed.'
