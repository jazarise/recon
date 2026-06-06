#!/usr/bin/env bash
# ReconX Optional Tools Installer

set -e

echo "[*] Installing optional Go-based security tools..."

if ! command -v go &> /dev/null; then
    echo "[-] Go is not installed. Please install Go (golang) first."
    echo "    Visit: https://go.dev/doc/install"
    exit 1
fi

export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin

TOOLS=(
    "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"
    "github.com/projectdiscovery/katana/cmd/katana@latest"
    "github.com/hakluke/hakrawler@latest"
    "github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
    "github.com/lc/gau/v2/cmd/gau@latest"
    "github.com/tomnomnom/waybackurls@latest"
    "github.com/tomnomnom/assetfinder@latest"
    "github.com/sensepost/gowitness@latest"
)

for tool in "${TOOLS[@]}"; do
    echo "  -> Installing $tool..."
    go install -v "$tool"
done

# Findomain (Rust, pre-compiled binary is easier)
if ! command -v findomain &> /dev/null; then
    echo "  -> Installing findomain..."
    wget -q https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux-i386.zip -O findomain.zip
    unzip -q -o findomain.zip
    chmod +x findomain
    mv findomain "$GOPATH/bin/"
    rm findomain.zip
fi

echo "[+] All tools installed to $GOPATH/bin"
echo "    Ensure $GOPATH/bin is in your PATH."
