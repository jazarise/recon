#!/usr/bin/env bash
# ReconX Production Installer (Linux/WSL)

set -e

echo "[*] ReconX V2.0.0 Installation Started"

# Ensure we are in the project root
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)

# Create virtual environment
echo "[*] Creating Python Virtual Environment..."
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
echo "[*] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create global executable
echo "[*] Registering 'reconx' command globally..."
mkdir -p "$HOME/.local/bin"
cat <<EOF > "$HOME/.local/bin/reconx"
#!/usr/bin/env bash
source "$PROJECT_ROOT/venv/bin/activate"
python "$PROJECT_ROOT/reconx.py" "\$@"
EOF
chmod +x "$HOME/.local/bin/reconx"

echo "[+] Installation successful!"
echo "    You can now run 'reconx' from any directory."
echo "    Ensure $HOME/.local/bin is in your PATH."
