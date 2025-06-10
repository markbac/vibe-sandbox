# This script sets up a Python virtual environment and installs dependencies

$venvPath = ".venv"

if (-Not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..."
    python -m venv $venvPath
} else {
    Write-Host "Virtual environment already exists."
}

Write-Host "Activating virtual environment and installing requirements..."
& $venvPath\Scripts\Activate.ps1
pip install --upgrade pip
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Write-Host "No requirements.txt found. Skipping dependency installation."
}
