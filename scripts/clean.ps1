$ErrorActionPreference = "SilentlyContinue"
Set-Location (Join-Path $PSScriptRoot "..")

$targets = @(
    ".pytest_cache",
    "tests\__pycache__",
    "sd\__pycache__",
    "sd\flagged",
    ".venv-1"
)

foreach ($target in $targets) {
    if (Test-Path $target) {
        Remove-Item -Recurse -Force $target
        Write-Host "Removed $target"
    }
}

Write-Host "Cleanup finished."
