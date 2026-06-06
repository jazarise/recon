#!/bin/bash

# ==============================================================================
# PROJECT: BCHackTool Professional Edition
# VERSION: v4.0
# AUTHOR: ByCh4n
# DATE: 2026-01-09
# FEATURES: Modern UI/UX, Parallel Scanning, Real-time Progress,
#           Subdomain List Input, Clean TXT Reports
# ==============================================================================

set -uo pipefail

# --- CONFIGURATION ---
readonly VERSION="v4.0 Professional"
readonly WORKSPACE="$HOME/.bchacktool"
readonly RESULTS_DIR="$(pwd)/BCHackTool_Results"
readonly CONFIG_FILE="$WORKSPACE/config.json"
readonly LOG_FILE="$WORKSPACE/bchacktool.log"
readonly CHECKPOINT_DIR="$WORKSPACE/checkpoints"

# Performance settings
readonly MAX_PARALLEL_JOBS=10
readonly TIMEOUT_SECONDS=300

# Colors
readonly RED='\033[1;31m'
readonly GREEN='\033[1;32m'
readonly BLUE='\033[1;34m'
readonly CYAN='\033[1;36m'
readonly YELLOW='\033[1;33m'
readonly PURPLE='\033[1;35m'
readonly WHITE='\033[1;37m'
readonly BOLD='\033[1m'
readonly RESET='\033[0m'

# Global variables
declare -A API_KEYS
declare TARGET_DIR
declare SCAN_START_TIME
declare SELECTED_MODE=""

# --- [2] UTILITY FUNCTIONS ---

log() {
    local level=$1
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" >> "$LOG_FILE"
}

status() {
    echo -e "${BLUE}[INFO]${RESET} $1"
    log "INFO" "$1"
}

success() {
    echo -e "${GREEN}[✓]${RESET} $1"
    log "SUCCESS" "$1"
}

warning() {
    echo -e "${YELLOW}[⚠]${RESET} $1"
    log "WARN" "$1"
}

error() {
    echo -e "${RED}[✗]${RESET} $1"
    log "ERROR" "$1"
}

# --- [3] SYSTEM CHECKS ---

check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "Root privileges required. Run: sudo bash $0"
        exit 1
    fi
}

check_dependencies() {
    local missing=()
    local required_cmds=(git curl jq python3 perl unzip pv)

    for cmd in "${required_cmds[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing+=("$cmd")
        fi
    done

    if [[ ! -f "$WORKSPACE/.build_deps_installed" ]]; then
        local build_deps=(gcc make libpcap-dev)
        local missing_build=()

        for pkg in "${build_deps[@]}"; do
            if ! dpkg -l "$pkg" 2>/dev/null | grep -q "^ii"; then
                missing_build+=("$pkg")
            fi
        done

        if [[ ${#missing_build[@]} -gt 0 ]]; then
            warning "Missing build dependencies: ${missing_build[*]}"
            missing+=("${missing_build[@]}")
        fi

        if [[ ${#missing_build[@]} -eq 0 ]]; then
            touch "$WORKSPACE/.build_deps_installed"
        fi
    fi

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo ""
        status "Installing missing packages: ${missing[*]}"
        apt-get update -qq
        apt-get install -y -qq "${missing[@]}" 2>&1 | tee -a "$LOG_FILE"
        touch "$WORKSPACE/.build_deps_installed"
        success "System packages installed successfully"
        echo ""
    fi

    if ! command -v go &> /dev/null && [[ ! -f /usr/local/go/bin/go ]]; then
        echo ""
        status "Go programming language not found - Installing..."
        echo -e "${CYAN}  This is required for security tools (Subfinder, Naabu, etc.)${RESET}"

        local go_version="1.22.0"
        local go_archive="go${go_version}.linux-amd64.tar.gz"

        status "Downloading Go ${go_version}..."
        cd /tmp
        if wget -q --show-progress "https://go.dev/dl/${go_archive}" 2>&1; then
            status "Installing Go to /usr/local/go..."
            rm -rf /usr/local/go
            tar -C /usr/local -xzf "${go_archive}"
            rm "${go_archive}"

            export GOROOT=/usr/local/go
            export GOPATH=$HOME/go
            export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

            local profile_file="$HOME/.profile"
            [[ ! -f "$profile_file" ]] && profile_file="$HOME/.bashrc"
            if ! grep -q "export GOROOT=/usr/local/go" "$profile_file" 2>/dev/null; then
                echo 'export GOROOT=/usr/local/go' >> "$profile_file"
                echo 'export GOPATH=$HOME/go' >> "$profile_file"
                echo 'export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin' >> "$profile_file"
            fi

            local go_ver=$(/usr/local/go/bin/go version | awk '{print $3}')
            success "Go installed successfully: ${go_ver}"
            status "Go path configured: /usr/local/go/bin"
            echo ""
        else
            error "Failed to download Go. Check internet connection."
            return 1
        fi
    elif [[ -f /usr/local/go/bin/go ]] && ! command -v go &> /dev/null; then
        echo ""
        warning "Go found but not in PATH - Configuring environment..."
        export GOROOT=/usr/local/go
        export GOPATH=$HOME/go
        export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

        if ! grep -q "export GOROOT=/usr/local/go" /root/.profile 2>/dev/null; then
            echo 'export GOROOT=/usr/local/go' >> /root/.profile
            echo 'export GOPATH=$HOME/go' >> /root/.profile
            echo 'export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin' >> /root/.profile
        fi

        local go_ver=$(/usr/local/go/bin/go version | awk '{print $3}')
        success "Go environment configured: ${go_ver}"
        echo ""
    fi
}

setup_environment() {
    mkdir -p "$WORKSPACE" "$RESULTS_DIR" "$CHECKPOINT_DIR"

    # Setup Go environment
    if [[ -z "${GOROOT:-}" ]]; then
        export GOROOT=/usr/local/go
    fi

    export GOPATH=$HOME/go
    export PATH=$PATH:$GOROOT/bin:$GOPATH/bin

    if [[ ! -f "$CONFIG_FILE" ]]; then
        cat > "$CONFIG_FILE" <<EOF
{
    "api_keys": {
        "shodan": "",
        "virustotal": "",
        "securitytrails": "",
        "censys": ""
    },
    "notifications": {
        "telegram_bot_token": "",
        "telegram_chat_id": "",
        "discord_webhook": "",
        "slack_webhook": ""
    },
    "scan_settings": {
        "max_parallel": $MAX_PARALLEL_JOBS,
        "timeout": $TIMEOUT_SECONDS
    }
}
EOF
        success "Config file created at: $CONFIG_FILE"
    fi

    load_config
}

load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        API_KEYS[shodan]=$(jq -r '.api_keys.shodan // ""' "$CONFIG_FILE")
        API_KEYS[virustotal]=$(jq -r '.api_keys.virustotal // ""' "$CONFIG_FILE")
        API_KEYS[securitytrails]=$(jq -r '.api_keys.securitytrails // ""' "$CONFIG_FILE")
    fi
}

# --- [4] BANNER ---

banner() {
    clear
    echo ""
    echo -e "${RED}${BOLD}"
    echo "    ██████╗  ██████╗██╗  ██╗ █████╗  ██████╗██╗  ██╗████████╗"
    echo "    ██╔══██╗██╔════╝██║  ██║██╔══██╗██╔════╝██║ ██╔╝╚══██╔══╝"
    echo "    ██████╔╝██║     ███████║███████║██║     █████╔╝    ██║   "
    echo "    ██╔══██╗██║     ██╔══██║██╔══██║██║     ██╔═██╗    ██║   "
    echo "    ██████╔╝╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗   ██║   "
    echo "    ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   "
    echo -e "${RESET}"
    echo -e "${CYAN}    Professional Penetration Testing Framework${RESET}"
    echo -e "${YELLOW}    Version: ${VERSION} | Build: 2026.01${RESET}"
    echo ""
}

# --- [5] TOOL INSTALLATION ---

install_go_tool() {
    local tool=$1
    local name=$(basename "$tool")
    local force_update=${2:-false}
    local silent=${3:-false}

    if ! command -v "$name" &> /dev/null || [[ "$force_update" == "true" ]]; then
        if [[ "$silent" != "true" ]]; then
            if [[ "$force_update" == "true" ]]; then
                status "Updating $name to latest version..."
            else
                status "Installing $name..."
            fi
        fi
        local GO_BINARY=""
        local GOROOT_OVERRIDE=""
        local GOPATH_OVERRIDE="/root/go"

        if [[ -f /usr/local/go/bin/go ]]; then
            GO_BINARY="/usr/local/go/bin/go"
            GOROOT_OVERRIDE="/usr/local/go"
        elif command -v go &> /dev/null; then
            GO_BINARY=$(which go)
            GOROOT_OVERRIDE=$(go env GOROOT 2>/dev/null || echo "")
        else
            error "Go is not installed. Please run the script normally to install dependencies first."
            return 1
        fi

        mkdir -p "$GOPATH_OVERRIDE/bin"
        local output_dest="/dev/null"
        [[ "$silent" != "true" ]] && output_dest="$LOG_FILE"

        if env -i \
            HOME="/root" \
            GOROOT="$GOROOT_OVERRIDE" \
            GOPATH="$GOPATH_OVERRIDE" \
            PATH="$(dirname "$GO_BINARY"):/root/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
            "$GO_BINARY" install "$tool@latest" >> "$output_dest" 2>&1; then

            if [[ ":$PATH:" != *":/root/go/bin:"* ]]; then
                export PATH="/root/go/bin:$PATH"
            fi
            if [[ "$silent" != "true" ]]; then
                if [[ "$force_update" == "true" ]]; then
                    success "$name updated"
                else
                    success "$name installed"
                fi
            fi
        else
            if [[ "$silent" != "true" ]]; then
                error "Failed to install/update $name"
            fi
            return 1
        fi
    fi
}

update_all_tools() {
    clear
    echo ""
    echo -e "${BOLD}${CYAN}🔄 UPDATE ALL TOOLS${RESET}"
    echo ""

    # Ensure Go is in PATH
    if [[ -f /usr/local/go/bin/go ]] && ! command -v go &> /dev/null; then
        export GOROOT=/usr/local/go
        export GOPATH=$HOME/go
        export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
    fi

    echo -e "  ${CYAN}📦 Updating Go-based tools...${RESET}"
    echo ""

    local go_tools=(
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
        "github.com/projectdiscovery/naabu/v2/cmd/naabu"
        "github.com/projectdiscovery/httpx/cmd/httpx"
        "github.com/projectdiscovery/nuclei/v3/cmd/nuclei"
        "github.com/projectdiscovery/notify/cmd/notify"
        "github.com/tomnomnom/assetfinder"
        "github.com/tomnomnom/waybackurls"
        "github.com/lc/gau/v2/cmd/gau"
    )
    for tool in "${go_tools[@]}"; do
        local tool_name=$(basename "$tool")
        echo -e "     ${YELLOW}⏳${RESET} $tool_name"
    done
    echo ""
    echo -ne "     ${CYAN}Updating in parallel...${RESET}"
    for tool in "${go_tools[@]}"; do
        install_go_tool "$tool" "true" "true" &
    done
    wait
    echo -e "\r     ${GREEN}✓ Successfully updated ${#go_tools[@]} tools${RESET}     "
    echo ""

    echo -e "  ${CYAN}📦 Updating other tools...${RESET}"
    echo ""

    # Update findomain
    echo -ne "     ${YELLOW}⏳${RESET} Findomain..."
    if wget -q https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux.zip -O /tmp/findomain.zip 2>/dev/null; then
        unzip -o -q /tmp/findomain.zip -d /tmp 2>/dev/null
        chmod +x /tmp/findomain
        mv -f /tmp/findomain /usr/local/bin/ 2>/dev/null
        rm -f /tmp/findomain.zip
        echo -e "\r     ${GREEN}✓${RESET} Findomain        "
    else
        echo -e "\r     ${YELLOW}⚠${RESET} Findomain (failed)"
    fi


    echo ""
    echo -e "  ${GREEN}✅ All tools updated successfully!${RESET}"
    echo ""
}

install_tools() {
    status "Checking and installing required tools..."
    echo ""

    # Ensure Go environment is set up
    if [[ -f /usr/local/go/bin/go ]]; then
        export GOROOT=/usr/local/go
        # Use /root/go when running as root regardless of $HOME
        if [[ $EUID -eq 0 ]]; then
            export GOPATH=/root/go
        else
            export GOPATH=$HOME/go
        fi
        export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
    elif command -v go &> /dev/null; then
        # Use system Go if BCHackTool's Go not installed
        export GOROOT=$(go env GOROOT 2>/dev/null)
        if [[ $EUID -eq 0 ]]; then
            export GOPATH=/root/go
        else
            export GOPATH=$HOME/go
        fi
        export PATH=$PATH:$(dirname $(which go)):$GOPATH/bin
    fi

    local go_tools=(
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
        "github.com/projectdiscovery/naabu/v2/cmd/naabu"
        "github.com/projectdiscovery/httpx/cmd/httpx"
        "github.com/projectdiscovery/nuclei/v3/cmd/nuclei"
        "github.com/projectdiscovery/notify/cmd/notify"
        "github.com/tomnomnom/assetfinder"
        "github.com/tomnomnom/waybackurls"
        "github.com/lc/gau/v2/cmd/gau"
    )

    # Install Go tools in parallel
    local installed_any=false
    for tool in "${go_tools[@]}"; do
        local tool_name=$(basename "$tool")
        if ! command -v "$tool_name" &> /dev/null; then
            install_go_tool "$tool" &
            installed_any=true
        fi
    done
    wait

    # Install findomain
    if ! command -v findomain &> /dev/null; then
        status "Installing findomain..."
        wget -q https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux.zip -O /tmp/findomain.zip
        unzip -q /tmp/findomain.zip -d /tmp
        chmod +x /tmp/findomain
        mv /tmp/findomain /usr/local/bin/
        rm /tmp/findomain.zip
        success "Findomain installed"
        installed_any=true
    fi

    # Clone additional tools
    mkdir -p "$WORKSPACE/tools"


    # Update nuclei templates only on first install
    if command -v nuclei &> /dev/null && [[ ! -f "$WORKSPACE/.templates_updated" ]]; then
        status "Updating Nuclei templates (first time only)..."
        nuclei -update-templates -silent 2>&1 | tee -a "$LOG_FILE"
        touch "$WORKSPACE/.templates_updated"
        success "Nuclei templates updated"
    fi

    echo ""
    if $installed_any; then
        success "Tool installation completed!"
    else
        success "All tools are already installed!"
    fi
}

# --- [6] RECON ENGINE WITH PARALLEL PROCESSING ---

run_recon_tool() {
    local tool_name=$1
    local domain=$2
    local output=$3
    local status_file="${output}.status"

    case $tool_name in
        subfinder)
            timeout $TIMEOUT_SECONDS subfinder -d "$domain" -all -silent -o "$output" >/dev/null 2>&1
            if [[ $? -eq 124 ]]; then
                echo "TIMEOUT" > "$status_file"
            elif [[ -s "$output" ]]; then
                echo "OK" > "$status_file"
            else
                echo "EMPTY" > "$status_file"
            fi
            touch "$output"
            ;;
        assetfinder)
            timeout $TIMEOUT_SECONDS assetfinder --subs-only "$domain" > "$output" 2>/dev/null
            if [[ $? -eq 124 ]]; then
                echo "TIMEOUT" > "$status_file"
            elif [[ -s "$output" ]]; then
                echo "OK" > "$status_file"
            else
                echo "EMPTY" > "$status_file"
            fi
            touch "$output"
            ;;
        findomain)
            timeout $TIMEOUT_SECONDS findomain -t "$domain" -q -u "$output" >/dev/null 2>&1
            if [[ $? -eq 124 ]]; then
                echo "TIMEOUT" > "$status_file"
            elif [[ -s "$output" ]]; then
                echo "OK" > "$status_file"
            else
                echo "EMPTY" > "$status_file"
            fi
            touch "$output"
            ;;
        wayback)
            timeout $TIMEOUT_SECONDS sh -c "echo '$domain' | waybackurls 2>/dev/null | cut -d '/' -f 3 | grep -E '\.$domain$' | sort -u > '$output'"
            if [[ $? -eq 124 ]]; then
                echo "TIMEOUT" > "$status_file"
            elif [[ -s "$output" ]]; then
                echo "OK" > "$status_file"
            else
                echo "EMPTY" > "$status_file"
            fi
            touch "$output"
            ;;
        gau)
            timeout $TIMEOUT_SECONDS sh -c "echo '$domain' | gau --subs 2>/dev/null | cut -d '/' -f 3 | grep -E '\.$domain$' | sort -u > '$output'"
            if [[ $? -eq 124 ]]; then
                echo "TIMEOUT" > "$status_file"
            elif [[ -s "$output" ]]; then
                echo "OK" > "$status_file"
            else
                echo "EMPTY" > "$status_file"
            fi
            touch "$output"
            ;;
        crtsh)
            local http_code=$(timeout $TIMEOUT_SECONDS curl -s -o "$output" -w "%{http_code}" "https://crt.sh/?q=%25.$domain&output=json" 2>/dev/null)
            if [[ $? -eq 124 ]]; then
                echo "TIMEOUT" > "$status_file"
            elif [[ "$http_code" == "429" ]]; then
                echo "RATELIMIT" > "$status_file"
            elif [[ -s "$output" ]]; then
                jq -r '.[].name_value' "$output" 2>/dev/null | sed 's/\*\.//g' | grep -v '^$' | sort -u > "${output}.tmp"
                mv "${output}.tmp" "$output"
                if [[ -s "$output" ]]; then
                    echo "OK" > "$status_file"
                else
                    echo "EMPTY" > "$status_file"
                fi
            else
                echo "EMPTY" > "$status_file"
            fi
            touch "$output"
            ;;
        anubis)
            local http_code=$(timeout $TIMEOUT_SECONDS curl -s -o "$output" -w "%{http_code}" "https://anubisdb.com/anubis/subdomains/$domain" 2>/dev/null)
            if [[ $? -eq 124 ]]; then
                echo "TIMEOUT" > "$status_file"
            elif [[ "$http_code" == "429" ]]; then
                echo "RATELIMIT" > "$status_file"
            elif [[ -s "$output" ]]; then
                jq -r '.[]' "$output" 2>/dev/null | grep -v '^$' | sort -u > "${output}.tmp"
                mv "${output}.tmp" "$output"
                if [[ -s "$output" ]]; then
                    echo "OK" > "$status_file"
                else
                    echo "EMPTY" > "$status_file"
                fi
            else
                echo "EMPTY" > "$status_file"
            fi
            touch "$output"
            ;;
    esac
}

parallel_recon() {
    local domain=$1
    local output_dir=$2

    status "🔍 Running subdomain enumeration tools"
    echo ""

    local tools=(subfinder assetfinder findomain wayback gau crtsh anubis)
    local tool_names=("🔍 Subfinder" "🌐 Assetfinder" "📡 Findomain" "📚 Wayback" "🔗 GAU" "🔒 Crt.sh" "📋 Anubis")
    declare -A tool_pids

    # Launch all tools in parallel
    for i in "${!tools[@]}"; do
        run_recon_tool "${tools[$i]}" "$domain" "$output_dir/${tools[$i]}_raw.txt" &
        tool_pids[${tools[$i]}]=$!
    done

    # Wait for all to complete and show status
    for i in "${!tools[@]}"; do
        local tool="${tools[$i]}"
        local tool_name="${tool_names[$i]}"
        local pid="${tool_pids[$tool]}"

        wait "$pid" 2>/dev/null || true

        # Check status file
        local status_file="$output_dir/${tool}_raw.txt.status"
        if [[ -f "$status_file" ]]; then
            local status_code=$(cat "$status_file" 2>/dev/null)
            case "$status_code" in
                OK)
                    local count=$(wc -l < "$output_dir/${tool}_raw.txt" 2>/dev/null || echo 0)
                    echo -e "  ✅ ${tool_name}: ${GREEN}${count}${RESET} results"
                    ;;
                EMPTY)
                    echo -e "  ⚠️  ${tool_name}: ${YELLOW}0 results${RESET}"
                    ;;
                TIMEOUT)
                    echo -e "  ⏱️  ${tool_name}: ${YELLOW}timeout${RESET}"
                    ;;
                RATELIMIT)
                    echo -e "  🚫 ${tool_name}: ${YELLOW}rate limited${RESET}"
                    ;;
                *)
                    echo -e "  ❌ ${tool_name}: ${RED}failed${RESET}"
                    ;;
            esac
        else
            echo -e "  ❌ ${tool_name}: ${RED}no status${RESET}"
        fi
    done

    echo ""
    echo ""

    # Merge and deduplicate all results
    if ls "$output_dir"/*_raw.txt 1> /dev/null 2>&1; then
        cat "$output_dir"/*_raw.txt 2>/dev/null | \
            grep -v "^$" | \
            grep -v "^\*" | \
            grep -v "^#" | \
            grep -v "^OK$" | \
            grep -v "^FAIL$" | \
            grep '\.' | \
            sort -u > "$output_dir/subdomains_temp.txt" || true

        if [[ -s "$output_dir/subdomains_temp.txt" ]]; then
            mv "$output_dir/subdomains_temp.txt" "$output_dir/subdomains.txt"
            local count=$(wc -l < "$output_dir/subdomains.txt")
            success "✓ Total: $count unique subdomains"
            echo ""
            echo -e "${CYAN}  📋 Sample subdomains:${RESET}"
            head -5 "$output_dir/subdomains.txt" | while read -r sub; do
                echo -e "    ${GREEN}→${RESET} $sub"
            done
            if [[ $count -gt 5 ]]; then
                echo -e "    ${CYAN}... and $((count - 5)) more${RESET}"
            fi
            echo ""
        else
            echo "$domain" > "$output_dir/subdomains.txt"
            warning "⚠️  No subdomains found, using main domain only"
            echo ""
        fi
    else
        echo "$domain" > "$output_dir/subdomains.txt"
        warning "⚠️  No tool output generated, using main domain only"
        echo ""
    fi

    return 0
}

# --- [7] PORT SCANNING ---

scan_ports() {
    local input_file=$1
    local output_file=$2

    status "🔎 Scanning ports with Naabu (top 1000 ports)..."
    echo ""

    # Run naabu silently (rate 300 to avoid IDS/IPS detection)
    naabu -list "$input_file" \
        -exclude-cdn \
        -top-ports 1000 \
        -rate 300 \
        -silent \
        -o "$output_file" >/dev/null 2>&1

    # Show results
    if [[ -s "$output_file" ]]; then
        local count=$(wc -l < "$output_file")
        success "✓ Found $count open ports"
        echo ""
        # Show sample ports
        echo -e "${CYAN}  Sample ports:${RESET}"
        head -5 "$output_file" | while read -r port; do
            echo -e "    ${GREEN}→${RESET} $port"
        done
        if [[ $count -gt 5 ]]; then
            echo -e "    ${CYAN}... and $((count - 5)) more${RESET}"
        fi
        echo ""
        return 0
    else
        warning "No open ports found"
        echo ""
        return 0
    fi
}

# --- [8] WEB PROBING ---

probe_web_services() {
    local input_file=$1
    local output_file=$2

    status "🌐 Probing web services with Httpx..."
    echo ""

    # Run httpx completely silently
    httpx -l "$input_file" \
        -silent \
        -follow-redirects \
        -status-code \
        -title \
        -tech-detect \
        -json \
        -o "$output_file" >/dev/null 2>&1

    # Parse and show clean results
    if [[ -s "$output_file" ]]; then
        local count=0
        local alive_file="$(dirname "$output_file")/alive.txt"

        # Create alive.txt for nuclei
        > "$alive_file"

        echo ""
        while IFS= read -r line; do
            local url=$(echo "$line" | jq -r '.url // empty' 2>/dev/null)
            local status=$(echo "$line" | jq -r '.status_code // empty' 2>/dev/null)
            local title=$(echo "$line" | jq -r '.title // empty' 2>/dev/null | cut -c1-40)

            if [[ -n "$url" ]]; then
                # Add to alive.txt for nuclei
                echo "$url" >> "$alive_file"

                if [[ -n "$title" ]]; then
                    echo -e "  ${GREEN}[${status}]${RESET} $url ${CYAN}($title)${RESET}"
                else
                    echo -e "  ${GREEN}[${status}]${RESET} $url"
                fi
                ((count++))
            fi
        done < "$output_file"

        echo ""
        success "Found $count live web services"
        echo ""
        return 0
    else
        warning "No live web services found"
        # Create empty alive.txt
        touch "$(dirname "$output_file")/alive.txt"
        echo ""
        return 0
    fi
}

# --- [9] VULNERABILITY SCANNING ---

scan_vulnerabilities() {
    local mode=$1
    local target_dir=$2

    status "🔍 Starting Nuclei vulnerability scan (Mode: $mode)..."

    local templates=""
    local input_file=""
    local output_file="$target_dir/nuclei_results.json"
    local live_output="$target_dir/nuclei_live.json"

    # All modes now use ALL templates - no template filtering
    templates=""

    case $mode in
        A|WEB)
            # Web mode: target alive web services
            input_file="$target_dir/alive.txt"
            ;;
        B|DNS)
            # DNS mode: target all subdomains
            input_file="$target_dir/subdomains.txt"
            ;;
        C|NET)
            # Network mode: target open ports
            input_file="$target_dir/ports.txt"
            ;;
        ALL)
            # ALL mode: combine all targets
            {
                # Add alive URLs (for http templates)
                [[ -f "$target_dir/alive.txt" ]] && cat "$target_dir/alive.txt" 2>/dev/null

                # Add plain subdomains (for dns templates)
                [[ -f "$target_dir/subdomains.txt" ]] && cat "$target_dir/subdomains.txt" 2>/dev/null

                # Add ports (for network templates)
                [[ -f "$target_dir/ports.txt" ]] && cat "$target_dir/ports.txt" 2>/dev/null
            } | grep -v "^$" | sort -u > "$target_dir/all_targets.txt"
            input_file="$target_dir/all_targets.txt"
            ;;
    esac

    # Create empty output file first
    touch "$output_file"
    touch "$live_output"

    if [[ ! -f "$input_file" || ! -s "$input_file" ]]; then
        warning "No targets found for scanning, skipping Nuclei"
        success "No vulnerabilities found (no targets to scan)"
        return 0
    fi

    local target_count=$(wc -l < "$input_file" 2>/dev/null || echo 0)

    if [[ $target_count -eq 0 ]]; then
        warning "Target file is empty, skipping Nuclei"
        success "No vulnerabilities found (no targets to scan)"
        return 0
    fi

    echo ""
    echo -e "${CYAN}[⏳]${RESET} Scanning ${BOLD}$target_count targets${RESET} with Nuclei"
    echo ""
    echo -e "${YELLOW}     This may take several minutes depending on target size${RESET}"
    echo -e "${YELLOW}     Press Ctrl+C anytime to skip and generate report${RESET}"
    echo ""
    echo -e "${GREEN}[▶]${RESET} Starting vulnerability scan..."
    echo ""

    # Track if scan was interrupted by user
    local nuclei_interrupted_file="$target_dir/.nuclei_interrupted"
    echo "0" > "$nuclei_interrupted_file"

    # Allow Ctrl+C to skip nuclei
    trap 'echo "1" > "'"$nuclei_interrupted_file"'"; pkill -P $$ nuclei 2>/dev/null' INT

    set +e

    nuclei -l "$input_file" \
        $templates \
        -jsonl \
        -o "$live_output" \
        -rate-limit 150 \
        -bulk-size 25 \
        -c 25 2>&1 | while IFS= read -r line; do

        if echo "$line" | grep -q '"template-id"'; then
            local vuln_name=$(echo "$line" | grep -oP '"template-id"\s*:\s*"\K[^"]+' | head -1)
            local vuln_severity=$(echo "$line" | grep -oP '"severity"\s*:\s*"\K[^"]+' | head -1 | tr '[:lower:]' '[:upper:]')
            local vuln_url=$(echo "$line" | grep -oP '"matched-at"\s*:\s*"\K[^"]+' | head -1)
            local vuln_type=$(echo "$line" | grep -oP '"type"\s*:\s*"\K[^"]+' | head -1)

            [[ -z "$vuln_name" ]] && vuln_name=$(echo "$line" | grep -oP '"name"\s*:\s*"\K[^"]+' | head -1)
            [[ -z "$vuln_url" ]] && vuln_url=$(echo "$line" | grep -oP '"host"\s*:\s*"\K[^"]+' | head -1)

            if [[ -n "$vuln_name" ]] && [[ -n "$vuln_severity" ]]; then
                [[ ${#vuln_url} -gt 60 ]] && vuln_url="${vuln_url:0:60}..."
                case "$vuln_severity" in
                    CRITICAL)
                        echo -e "  ${RED}🔴 [CRITICAL]${RESET} ${BOLD}$vuln_name${RESET}"
                        [[ -n "$vuln_url" ]] && echo -e "     └─ Target: ${CYAN}$vuln_url${RESET}"
                        ;;
                    HIGH)
                        echo -e "  ${BOLD}${RED}🟠 [HIGH]${RESET} ${BOLD}$vuln_name${RESET}"
                        [[ -n "$vuln_url" ]] && echo -e "     └─ Target: ${CYAN}$vuln_url${RESET}"
                        ;;
                    MEDIUM)
                        echo -e "  ${YELLOW}🟡 [MEDIUM]${RESET} $vuln_name"
                        [[ -n "$vuln_url" ]] && echo -e "     └─ Target: ${CYAN}$vuln_url${RESET}"
                        ;;
                    LOW)
                        echo -e "  ${BLUE}🟢 [LOW]${RESET} $vuln_name"
                        [[ -n "$vuln_url" ]] && echo -e "     └─ Target: ${CYAN}$vuln_url${RESET}"
                        ;;
                    INFO)
                        echo -e "  ${CYAN}ℹ️  [INFO]${RESET} $vuln_name"
                        [[ -n "$vuln_url" ]] && echo -e "     └─ Target: ${CYAN}$vuln_url${RESET}"
                        ;;
                esac
            fi
        else
            # Show other output (warnings, errors, info messages)
            echo "$line"
        fi
    done

    # Capture the exit status of nuclei (from the pipe)
    local nuclei_exit=${PIPESTATUS[0]}

    # Check if scan was interrupted
    local was_interrupted=$(cat "$nuclei_interrupted_file" 2>/dev/null || echo "0")

    rm -f "$nuclei_interrupted_file"

    # Copy live output to final output
    [[ -f "$live_output" ]] && cat "$live_output" > "$output_file"
    rm -f "$live_output"

    set -e  # Re-enable exit on error

    # Reset trap
    trap - INT

    # Flag to track if we should show summary and advanced scanning
    local show_summary=true

    # If scan was interrupted by user, don't show summary or continue
    if [[ "$was_interrupted" == "1" ]]; then
        warning "Nuclei scan was interrupted - skipping summary and advanced scanning"
        warning "Partial results saved to: $output_file"
        show_summary=false
    # If Nuclei crashed or exited abnormally, don't show summary
    elif [[ $nuclei_exit -ne 0 ]]; then
        echo ""
        error "Nuclei scan failed with exit code $nuclei_exit"
        warning "This could indicate:"
        echo -e "${YELLOW}    • Network connectivity issues${RESET}"
        echo -e "${YELLOW}    • Out of memory${RESET}"
        echo -e "${YELLOW}    • Template errors${RESET}"
        echo -e "${YELLOW}    • Target unreachable${RESET}"
        echo ""
        warning "Partial results (if any) saved to: $output_file"
        warning "Skipping summary and advanced scanning"
        show_summary=false
    fi

    # Generate clean TXT report from Nuclei JSON results
    if [[ -f "$output_file" && -s "$output_file" ]]; then
        local txt_report="$target_dir/vulnerabilities.txt"
        echo "BCHackTool v4.0 - Vulnerability Scan Results" > "$txt_report"
        echo "=============================================" >> "$txt_report"
        echo "Scan Date: $(date '+%Y-%m-%d %H:%M:%S')" >> "$txt_report"
        echo "Target: $mode scan" >> "$txt_report"
        echo "" >> "$txt_report"

        # Parse JSON and create clean TXT output
        jq -r '.info.severity as $sev | .info.name as $name | .info["template-id"] as $tid | ."matched-at" as $url | "[\($sev | ascii_upcase)] \($name // $tid)\n  Target: \($url)\n"' "$output_file" 2>/dev/null >> "$txt_report" || echo "Error parsing results" >> "$txt_report"

        status "📄 Clean vulnerability report saved: vulnerabilities.txt"
    fi

    # Only show summary and run advanced scanning if scan completed successfully
    if [[ "$show_summary" == "true" ]]; then
        echo ""

    # Count vulnerabilities by severity
    local vuln_count=$(wc -l < "$output_file" 2>/dev/null || echo 0)
    local critical_count=0
    local high_count=0
    local medium_count=0
    local low_count=0
    local info_count=0

    if [[ $vuln_count -gt 0 ]]; then
        local severity_counts=$(jq -r '.info.severity' "$output_file" 2>/dev/null | sort | uniq -c | awk '{print $2":"$1}' || echo "")

        critical_count=$(echo "$severity_counts" | grep "^critical:" | cut -d: -f2 || echo 0)
        high_count=$(echo "$severity_counts" | grep "^high:" | cut -d: -f2 || echo 0)
        medium_count=$(echo "$severity_counts" | grep "^medium:" | cut -d: -f2 || echo 0)
        low_count=$(echo "$severity_counts" | grep "^low:" | cut -d: -f2 || echo 0)
        info_count=$(echo "$severity_counts" | grep "^info:" | cut -d: -f2 || echo 0)

        [[ -z "$critical_count" ]] && critical_count=0
        [[ -z "$high_count" ]] && high_count=0
        [[ -z "$medium_count" ]] && medium_count=0
        [[ -z "$low_count" ]] && low_count=0
        [[ -z "$info_count" ]] && info_count=0

        echo ""
        echo -e "  ${BOLD}${WHITE}🛡️  VULNERABILITY SUMMARY${RESET}"
        echo ""
        [[ $critical_count -gt 0 ]] && echo -e "     ${RED}🔴 Critical:${RESET} ${BOLD}$critical_count${RESET} ${RED}<- IMMEDIATE ACTION REQUIRED${RESET}"
        [[ $high_count -gt 0 ]] && echo -e "     ${BOLD}${RED}🟠 High:${RESET}     ${BOLD}$high_count${RESET}"
        [[ $medium_count -gt 0 ]] && echo -e "     ${YELLOW}🟡 Medium:${RESET}   $medium_count"
        [[ $low_count -gt 0 ]] && echo -e "     ${BLUE}🟢 Low:${RESET}      $low_count"
        [[ $info_count -gt 0 ]] && echo -e "     ${CYAN}ℹ️  Info:${RESET}     $info_count"
        echo ""
        echo -e "     ${BOLD}📊 Total:${RESET}    ${GREEN}$vuln_count findings${RESET}"
        echo ""
    else
        success "✓ No vulnerabilities found"
    fi
    fi

    return 0
}



# --- [11] NOTIFICATION SYSTEM ---

send_notification() {
    local message=$1

    # Telegram
    local telegram_token=$(jq -r '.notifications.telegram_bot_token // ""' "$CONFIG_FILE")
    local telegram_chat=$(jq -r '.notifications.telegram_chat_id // ""' "$CONFIG_FILE")

    if [[ -n "$telegram_token" && -n "$telegram_chat" ]]; then
        curl -s -X POST "https://api.telegram.org/bot${telegram_token}/sendMessage" \
            -d "chat_id=${telegram_chat}" \
            -d "text=${message}" \
            -d "parse_mode=HTML" > /dev/null 2>&1 || true
    fi

    # Discord
    local discord_webhook=$(jq -r '.notifications.discord_webhook // ""' "$CONFIG_FILE")

    if [[ -n "$discord_webhook" ]]; then
        curl -s -H "Content-Type: application/json" \
            -X POST \
            -d "{\"content\": \"$message\"}" \
            "$discord_webhook" > /dev/null 2>&1 || true
    fi
}

# --- [12] CHECKPOINT SYSTEM ---

save_checkpoint() {
    local domain=$1
    local stage=$2

    echo "$stage" > "$CHECKPOINT_DIR/${domain}.checkpoint"
}

load_checkpoint() {
    local domain=$1

    if [[ -f "$CHECKPOINT_DIR/${domain}.checkpoint" ]]; then
        cat "$CHECKPOINT_DIR/${domain}.checkpoint"
    else
        echo "start"
    fi
}

clear_checkpoint() {
    local domain=$1
    rm -f "$CHECKPOINT_DIR/${domain}.checkpoint"
}

# --- [13] MAIN SCANNER ---

run_subdomain_scan() {
    local subdomain_file=$1
    local mode=$2

    SCAN_START_TIME=$(date +%s)

    local timestamp=$(date +%Y%m%d_%H%M%S)
    local scan_name=$(basename "$subdomain_file" .txt)
    TARGET_DIR="$RESULTS_DIR/${scan_name}_${timestamp}"

    mkdir -p "$TARGET_DIR"

    # Copy subdomain list to target directory
    cp "$subdomain_file" "$TARGET_DIR/subdomains.txt"

    # Trap Ctrl+C to allow graceful skip
    trap 'echo -e "\n${YELLOW}[⚠]${RESET} Scan interrupted by user, continuing to report generation..."; return 0' INT

    banner
    echo -e "${BOLD}${YELLOW}    SCAN CONFIGURATION${RESET}"
    echo -e "    Target: ${BOLD}$scan_name${RESET}"
    echo -e "    Mode:   ${BOLD}$mode${RESET}"
    echo -e "    Type:   ${BOLD}Subdomain List (Skip Recon)${RESET}"
    echo -e "    Time:   ${BOLD}$(date '+%Y-%m-%d %H:%M:%S')${RESET}"
    echo ""

    local total_subdomains=$(wc -l < "$TARGET_DIR/subdomains.txt")
    status "Loaded $total_subdomains subdomains from file"
    echo ""

    # Stage 1: Port Scanning (skipping recon)
    if scan_ports "$TARGET_DIR/subdomains.txt" "$TARGET_DIR/ports.txt"; then
        success "Port scanning completed"
    fi

    # Stage 2: Web Probing
    if probe_web_services "$TARGET_DIR/ports.txt" "$TARGET_DIR/httpx_results.json"; then
        success "Web probing completed"
    fi

    # Stage 3: Vulnerability Scanning
    scan_vulnerabilities "$mode" "$TARGET_DIR"

    local scan_end_time=$(date +%s)
    local total_duration=$((scan_end_time - SCAN_START_TIME))

    echo ""
    echo -e "${BOLD}${GREEN}    SCAN COMPLETED!${RESET}"
    echo -e "    Duration: $(date -u -d @${total_duration} +"%H:%M:%S")"
    echo -e "    Results:  ${BLUE}$TARGET_DIR${RESET}"

    send_notification "✅ BCHackTool subdomain scan completed for $scan_name in $(date -u -d @${total_duration} +"%H:%M:%S")"

    read -p "Press Enter to continue..."
}

run_full_scan() {
    local scan_type=$1
    local input=$2
    local mode=$3

    SCAN_START_TIME=$(date +%s)

    local timestamp=$(date +%Y%m%d_%H%M%S)
    local scan_name=$(basename "$input" .txt)
    TARGET_DIR="$RESULTS_DIR/${scan_name}_${timestamp}"

    mkdir -p "$TARGET_DIR"

    # Trap Ctrl+C to allow graceful skip
    trap 'echo -e "\n${YELLOW}[⚠]${RESET} Scan interrupted by user, continuing to report generation..."; return 0' INT

    banner
    echo -e "${BOLD}${YELLOW}    SCAN CONFIGURATION${RESET}"
    echo -e "    Target: ${BOLD}$scan_name${RESET}"
    echo -e "    Mode:   ${BOLD}$mode${RESET}"
    echo -e "    Time:   ${BOLD}$(date '+%Y-%m-%d %H:%M:%S')${RESET}"
    echo ""

    # Clear any old checkpoints for fresh scan
    clear_checkpoint "$scan_name"

    # Stage 1: Recon
    local checkpoint=$(load_checkpoint "$scan_name")

    if [[ "$checkpoint" == "start" ]]; then
        if parallel_recon "$input" "$TARGET_DIR"; then
            save_checkpoint "$scan_name" "recon_done"
        else
            error "Recon failed"
            return 1
        fi
    fi

    # Stage 2: Port Scanning
    if [[ "$checkpoint" =~ ^(start|recon_done)$ ]]; then
        if scan_ports "$TARGET_DIR/subdomains.txt" "$TARGET_DIR/ports.txt"; then
            save_checkpoint "$scan_name" "ports_done"
        fi
    fi

    # Stage 3: Web Probing
    if [[ "$checkpoint" =~ ^(start|recon_done|ports_done)$ ]]; then
        if probe_web_services "$TARGET_DIR/ports.txt" "$TARGET_DIR/httpx_results.json"; then
            # alive.txt is already created by probe_web_services
            save_checkpoint "$scan_name" "web_done"
        fi
    fi

    # Stage 4: Vulnerability Scanning
    scan_vulnerabilities "$mode" "$TARGET_DIR"

    clear_checkpoint "$scan_name"

    local scan_end_time=$(date +%s)
    local total_duration=$((scan_end_time - SCAN_START_TIME))
    local duration_formatted=$(date -u -d @${total_duration} +"%H:%M:%S")

    # Count results
    local subdomain_count=$(wc -l < "$TARGET_DIR/subdomains.txt" 2>/dev/null || echo 0)
    local port_count=$(wc -l < "$TARGET_DIR/ports.txt" 2>/dev/null || echo 0)
    local alive_count=$(wc -l < "$TARGET_DIR/alive.txt" 2>/dev/null || echo 0)
    local vuln_count=$(wc -l < "$TARGET_DIR/nuclei_results.json" 2>/dev/null || echo 0)

    # Count by severity
    local critical_count=0
    local high_count=0
    local medium_count=0
    local low_count=0
    local info_count=0

    if [[ $vuln_count -gt 0 ]]; then
        critical_count=$(jq -r 'select(.info.severity=="critical") | .info.severity' "$TARGET_DIR/nuclei_results.json" 2>/dev/null | wc -l || echo 0)
        high_count=$(jq -r 'select(.info.severity=="high") | .info.severity' "$TARGET_DIR/nuclei_results.json" 2>/dev/null | wc -l || echo 0)
        medium_count=$(jq -r 'select(.info.severity=="medium") | .info.severity' "$TARGET_DIR/nuclei_results.json" 2>/dev/null | wc -l || echo 0)
        low_count=$(jq -r 'select(.info.severity=="low") | .info.severity' "$TARGET_DIR/nuclei_results.json" 2>/dev/null | wc -l || echo 0)
        info_count=$(jq -r 'select(.info.severity=="info") | .info.severity' "$TARGET_DIR/nuclei_results.json" 2>/dev/null | wc -l || echo 0)
    fi

    echo ""
    echo ""
    echo ""
    echo -e "  ${BOLD}${GREEN}🎯 SCAN COMPLETED SUCCESSFULLY${RESET}"
    echo ""
    echo ""
    echo -e "  ${BOLD}Target:${RESET}       ${CYAN}$scan_name${RESET}"
    echo -e "  ${BOLD}Duration:${RESET}     ${CYAN}$duration_formatted${RESET}"
    echo -e "  ${BOLD}Mode:${RESET}         ${CYAN}$mode (Comprehensive)${RESET}"
    echo ""
    echo ""
    echo -e "  ${BOLD}${CYAN}📡 DISCOVERY RESULTS${RESET}"
    echo ""
    echo -e "     ${WHITE}Subdomains:${RESET}     ${GREEN}$subdomain_count found${RESET}"
    echo -e "     ${WHITE}Open Ports:${RESET}     ${GREEN}$port_count found${RESET}"
    echo -e "     ${WHITE}Live Services:${RESET}  ${GREEN}$alive_count active${RESET}"
    echo ""
    echo ""
    if [[ $vuln_count -gt 0 ]]; then
        echo -e "  ${BOLD}${RED}🛡️  VULNERABILITY FINDINGS${RESET}"
        echo ""
        [[ $critical_count -gt 0 ]] && echo -e "     ${RED}🔴 Critical:${RESET}    ${BOLD}${RED}$critical_count${RESET}  ${RED}<-- IMMEDIATE ACTION REQUIRED${RESET}"
        [[ $high_count -gt 0 ]] && echo -e "     ${BOLD}${RED}🟠 High:${RESET}        ${BOLD}$high_count${RESET}"
        [[ $medium_count -gt 0 ]] && echo -e "     ${YELLOW}🟡 Medium:${RESET}      $medium_count"
        [[ $low_count -gt 0 ]] && echo -e "     ${BLUE}🟢 Low:${RESET}         $low_count"
        [[ $info_count -gt 0 ]] && echo -e "     ${CYAN}ℹ️  Info:${RESET}        $info_count"
        echo ""
        echo -e "     ${BOLD}📊 Total:${RESET}       ${BOLD}${GREEN}$vuln_count findings${RESET}"
    else
        echo -e "  ${BOLD}${CYAN}🛡️  VULNERABILITY FINDINGS${RESET}"
        echo ""
        echo -e "     ${GREEN}✓ No vulnerabilities found${RESET}"
    fi
    echo ""
    echo ""
    echo -e "  ${BOLD}${PURPLE}📄 OUTPUT FILES${RESET}"
    echo ""
    echo -e "     ${WHITE}Scan Results:${RESET} ${BLUE}$TARGET_DIR/${RESET}"
    echo ""
    echo ""

    send_notification "✅ BCHackTool scan completed for $scan_name in $duration_formatted"

    echo -e "${CYAN}Press Enter to return to main menu...${RESET}"
    read
}

# --- [14] MODE SELECTION ---

select_scan_mode() {
    echo ""
    echo -e "${BOLD}${PURPLE}    SELECT SCAN MODE${RESET}"
    echo ""
    echo -e "    ${BOLD}[A]${RESET} WEB APPLICATION SCAN"
    echo -e "        → XSS, SQLi, CVE, LFI, RCE Detection"
    echo ""
    echo -e "    ${BOLD}[B]${RESET} DNS & INFRASTRUCTURE SCAN"
    echo -e "        → Subdomain Takeover, DNS Misconfig"
    echo ""
    echo -e "    ${BOLD}[C]${RESET} NETWORK SERVICE SCAN"
    echo -e "        → FTP, SSH, Redis, MongoDB, SMTP"
    echo ""
    echo -e "    ${BOLD}[ALL]${RESET} COMPREHENSIVE SCAN"
    echo -e "        → Web + DNS + Network (Complete Analysis)"
    echo ""
    echo -ne "    ${CYAN}Mode>${RESET} "
    read -r choice_val
    choice_val=$(echo "$choice_val" | xargs)

    case ${choice_val,,} in
        a) SELECTED_MODE="A" ;;
        b) SELECTED_MODE="B" ;;
        c) SELECTED_MODE="C" ;;
        all) SELECTED_MODE="ALL" ;;
        *)
            error "Invalid selection!"
            SELECTED_MODE="INVALID"
            return 1
            ;;
    esac

    success "Mode selected: $SELECTED_MODE"
    return 0
}

# --- [15] SYSTEM STATUS ---

show_system_status() {
    clear
    echo ""
    echo -e "${BOLD}${CYAN}    🔧 SYSTEM & TOOLS STATUS${RESET}"
    echo ""

    # Check Go installation
    echo -e "${BOLD}${PURPLE}[1] 🔷 Go Programming Language${RESET}"
    if command -v go &> /dev/null; then
        local go_ver=$(go version 2>/dev/null | awk '{print $3}' || echo "unknown")
        local go_path=$(which go 2>/dev/null)
        local go_root=$(go env GOROOT 2>/dev/null || echo "not set")

        echo -e "    Status: ${GREEN}✓ INSTALLED${RESET}"
        echo -e "    Version: ${GREEN}${go_ver}${RESET}"
        echo -e "    Location: ${CYAN}${go_path}${RESET}"

        # Check if it's the system Go vs our installed Go
        if [[ "$go_path" == "/usr/bin/go" ]] && [[ -f /usr/local/go/bin/go ]]; then
            echo -e "    ${YELLOW}Note: System Go detected. BCHackTool tools at: /usr/local/go/bin${RESET}"
        fi

        if [[ "$go_root" != *"/usr/local/go"* ]] && [[ -d /usr/local/go ]]; then
            echo -e "    ${YELLOW}GOROOT: ${go_root} (expected: /usr/local/go)${RESET}"
            echo -e "    ${YELLOW}Tip: Tools may not work correctly. Run 'export PATH=/usr/local/go/bin:\$PATH'${RESET}"
        fi
    elif [[ -f /usr/local/go/bin/go ]]; then
        local go_ver=$(/usr/local/go/bin/go version | awk '{print $3}')
        echo -e "    Status: ${YELLOW}⚠ INSTALLED (not in PATH)${RESET}"
        echo -e "    Version: ${YELLOW}${go_ver}${RESET}"
        echo -e "    Location: ${CYAN}/usr/local/go/bin/go${RESET}"
        echo -e "    ${YELLOW}Action: Run 'source /root/.profile' or restart terminal${RESET}"
    else
        echo -e "    Status: ${RED}✗ NOT INSTALLED${RESET}"
        echo -e "    ${RED}Action: Will be installed automatically on next scan${RESET}"
    fi
    echo ""

    # Check security tools
    echo -e "${BOLD}${PURPLE}[2] 🛡️  Security Scanning Tools${RESET}"

    local tools=(
        "subfinder:Subfinder:github.com/projectdiscovery/subfinder"
        "assetfinder:Assetfinder:github.com/tomnomnom/assetfinder"
        "findomain:Findomain:github.com/Findomain/Findomain"
        "waybackurls:Waybackurls:github.com/tomnomnom/waybackurls"
        "gau:GAU:github.com/lc/gau"
        "naabu:Naabu:github.com/projectdiscovery/naabu"
        "httpx:Httpx:github.com/projectdiscovery/httpx"
        "nuclei:Nuclei:github.com/projectdiscovery/nuclei"
    )

    local installed_count=0
    local total_count=${#tools[@]}

    for tool_info in "${tools[@]}"; do
        IFS=':' read -r cmd name repo <<< "$tool_info"
        if command -v "$cmd" &> /dev/null; then
            local version=""
            # Different tools use different version flags
            case $cmd in
                subfinder|naabu|httpx|nuclei)
                    version=$("$cmd" -version 2>/dev/null | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "installed")
                    ;;
                assetfinder)
                    version=$("$cmd" --help 2>&1 | grep -i version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "installed")
                    ;;
                findomain)
                    version=$("$cmd" --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "installed")
                    ;;
                waybackurls|gau)
                    version=$("$cmd" -version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "installed")
                    ;;
                *)
                    version="installed"
                    ;;
            esac

            if [[ "$version" =~ ^v[0-9] ]]; then
                echo -e "    ${GREEN}✓${RESET} ${name}: ${GREEN}${version}${RESET}"
            else
                echo -e "    ${GREEN}✓${RESET} ${name}: ${GREEN}✓ Installed${RESET}"
            fi
            ((installed_count++))
        else
            echo -e "    ${RED}✗${RESET} ${name}: ${RED}Not installed${RESET}"
        fi
    done

    echo ""
    echo -e "    ${BOLD}Installation Progress: ${installed_count}/${total_count} tools${RESET}"

    if [[ $installed_count -eq $total_count ]]; then
        echo -e "    ${GREEN}All tools are ready!${RESET}"
    else
        echo -e "    ${YELLOW}Missing tools will be installed automatically on first run${RESET}"
    fi
    echo ""

    # Check system resources
    echo -e "${BOLD}${PURPLE}[3] 💻 System Resources${RESET}"

    local cpu_cores=$(nproc)
    local mem_total=$(free -h | awk '/^Mem:/ {print $2}')
    local mem_used=$(free -h | awk '/^Mem:/ {print $3}')
    local disk_space=$(df -h "$WORKSPACE" 2>/dev/null | awk 'NR==2 {print $4}' || echo "unknown")

    echo -e "    CPU Cores: ${CYAN}${cpu_cores}${RESET}"
    echo -e "    Memory: ${CYAN}${mem_used} / ${mem_total}${RESET}"
    echo -e "    Disk Space Available: ${CYAN}${disk_space}${RESET}"
    echo ""

    # Check Nuclei templates
    echo -e "${BOLD}${PURPLE}[4] 📦 Nuclei Templates${RESET}"

    if command -v nuclei &> /dev/null; then
        local template_count=$(nuclei -tl 2>/dev/null | wc -l || echo "0")
        if [[ $template_count -gt 0 ]]; then
            echo -e "    Templates: ${GREEN}${template_count} loaded${RESET}"
            if [[ -f "$WORKSPACE/.templates_updated" ]]; then
                local last_update=$(stat -c %y "$WORKSPACE/.templates_updated" 2>/dev/null | cut -d' ' -f1 || echo "unknown")
                echo -e "    Last Update: ${CYAN}${last_update}${RESET}"
            fi
        else
            echo -e "    Templates: ${YELLOW}Not initialized${RESET}"
            echo -e "    ${YELLOW}Run 'T' from main menu to update templates${RESET}"
        fi
    else
        echo -e "    Status: ${RED}Nuclei not installed${RESET}"
    fi
    echo ""

    # Check configuration
    echo -e "${BOLD}${PURPLE}[6] ⚙️  Configuration${RESET}"

    if [[ -f "$CONFIG_FILE" ]]; then
        echo -e "    Config File: ${GREEN}✓ Found${RESET}"
        echo -e "    Location: ${CYAN}${CONFIG_FILE}${RESET}"

        # Check API keys
        local shodan_key=$(jq -r '.api_keys.shodan // ""' "$CONFIG_FILE")
        local vt_key=$(jq -r '.api_keys.virustotal // ""' "$CONFIG_FILE")

        if [[ -n "$shodan_key" && "$shodan_key" != "" ]]; then
            echo -e "    Shodan API: ${GREEN}✓ Configured${RESET}"
        else
            echo -e "    Shodan API: ${YELLOW}⚠ Not configured${RESET}"
        fi

        if [[ -n "$vt_key" && "$vt_key" != "" ]]; then
            echo -e "    VirusTotal API: ${GREEN}✓ Configured${RESET}"
        else
            echo -e "    VirusTotal API: ${YELLOW}⚠ Not configured${RESET}"
        fi
    else
        echo -e "    Config File: ${RED}✗ Not found${RESET}"
    fi
    echo ""

    # Show workspace info
    echo -e "${BOLD}${PURPLE}[7] 📂 Workspace Information${RESET}"
    echo -e "    Results: ${CYAN}${RESULTS_DIR}${RESET}"
    echo -e "    Logs: ${CYAN}${LOG_FILE}${RESET}"

    if [[ -d "$RESULTS_DIR" ]]; then
        local scan_count=$(ls -1 "$RESULTS_DIR" 2>/dev/null | wc -l || echo "0")
        echo -e "    Previous Scans: ${CYAN}${scan_count}${RESET}"
    fi
    echo ""

    echo ""

    # Check if any tools are missing
    if [[ $installed_count -lt $total_count ]]; then
        echo -e "${YELLOW}[!]${RESET} Some tools are missing. Would you like to install them now? ${GREEN}(y/N)${RESET}"
        read -r install_choice
        install_choice=$(echo "$install_choice" | xargs)
        if [[ "$install_choice" =~ ^[Yy]$ ]]; then
            echo ""
            status "Installing missing tools..."
            echo ""

            # Force install all tools
            install_tools

            echo ""
            success "Installation complete! Press Enter to refresh status..."
            read -p ""
            show_system_status
            return
        fi
    fi

    read -p "Press Enter to return to main menu..."
}

# --- [16] WIKI ---

show_wiki() {
    clear
    echo ""
    echo -e "${BOLD}${PURPLE}    📖 BCHackTool v4.0 - PROFESSIONAL GUIDE${RESET}"
    echo ""
    echo -e "${BOLD}${CYAN}✨ NEW IN v4.0 (Enhanced UI/UX):${RESET}"
    echo ""
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Complete UI/UX Redesign${RESET} - Modern emoji-rich interface with visual hierarchy"
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Real-time Progress Dashboard${RESET} - Live Nuclei stats with in-place updates (no scrolling)"
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Color-coded Severity${RESET} - 🔴 Critical, 🟠 High, 🟡 Medium, 🔵 Low, 🔷 Info"
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Clean Spacing Design${RESET} - Universal terminal compatibility (no box-drawing chars)"
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Clean TXT Reports${RESET} - Human-readable vulnerability reports in current directory"
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Live Progress Bars${RESET} - Visual feedback with █ characters and percentages"
    echo ""
    echo -e "${BOLD}${CYAN}🎯 FEATURES FROM v4.0:${RESET}"
    echo ""
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Subdomain List Input${RESET} - Skip recon, use pre-collected subdomains (Option 3)"
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Full Nuclei Severity Scan${RESET} - Now scans ALL severities (info, low, medium, high, critical)"
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Real-time Nuclei Progress${RESET} - See live scan progress and statistics"
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Enhanced Template Coverage${RESET} - SSL/TLS, Headless, WebSocket, WHOIS templates"
    echo -e "  ${GREEN}✓${RESET} ${BOLD}System Status Check${RESET} - Press 'S' to view installed tools and versions"
    echo -e "  ${GREEN}✓${RESET} ${BOLD}Current Directory Output${RESET} - All results saved in BCHackTool_Results/ folder"
    echo ""
    echo -e "${BOLD}${CYAN}FEATURES FROM v3.1:${RESET}"
    echo ""
    echo -e "  ${GREEN}✓${RESET} Parallel scanning (10x faster)"
    echo -e "  ${GREEN}✓${RESET} Error handling & auto-retry"
    echo -e "  ${GREEN}✓${RESET} JSON output & structured data"
    echo -e "  ${GREEN}✓${RESET} Resume capability (continue interrupted scans)"
    echo -e "  ${GREEN}✓${RESET} Telegram/Discord notifications"
    echo -e "  ${GREEN}✓${RESET} API key integration (Shodan, VirusTotal, etc.)"
    echo -e "  ${GREEN}✓${RESET} Progress indicators & ETA"
    echo -e "  ${GREEN}✓${RESET} Comprehensive logging"
    echo ""
    echo ""
    echo -e "${BOLD}${CYAN}CONFIGURATION:${RESET}"
    echo ""
    echo -e "  Config file: ${BOLD}$CONFIG_FILE${RESET}"
    echo ""
    echo -e "  ${YELLOW}API Keys (for enhanced scanning):${RESET}"
    echo -e "    • Shodan API: https://account.shodan.io/"
    echo -e "    • VirusTotal API: https://virustotal.com/gui/my-apikey"
    echo -e "    • SecurityTrails API: https://securitytrails.com/"
    echo ""
    echo -e "  ${YELLOW}Notifications:${RESET}"
    echo -e "    • Telegram Bot Token & Chat ID"
    echo -e "    • Discord Webhook URL"
    echo -e "    • Slack Webhook URL"
    echo ""
    echo ""
    echo -e "${BOLD}${CYAN}SCAN MODES EXPLAINED:${RESET}"
    echo ""
    echo -e "  ${BOLD}[A] WEB SCAN:${RESET}"
    echo -e "      Targets: Live web applications only"
    echo -e "      Templates: HTTP, CVE, Vulnerabilities"
    echo -e "      Best for: Bug bounty web app testing"
    echo ""
    echo -e "  ${BOLD}[B] DNS SCAN:${RESET}"
    echo -e "      Targets: All subdomains (even non-HTTP)"
    echo -e "      Templates: DNS, Takeovers"
    echo -e "      Best for: Infrastructure assessment"
    echo ""
    echo -e "  ${BOLD}[C] NETWORK SCAN:${RESET}"
    echo -e "      Targets: Non-web services (FTP, SSH, etc.)"
    echo -e "      Templates: Network protocols"
    echo -e "      Best for: Internal network pentesting"
    echo ""
    echo -e "  ${BOLD}[ALL] COMPREHENSIVE:${RESET}"
    echo -e "      Targets: Everything combined"
    echo -e "      Templates: All categories"
    echo -e "      Best for: Complete security audit"
    echo ""
    echo ""
    echo -e "${BOLD}${CYAN}PIPELINE ARCHITECTURE:${RESET}"
    echo ""
    echo -e "  ${YELLOW}Stage 1: RECONNAISSANCE${RESET} (Parallel)"
    echo -e "    ─ Subfinder (Passive OSINT)"
    echo -e "    ─ Assetfinder (Web scraping)"
    echo -e "    ─ Findomain (Multi-source API)"
    echo -e "    ─ Wayback Machine (Archive.org)"
    echo -e "    ─ GAU (GetAllUrls)"
    echo -e "    ─ Crt.sh (Certificate logs)"
    echo -e "    ─ Anubis (Passive DNS)"
    echo ""
    echo -e "  ${YELLOW}Stage 2: PORT SCANNING${RESET}"
    echo -e "    ─ Naabu (Fast SYN scanner)"
    echo ""
    echo -e "  ${YELLOW}Stage 3: WEB PROBING${RESET}"
    echo -e "    ─ Httpx (HTTP probe + tech detection)"
    echo ""
    echo -e "  ${YELLOW}Stage 4: VULNERABILITY SCANNING${RESET}"
    echo -e "    ─ Nuclei (Template-based scanner)"
    echo ""
    echo -e "  ${YELLOW}Stage 5: REPORTING${RESET}"
    echo -e "    ─ JSON (Machine-readable)"
    echo -e "    ─ HTML (Human-readable)"
    echo -e "    ─ Notifications (Telegram/Discord)"
    echo ""
    echo ""
    echo -e "${BOLD}${CYAN}SUBDOMAIN LIST INPUT (NEW in v4.0):${RESET}"
    echo ""
    echo -e "  ${BOLD}When to use option 3?${RESET}"
    echo -e "    • Already have subdomain list from previous reconnaissance"
    echo -e "    • Want to skip recon phase and save time"
    echo -e "    • Testing specific subdomains"
    echo -e "    • Integrating with external recon tools"
    echo ""
    echo -e "  ${BOLD}File format example:${RESET}"
    echo -e "    ${YELLOW}subdomains.txt:${RESET}"
    echo -e "      example.com"
    echo -e "      www.example.com"
    echo -e "      api.example.com"
    echo -e "      mail.example.com"
    echo ""
    echo -e "  ${BOLD}What happens:${RESET}"
    echo -e "    ✓ SKIP: Reconnaissance phase"
    echo -e "    ✓ RUN: Port scanning (Naabu)"
    echo -e "    ✓ RUN: Web probing (Httpx)"
    echo -e "    ✓ RUN: Vulnerability scanning (Nuclei)"
    echo -e "    ✓ RUN: Report generation"
    echo ""
    echo ""
    echo -e "${BOLD}${CYAN}MENU SHORTCUTS:${RESET}"
    echo ""
    echo -e "  ${BOLD}Main Menu Options:${RESET}"
    echo -e "    ${CYAN}1-6${RESET}   - Numbered scan options"
    echo -e "    ${CYAN}S${RESET}     - System & Tools Status (check installed tools)"
    echo -e "    ${CYAN}T${RESET}     - Update Nuclei Templates"
    echo -e "    ${CYAN}U${RESET}     - Update All Tools to latest versions"
    echo -e "    ${CYAN}H${RESET}     - Help & Wiki (this guide)"
    echo -e "    ${CYAN}L${RESET}     - View Logs"
    echo -e "    ${CYAN}99${RESET}    - Clean & Uninstall"
    echo -e "    ${CYAN}0${RESET}     - Exit"
    echo ""
    echo ""
    echo -e "${BOLD}${CYAN}ADVANCED TIPS:${RESET}"
    echo ""
    echo -e "  • Resume interrupted scans automatically (checkpoint system)"
    echo -e "  • Check logs at: ${YELLOW}$LOG_FILE${RESET}"
    echo -e "  • Results saved with timestamp for comparison"
    echo -e "  • Use 'ALL' mode for comprehensive security audits"
    echo -e "  • Parallel processing reduces scan time by 70-80%"
    echo -e "  • Use option 3 (Subdomain List) to skip recon and save 30-50% time"
    echo -e "  • Full severity scanning helps find ALL potential issues"
    echo -e "  • Press ${CYAN}S${RESET} anytime to check tool installation status"
    echo -e "  • Results saved in clean TXT format in BCHackTool_Results/ folder"
    echo ""
    echo ""
    read -p "Press Enter to return to main menu..."
}

# --- [17] MAIN MENU ---

main_menu() {
    while true; do
        banner
        echo -e "${BOLD}${CYAN}    MAIN MENU${RESET}"
        echo ""
        echo -e "    ${GREEN}[1]${RESET}  🎯 Single Domain Scan"
        echo -e "    ${GREEN}[2]${RESET}  📁 Multiple Domains (from file)"
        echo -e "    ${GREEN}[3]${RESET}  ⚡ Scan with Subdomain List (Skip Recon)"
        echo -e "    ${GREEN}[4]${RESET}  🔑 Configure API Keys"
        echo -e "    ${GREEN}[5]${RESET}  🔔 Setup Notifications"
        echo -e "    ${GREEN}[6]${RESET}  📊 View Previous Scans"
        echo ""
        echo -e "    ${CYAN}[S]${RESET}  🔧 System & Tools Status"
        echo -e "    ${CYAN}[T]${RESET}  📦 Update Nuclei Templates"
        echo -e "    ${CYAN}[U]${RESET}  🔄 Update All Tools"
        echo ""
        echo -e "    ${YELLOW}[H]${RESET}  📖 Help & Wiki"
        echo -e "    ${YELLOW}[L]${RESET}  📋 View Logs"
        echo ""
        echo -e "    ${RED}[99]${RESET} 🧹 Clean & Uninstall"
        echo -e "    ${RED}[0]${RESET}  👋 Exit"
        echo ""
        echo -ne "    ${CYAN}>${RESET} "
        read -r choice
        choice=$(echo "$choice" | xargs)

        case ${choice,,} in
            1)
                echo ""
                echo -ne "${CYAN}🎯 Enter target domain: ${RESET}"
                read -r domain
                domain=$(echo "$domain" | xargs)
                if [[ -z "$domain" ]]; then
                    error "❌ Domain cannot be empty!"
                    sleep 1
                    continue
                fi

                # Validate domain format using grep
                if ! echo "$domain" | grep -qP '^[a-zA-Z0-9.-]+$'; then
                    error "❌ Invalid domain format! Use only letters, numbers, dots, and hyphens."
                    sleep 1
                    continue
                fi

                # Validate domain structure (must have at least one dot)
                if [[ ! "$domain" =~ \. ]]; then
                    warning "⚠️  Domain should contain at least one dot (e.g., example.com)"
                    echo -ne "${YELLOW}Continue anyway? (y/N): ${RESET}"
                    read -r confirm
                    confirm=$(echo "$confirm" | xargs)
                    if [[ ! "${confirm,,}" == "y" ]]; then
                        continue
                    fi
                fi

                if ! select_scan_mode; then
                    sleep 1
                    continue
                fi

                run_full_scan "single" "$domain" "$SELECTED_MODE"
                ;;
            2)
                echo ""
                echo -ne "${CYAN}📁 Enter file path: ${RESET}"
                read -r filepath
                filepath=$(echo "$filepath" | xargs)
                if [[ -z "$filepath" || ! -f "$filepath" ]]; then
                    error "❌ File not found!"
                    sleep 1
                    continue
                fi

                if ! select_scan_mode; then
                    sleep 1
                    continue
                fi

                status "📋 Processing domains from file..."
                local domain_count=$(wc -l < "$filepath")
                echo -e "${CYAN}    Found ${BOLD}$domain_count${RESET}${CYAN} domains to scan${RESET}"

                while read domain; do
                    [[ -z "$domain" ]] && continue
                    run_full_scan "single" "$domain" "$SELECTED_MODE"
                done < "$filepath"
                ;;
            3)
                echo ""
                echo -ne "${CYAN}⚡ Enter subdomain list file path: ${RESET}"
                read -r subdomain_file
                subdomain_file=$(echo "$subdomain_file" | xargs)
                if [[ -z "$subdomain_file" || ! -f "$subdomain_file" ]]; then
                    error "❌ File not found!"
                    sleep 1
                    continue
                fi

                if ! select_scan_mode; then
                    sleep 1
                    continue
                fi

                local sub_count=$(wc -l < "$subdomain_file")
                status "⚡ Skipping reconnaissance phase..."
                echo -e "${CYAN}    Using ${BOLD}$sub_count${RESET}${CYAN} pre-collected subdomains${RESET}"

                run_subdomain_scan "$subdomain_file" "$SELECTED_MODE"
                ;;
            4)
                echo ""
                status "🔑 Opening API key configuration..."
                ${EDITOR:-nano} "$CONFIG_FILE"
                load_config
                success "✓ Configuration updated!"
                sleep 1
                ;;
            5)
                echo ""
                status "🔔 Opening notification settings..."
                ${EDITOR:-nano} "$CONFIG_FILE"
                success "✓ Notification settings updated!"
                sleep 1
                ;;
            6)
                echo ""
                status "📊 Recent scans:"
                echo ""
                if [[ -d "$RESULTS_DIR" ]] && [[ $(ls -A "$RESULTS_DIR" 2>/dev/null | wc -l) -gt 0 ]]; then
                    ls -1dt "$RESULTS_DIR"/* 2>/dev/null | head -10 | while read -r scan_dir; do
                        local scan_name=$(basename "$scan_dir")
                        local scan_date=$(echo "$scan_name" | grep -oP '\d{8}_\d{6}' | sed 's/_/ /')
                        local vuln_file="$scan_dir/nuclei_results.json"
                        local vuln_count=0
                        [[ -f "$vuln_file" ]] && vuln_count=$(wc -l < "$vuln_file" 2>/dev/null || echo 0)

                        if [[ $vuln_count -gt 0 ]]; then
                            echo -e "    ${GREEN}●${RESET} $scan_name ${YELLOW}($vuln_count findings)${RESET}"
                        else
                            echo -e "    ${BLUE}●${RESET} $scan_name ${CYAN}(no findings)${RESET}"
                        fi
                    done
                else
                    echo -e "    ${YELLOW}No previous scans found${RESET}"
                fi
                echo ""
                read -p "Press Enter to continue..."
                ;;
            s)
                show_system_status
                ;;
            t)
                echo ""
                status "📦 Updating Nuclei templates..."
                nuclei -update-templates 2>&1 | tee -a "$LOG_FILE"
                success "✓ Templates updated!"
                sleep 2
                ;;
            u)
                echo ""
                update_all_tools
                read -p "Press Enter to continue..."
                ;;
            h)
                show_wiki
                ;;
            l)
                echo ""
                echo -e "${BOLD}${CYAN}📋 Recent Log Entries (Last 50 lines):${RESET}"
                echo ""
                tail -n 50 "$LOG_FILE" 2>/dev/null || echo -e "${YELLOW}No log entries found${RESET}"
                echo ""
                echo ""
                read -p "Press Enter to continue..."
                ;;
            99)
                echo ""
                echo -e "${BOLD}${RED}🧹 CLEAN & UNINSTALL${RESET}"
                echo ""
                echo -e "${YELLOW}⚠️  This will remove:${RESET}"
                echo -e "    • All scan results"
                echo -e "    • Configuration files"
                echo -e "    • Logs and checkpoints"
                echo -e "    • All downloaded tools"
                echo ""
                echo -ne "${RED}Are you sure? This cannot be undone! (y/N): ${RESET}"
                read -r confirm
                confirm=$(echo "$confirm" | xargs)
                if [[ "${confirm,,}" == "y" ]]; then
                    echo ""
                    echo -e "${BLUE}[INFO]${RESET} 🧹 Cleaning workspace..."
                    rm -rf "$WORKSPACE"
                    echo -e "${GREEN}[✓]${RESET} ✓ All data removed. Goodbye!"
                    exit 0
                else
                    echo ""
                    echo -e "${CYAN}Cancelled. No changes made.${RESET}"
                    sleep 1
                fi
                ;;
            0)
                echo ""
                echo -e "${GREEN}👋 Thanks for using BCHackTool! Stay safe.${RESET}"
                exit 0
                ;;
            *)
                error "❌ Invalid option!"
                sleep 1
                ;;
        esac
    done
}

# --- [18] ENTRY POINT ---

main() {
    check_root
    setup_environment
    check_dependencies
    install_tools

    log "INFO" "BCHackTool $VERSION started"

    main_menu
}

# Run
main "$@"