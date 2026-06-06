<#
.SYNOPSIS
ReconX Production Installer (Windows PowerShell)
#>

$ErrorActionPreference = "Stop"

Write-Host "[*] ReconX V2.0.0 Installation Started" -ForegroundColor Cyan

# Ensure we are in the project root
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

# Create virtual environment
Write-Host "[*] Creating Python Virtual Environment..."
python -m venv venv

# Install dependencies
Write-Host "[*] Installing Python dependencies..."
& "$ProjectRoot\venv\Scripts\python.exe" -m pip install --upgrade pip
& "$ProjectRoot\venv\Scripts\python.exe" -m pip install -r requirements.txt

# Create global executable
Write-Host "[*] Registering 'reconx' command globally..."
$InstallersDir = "$ProjectRoot\installers"
if (-Not (Test-Path $InstallersDir)) {
    New-Item -ItemType Directory -Path $InstallersDir | Out-Null
}

$BatPath = "$InstallersDir\reconx.bat"
"@echo off`n`"$ProjectRoot\venv\Scripts\python.exe`" `"$ProjectRoot\reconx.py`" %*" | Out-File -FilePath $BatPath -Encoding utf8

Write-Host "[+] Installation successful!" -ForegroundColor Green
Write-Host "    Add '$InstallersDir' to your System PATH to use 'reconx' globally." -ForegroundColor Yellow
