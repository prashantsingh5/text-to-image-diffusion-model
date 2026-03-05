param(
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating .venv ..."
    py -m venv .venv
}

if (-not $SkipInstall) {
    Write-Host "Installing dependencies in .venv ..."
    .\.venv\Scripts\python -m pip install --upgrade pip
    .\.venv\Scripts\python -m pip install -r requirements.txt
}

Write-Host "Running tests ..."
.\.venv\Scripts\python -m pytest -q

Write-Host "Self-test completed successfully."
