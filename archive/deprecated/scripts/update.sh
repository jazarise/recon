#!/usr/bin/env bash
# ReconX Production Updater (Linux/WSL)

set -e

echo "[*] Updating ReconX V2.0.0..."

cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

# Pull latest changes if using git
if [ -d ".git" ]; then
    echo "[*] Pulling latest repository changes..."
    git pull
else
    echo "[-] Not a git repository, skipping pull."
fi

# Update dependencies
echo "[*] Updating Python dependencies..."
if [ -d "venv" ]; then
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "[-] Virtual environment not found. Please run scripts/install.sh first."
    exit 1
fi

echo "[+] Update successful!"
