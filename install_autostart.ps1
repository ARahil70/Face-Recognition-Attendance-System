$ErrorActionPreference = 'Stop'
$project = $PSScriptRoot
$python = Join-Path $project '.venv\Scripts\pythonw.exe'
$app = Join-Path $project 'src\attendance_app.py'

if (-not (Test-Path -LiteralPath $python)) { throw "Python environment not found at $python." }
if (-not (Test-Path -LiteralPath $app)) { throw "CampusFlow app not found at $app." }

$taskName = 'CampusFlow Attendance'
$actionOptions = @{
    Execute          = $python
    Argument         = "`"$app`""
    WorkingDirectory = $project
}
$action = New-ScheduledTaskAction @actionOptions
$trigger = New-ScheduledTaskTrigger -AtLogOn -User "$env:USERDOMAIN\$env:USERNAME"
$principalOptions = @{
    UserId    = "$env:USERDOMAIN\$env:USERNAME"
    LogonType = 'Interactive'
    RunLevel  = 'Limited'
}
$principal = New-ScheduledTaskPrincipal @principalOptions
$settingsOptions = @{
    StartWhenAvailable = $true
    RestartCount       = 3
    RestartInterval    = (New-TimeSpan -Minutes 1)
}
$settings = New-ScheduledTaskSettingsSet @settingsOptions
$registrationOptions = @{
    TaskName    = $taskName
    Action      = $action
    Trigger     = $trigger
    Principal   = $principal
    Settings    = $settings
    Description = 'Starts CampusFlow Attendance when this Windows user signs in.'
    Force       = $true
}
Register-ScheduledTask @registrationOptions | Out-Null
Write-Host "Installed '$taskName'. It starts at sign-in; keep this computer on and the chosen camera connected."
