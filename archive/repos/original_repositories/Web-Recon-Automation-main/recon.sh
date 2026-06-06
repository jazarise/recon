#!/bin/bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default values
DOMAIN=""
OUTPUT_DIR=""
SILENT=false
VERBOSE=false
LOG_FILE=""
SUBJACK_FINGERPRINTS=""

# Function to print banner
print_banner() {
    echo -e "${BLUE}"
    echo "    ____  ____  ___  ____  ____ "
    echo "   / __ \/ __ \/ _ \/ __ \/ __ \\"
    echo "  / /_/ / /_/ /  __/ /_/ / / / /"
    echo " / _, _/ .___/\___/\____/_/ /_/ "
    echo "/_/ |_/_/                       "
    echo "                                "
    echo -e "${NC}"
    echo -e "${YELLOW}Automated Web Reconnaissance Script${NC}"
    echo "-----------------------------------"
}

# Function to display usage
usage() {
    echo -e "Usage: $0 -d <domain> [-o <output_dir>] [-s] [-v] [-f <fingerprints_path>]"
    echo ""
    echo "Options:"
    echo "  -d    Target domain (required)"
    echo "  -o    Output directory (optional, defaults to domain name)"
    echo "  -s    Silent mode (suppress banner)"
    echo "  -v    Verbose mode (also log output to file)"
    echo "  -f    Path to subjack fingerprints.json (optional, auto-detected if omitted)"
    echo "  -h    Show this help message"
    exit 1
}

# Parse arguments
while getopts "d:o:svf:h" opt; do
    case $opt in
        d) DOMAIN=$OPTARG ;;
        o) OUTPUT_DIR=$OPTARG ;;
        s) SILENT=true ;;
        v) VERBOSE=true ;;
        f) SUBJACK_FINGERPRINTS=$OPTARG ;;
        h) usage ;;
        *) usage ;;
    esac
done

# Validate domain is provided and well-formed
if [ -z "$DOMAIN" ]; then
    echo -e "${RED}[!] Error: Domain is required.${NC}"
    usage
fi

if ! [[ "$DOMAIN" =~ ^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$ ]]; then
    echo -e "${RED}[!] Error: '$DOMAIN' does not look like a valid domain.${NC}"
    exit 1
fi

# Set output directory if not provided
if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="$DOMAIN"
fi

# Initialise log file path now so check_dependencies output is captured with -v.
# $OUTPUT_DIR must exist before log() can append to it.
if [ "$VERBOSE" = true ]; then
    mkdir -p "$OUTPUT_DIR"
    LOG_FILE="$OUTPUT_DIR/recon.log"
fi

# Print banner unless silent
if [ "$SILENT" = false ]; then
    print_banner
fi

# Trap SIGINT/SIGTERM for a clean exit message
trap 'echo -e "\n${RED}[!] Interrupted. Partial results saved in $OUTPUT_DIR/${NC}"; exit 130' INT TERM

# log() — echoes to terminal and optionally appends (ANSI-stripped) to log file
log() {
    local msg="$1"
    echo -e "$msg"
    if [ "$VERBOSE" = true ] && [ -n "$LOG_FILE" ]; then
        echo "$msg" | sed -E 's/\x1b\[[0-9;]*m//g' >> "$LOG_FILE"
    fi
}

# Function to check dependencies
check_dependencies() {
    log "${BLUE}[*] Checking installed dependencies...${NC}"
    # amass is excluded: the amass block is optional/commented-out
    local deps=("assetfinder" "subfinder" "httprobe" "subjack" "nmap" "waybackurls" "nuclei")
    local missing=false

    for tool in "${deps[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log "${RED}[!] $tool is not installed.${NC}"
            missing=true
        else
            log "${GREEN}[+] $tool is installed.${NC}"
        fi
    done

    if [ "$missing" = true ]; then
        log "${RED}[!] Please install missing tools before running this script.${NC}"
        exit 1
    fi
}

# Function to create output directories
setup_directories() {
    log "${BLUE}[*] Setting up directory structure in $OUTPUT_DIR/...${NC}"
    mkdir -p \
        "$OUTPUT_DIR/recon/scans" \
        "$OUTPUT_DIR/recon/httprobe" \
        "$OUTPUT_DIR/recon/potential_takeovers" \
        "$OUTPUT_DIR/recon/wayback/params" \
        "$OUTPUT_DIR/recon/wayback/extensions" \
        "$OUTPUT_DIR/recon/nuclei"

    touch "$OUTPUT_DIR/recon/httprobe/alive.txt"
    touch "$OUTPUT_DIR/recon/httprobe/alive_with_protocol.txt"
    touch "$OUTPUT_DIR/recon/final.txt"

    if [ "$VERBOSE" = true ]; then
        log "${BLUE}[*] Logging output to $LOG_FILE${NC}"
    fi
}

# Function for subdomain enumeration (subfinder + assetfinder run in parallel)
enumerate_subdomains() {
    log "${BLUE}[*] Starting subdomain enumeration...${NC}"

    local tmp_subfinder="$OUTPUT_DIR/recon/subfinder.tmp"
    local tmp_assetfinder="$OUTPUT_DIR/recon/assetfinder.tmp"

    log "${YELLOW}[*] Running subfinder and assetfinder in parallel...${NC}"

    subfinder -d "$DOMAIN" -silent > "$tmp_subfinder" &
    local pid_sub=$!

    assetfinder --subs-only "$DOMAIN" > "$tmp_assetfinder" &
    local pid_asset=$!

    wait "$pid_sub"    && log "${GREEN}[+] subfinder complete.${NC}"    || log "${YELLOW}[!] subfinder exited with errors.${NC}"
    wait "$pid_asset"  && log "${GREEN}[+] assetfinder complete.${NC}"  || log "${YELLOW}[!] assetfinder exited with errors.${NC}"

    # Merge both results, deduplicate, write to final.txt
    cat "$tmp_subfinder" "$tmp_assetfinder" 2>/dev/null | sort -u > "$OUTPUT_DIR/recon/final.txt"
    rm -f "$tmp_subfinder" "$tmp_assetfinder"

    log "${GREEN}[+] Found $(wc -l < "$OUTPUT_DIR/recon/final.txt") unique subdomains.${NC}"
}

# Function for live host discovery
check_live_hosts() {
    log "${BLUE}[*] Probing for live hosts with httprobe...${NC}"

    if [ ! -s "$OUTPUT_DIR/recon/final.txt" ]; then
        log "${YELLOW}[!] No subdomains found — skipping live host probe.${NC}"
        return
    fi

    # Keep protocol-prefixed URLs (needed by nuclei) and a hostname-only copy (needed by nmap/subjack)
    cat "$OUTPUT_DIR/recon/final.txt" \
        | httprobe -c 50 \
        | sort -u > "$OUTPUT_DIR/recon/httprobe/alive_with_protocol.txt"

    sed -E 's|https?://||' "$OUTPUT_DIR/recon/httprobe/alive_with_protocol.txt" \
        | sort -u > "$OUTPUT_DIR/recon/httprobe/alive.txt"

    log "${GREEN}[+] Found $(wc -l < "$OUTPUT_DIR/recon/httprobe/alive.txt") live hosts.${NC}"
}

# Function for subdomain takeover check
check_takeovers() {
    log "${BLUE}[*] Checking for subdomain takeovers...${NC}"

    # Auto-detect fingerprints.json if -f was not supplied
    if [ -z "$SUBJACK_FINGERPRINTS" ]; then
        local candidates=(
            "$HOME/go/pkg/mod/github.com/haccer/subjack/fingerprints.json"
            "$HOME/go/src/github.com/haccer/subjack/fingerprints.json"
            "/usr/local/share/subjack/fingerprints.json"
        )
        for candidate in "${candidates[@]}"; do
            if [ -f "$candidate" ]; then
                SUBJACK_FINGERPRINTS="$candidate"
                break
            fi
        done
    fi

    if [ -z "$SUBJACK_FINGERPRINTS" ] || [ ! -f "$SUBJACK_FINGERPRINTS" ]; then
        log "${YELLOW}[!] subjack fingerprints.json not found — skipping takeover check.${NC}"
        log "${YELLOW}    Provide the path with: -f <path/to/fingerprints.json>${NC}"
        return
    fi

    if [ ! -s "$OUTPUT_DIR/recon/final.txt" ]; then
        log "${YELLOW}[!] No subdomains found — skipping takeover check.${NC}"
        return
    fi

    subjack -w "$OUTPUT_DIR/recon/final.txt" -t 100 -timeout 30 -ssl \
        -c "$SUBJACK_FINGERPRINTS" \
        -o "$OUTPUT_DIR/recon/potential_takeovers/potential_takeovers.txt" -v \
        || log "${YELLOW}[!] subjack exited with errors.${NC}"
}

# Function for port scanning
scan_ports() {
    log "${BLUE}[*] Scanning for open ports with Nmap...${NC}"

    if [ ! -s "$OUTPUT_DIR/recon/httprobe/alive.txt" ]; then
        log "${YELLOW}[!] No live hosts found — skipping port scan.${NC}"
        return
    fi

    nmap -iL "$OUTPUT_DIR/recon/httprobe/alive.txt" -T4 \
        -oA "$OUTPUT_DIR/recon/scans/scanned" \
        || log "${YELLOW}[!] nmap exited with errors.${NC}"
}

# Function for Wayback Machine recon
wayback_recon() {
    log "${BLUE}[*] Scraping Wayback Machine data...${NC}"

    # timeout prevents indefinite hangs on large subdomain lists
    cat "$OUTPUT_DIR/recon/final.txt" \
        | timeout 300 waybackurls \
        | sort -u > "$OUTPUT_DIR/recon/wayback/wayback_output.txt" \
        || log "${YELLOW}[!] waybackurls exited with errors or timed out after 5 min.${NC}"

    log "${GREEN}[+] Found $(wc -l < "$OUTPUT_DIR/recon/wayback/wayback_output.txt") archived URLs.${NC}"

    log "${BLUE}[*] Extracting parameters and extensions...${NC}"

    # Fixed regex: match URLs that contain a query parameter (e.g. ?foo=)
    grep -E '\?[^&=]+=' "$OUTPUT_DIR/recon/wayback/wayback_output.txt" \
        | cut -d '=' -f 1 \
        | sort -u > "$OUTPUT_DIR/recon/wayback/params/wayback_params.txt" || true

    log "${GREEN}[+] Extracted $(wc -l < "$OUTPUT_DIR/recon/wayback/params/wayback_params.txt") unique parameter names.${NC}"

    # Extract URLs by extension (anchored so .js doesn't match .json, etc.)
    for ext in js json php aspx jsp; do
        grep -iE "\.$ext(\?|#|$)" "$OUTPUT_DIR/recon/wayback/wayback_output.txt" \
            > "$OUTPUT_DIR/recon/wayback/extensions/$ext.txt" || true
    done
}

# Function for Nuclei scanning
run_nuclei() {
    log "${BLUE}[*] Running Nuclei vulnerability scan...${NC}"

    if [ ! -s "$OUTPUT_DIR/recon/httprobe/alive_with_protocol.txt" ]; then
        log "${YELLOW}[!] No live hosts found — skipping Nuclei scan.${NC}"
        return
    fi

    # Omit -t to use all templates installed in the default nuclei path.
    # If this fails with "no templates found", run: nuclei -update-templates
    nuclei -l "$OUTPUT_DIR/recon/httprobe/alive_with_protocol.txt" \
        -o "$OUTPUT_DIR/recon/nuclei/nuclei_report.txt" \
        || log "${YELLOW}[!] nuclei exited with errors. If templates are missing, run: nuclei -update-templates${NC}"
}

# Function to generate summary Markdown report
generate_report() {
    log "${BLUE}[*] Generating summary report...${NC}"
    local report="$OUTPUT_DIR/report.md"

    {
        echo "# Reconnaissance Report for $DOMAIN"
        echo "Date: $(date)"
        echo ""

        echo "## Subdomains"
        echo "- Total Unique Subdomains: $(wc -l < "$OUTPUT_DIR/recon/final.txt")"
        echo "- Live Hosts: $(wc -l < "$OUTPUT_DIR/recon/httprobe/alive.txt")"
        echo ""

        echo "## Wayback Machine"
        echo "- Archived URLs: $(wc -l < "$OUTPUT_DIR/recon/wayback/wayback_output.txt" 2>/dev/null || echo 0)"
        echo "- Unique Parameter Names: $(wc -l < "$OUTPUT_DIR/recon/wayback/params/wayback_params.txt" 2>/dev/null || echo 0)"
        echo ""

        echo "## Port Scan"
        local nmap_file="$OUTPUT_DIR/recon/scans/scanned.nmap"
        if [ -f "$nmap_file" ] && [ -s "$nmap_file" ]; then
            echo '```'
            grep -E "^Host:|^[0-9]+/tcp|^[0-9]+/udp" "$nmap_file" || true
            echo '```'
        else
            echo "- No port scan results available."
        fi
        echo ""

        echo "## Potential Subdomain Takeovers"
        local takeovers="$OUTPUT_DIR/recon/potential_takeovers/potential_takeovers.txt"
        if [ -s "$takeovers" ]; then
            cat "$takeovers"
        else
            echo "- No subdomain takeovers detected."
        fi
        echo ""

        echo "## Nuclei Vulnerability Scan"
        local nuclei_report="$OUTPUT_DIR/recon/nuclei/nuclei_report.txt"
        if [ -s "$nuclei_report" ]; then
            echo "### Vulnerabilities Found"
            cat "$nuclei_report"
        else
            echo "- No vulnerabilities found by Nuclei."
        fi
    } > "$report"

    log "${GREEN}[+] Report generated at $report${NC}"
}

# Main execution flow
check_dependencies
setup_directories
enumerate_subdomains
check_live_hosts
check_takeovers
scan_ports
wayback_recon
run_nuclei
generate_report

log "${GREEN}[+] All recon tasks completed successfully!${NC}"
