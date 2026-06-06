# ReconX — Verified Installation & Setup Manual

> **Version:** 20.0.0 (Validated Release)  
> **Last Updated:** June 2026  
> **Platform:** Linux-Native Enterprise Reconnaissance

---

> [!NOTE]  
> Throughout this guide, `<RECONX_ROOT>` refers to your chosen installation directory (e.g., `/home/user/ReconX` or `/opt/ReconX`). All commands are designed to work regardless of where you clone the repository.

## 1. System Requirements

Ensure your system meets the following prerequisites before proceeding:
- **Operating System**: Kali Linux, Ubuntu 22.04+, Debian 12+, Arch, or Fedora
- **Python**: 3.11+
- **Node.js**: 18+ (For the Dashboard)
- **Nmap**: 7.90+ (For Network Discovery Plugin)

## 2. Environment Verification

We have included a script to automatically verify your system dependencies.

```bash
# Clone the repository
git clone https://github.com/reconx/reconx.git <RECONX_ROOT>
cd <RECONX_ROOT>

# Run the verification script
chmod +x scripts/verify_environment.sh
./scripts/verify_environment.sh
```

**Expected Output:**
```text
[PASS] Python (Python 3.11.x)
[PASS] pip (23.x)
[PASS] Node.js (v18.x)
[PASS] Nmap (7.90)
```
If any required tools report `[FAIL]`, please install them using your system's package manager (e.g., `sudo apt install nmap nodejs npm python3-venv`).

## 3. Python Environment Setup

ReconX uses an isolated virtual environment.

```bash
cd <RECONX_ROOT>
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Verify the Installation:**
```bash
python3 reconx.py --version
```
*Expected Output:* `ReconX Enterprise v30.0.0-enterprise` (or similar depending on active branch).

## 4. Configuration

```bash
cp .env.example .env
# Edit .env to add your OPENAI_API_KEY and other credentials
nano .env
```

## 5. Running the Backend API & Interactive CLI

ReconX can be operated purely from the terminal or via the Web Dashboard.

**To run the interactive terminal interface:**
```bash
cd <RECONX_ROOT>
source venv/bin/activate
python3 reconx.py
```

**To start the headless API Gateway (for the dashboard):**
```bash
cd <RECONX_ROOT>
source venv/bin/activate
python3 reconx.py dashboard
```
*Expected Output:* `[*] Starting Enterprise API Gateway...` (Runs on `http://127.0.0.1:8000`)

## 6. Dashboard Setup (Vite)

The ReconX Live Operations Dashboard uses React and Vite.

```bash
# Open a NEW terminal window
cd <RECONX_ROOT>/dashboard/frontend
npm install

# Start the development server
npm run dev
```

**Access the Dashboard:**
Open your browser and navigate to `http://localhost:5173`. 
*(Note: Earlier documentation erroneously listed port 3000. Vite defaults to 5173).*
