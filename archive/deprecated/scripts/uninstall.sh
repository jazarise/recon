#!/usr/bin/env bash
# ReconX Production Uninstaller (Linux/WSL)

echo "[*] Uninstalling ReconX V2.0.0..."

cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

# Remove global executable
if [ -f "$HOME/.local/bin/reconx" ]; then
    echo "[*] Removing global executable..."
    rm "$HOME/.local/bin/reconx"
fi

# Remove virtual environment
if [ -d "venv" ]; then
    echo "[*] Removing virtual environment..."
    rm -rf venv
fi

echo "[+] Uninstallation successful."
