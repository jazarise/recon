#!/usr/bin/env bash
# ReconX Installation Script — Kali Linux / Debian-based systems
set -e

RED='\033[0;31m'; CYAN='\033[0;36m'; GREEN='\033[0;32m'; NC='\033[0m'

echo -e "${RED}"
echo "  ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗"
echo "  ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝"
echo "  ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ "
echo "  ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ "
echo "  ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗"
echo "  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝"
echo -e "${NC}"
echo -e "${CYAN}ReconX Installer — Unified Reconnaissance Platform${NC}"
echo ""

# ── Python check ─────────────────────────────────────────────────────────────
PYTHON=$(which python3 2>/dev/null || which python 2>/dev/null)
if [ -z "$PYTHON" ]; then
  echo -e "${RED}[ERROR] Python 3.10+ is required. Install it first.${NC}"
  exit 1
fi
VER=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}[OK]${NC} Python $VER"

# ── Pip dependencies ──────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}[*] Installing Python dependencies…${NC}"
$PYTHON -m pip install -r requirements.txt --quiet --break-system-packages 2>/dev/null || \
  $PYTHON -m pip install -r requirements.txt --quiet
echo -e "${GREEN}[OK]${NC} Python packages installed"

# ── Create .env template ──────────────────────────────────────────────────────
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo -e "${GREEN}[OK]${NC} .env created from template (edit to add API keys)"
fi

# ── Create wrapper script ─────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
WRAPPER="$HOME/.local/bin/reconx"
mkdir -p "$HOME/.local/bin"

cat > "$WRAPPER" << WRAPPER_EOF
#!/usr/bin/env bash
cd "$SCRIPT_DIR"
exec python3 reconx.py "\$@"
WRAPPER_EOF

chmod +x "$WRAPPER"
echo -e "${GREEN}[OK]${NC} reconx command installed → $WRAPPER"

# ── Optional tools check ──────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}[*] Checking optional recon tools…${NC}"
TOOLS=(subfinder amass nmap naabu httpx katana hakrawler dnsx nuclei ffuf gobuster)
MISSING=()
for tool in "${TOOLS[@]}"; do
  if command -v "$tool" &>/dev/null; then
    echo -e "  ${GREEN}✓${NC} $tool"
  else
    echo -e "  ${RED}✗${NC} $tool (optional — install for full capability)"
    MISSING+=("$tool")
  fi
done

# ── PATH reminder ─────────────────────────────────────────────────────────────
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo ""
  echo -e "${CYAN}[!]${NC} Add to your shell profile to use 'reconx' globally:"
  echo -e "    echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc"
  echo -e "    source ~/.bashrc"
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ReconX installed successfully!      ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""
echo -e "  Run: ${CYAN}python3 reconx.py${NC}"
echo -e "  Or:  ${CYAN}reconx${NC}  (after adding ~/.local/bin to PATH)"
echo ""
