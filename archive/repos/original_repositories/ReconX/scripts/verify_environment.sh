#!/usr/bin/env bash
# ReconX Environment Verification Script
# This script verifies that all necessary dependencies are installed and available in the PATH.

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "  ReconX Environment Verification"
echo "========================================"
echo ""

check_command() {
    local cmd=$1
    local name=$2
    local required=$3

    if command -v $cmd &> /dev/null; then
        local version=""
        if [ "$cmd" = "python3" ]; then
            version=$($cmd --version 2>&1)
        elif [ "$cmd" = "pip" ] || [ "$cmd" = "pip3" ]; then
            version=$($cmd --version 2>&1 | awk '{print $2}')
        elif [ "$cmd" = "node" ] || [ "$cmd" = "npm" ]; then
            version=$($cmd --version 2>&1)
        else
            version="Found"
        fi
        echo -e "${GREEN}[PASS]${NC} $name ($version)"
    else
        if [ "$required" = "true" ]; then
            echo -e "${RED}[FAIL]${NC} $name Not Installed"
        else
            echo -e "${YELLOW}[WARNING]${NC} $name Missing (Optional but recommended)"
        fi
    fi
}

# Core Requirements
check_command "python3" "Python" "true"
check_command "pip" "pip" "true"

# Verify venv module
if python3 -c "import venv" &> /dev/null; then
    echo -e "${GREEN}[PASS]${NC} Python venv module"
else
    echo -e "${RED}[FAIL]${NC} Python venv module Not Installed"
fi

# Frontend Requirements
check_command "node" "Node.js" "true"
check_command "npm" "npm" "true"

# Reconnaissance Tools
check_command "nmap" "Nmap" "true"
check_command "git" "Git" "true"
check_command "curl" "Curl" "true"
check_command "whois" "Whois" "true"
check_command "dig" "DNS Utils (dig)" "true"
check_command "amass" "Amass" "false"
check_command "subfinder" "Subfinder" "false"
check_command "nuclei" "Nuclei" "false"

echo ""
echo "========================================"
echo "  Verification Complete"
echo "========================================"
