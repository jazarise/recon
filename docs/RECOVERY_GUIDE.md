# ReconX Recovery Guide
*Generated during Documentation Remediation*

This guide details steps to recover a broken ReconX environment.

## 1. Broken Virtual Environment
If you encounter `ModuleNotFoundError` despite installing dependencies, your virtual environment may be corrupted or bound to an older python version.

**Recovery:**
```bash
cd <RECONX_ROOT>
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Dependency Failures (Pip Errors)
If `pip install` fails due to C-extension build errors (often with packages like `psycopg2` or `cryptography`), ensure your OS has the necessary build tools.
```bash
sudo apt install build-essential python3-dev libffi-dev libssl-dev
```
Run `scripts/verify_environment.sh` to ensure base requirements are met.

## 3. Dashboard Failures (Vite)
If `npm run dev` hangs or throws `ESLint` / module resolution errors, your `node_modules` cache might be corrupt.
```bash
cd <RECONX_ROOT>/dashboard/frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
npm run dev
```

## 4. API Startup Failures (Port Conflicts)
If starting the dashboard backend fails with `[Errno 98] Address already in use`:
```bash
# Find the process blocking port 8000
lsof -i :8000
# Kill it (replace PID)
kill -9 <PID>
```
Alternatively, change the port in `.env` to `8080`.

## 5. Missing Modules or Commands
If ReconX claims a command like `nmap` is missing, you must install it at the system level. ReconX subprocess execution cannot run without the OS-level binary.
```bash
sudo apt install nmap whois dnsutils
```
