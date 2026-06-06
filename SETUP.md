# ReconX V2.0.0 — Ultimate Setup & Configuration Guide

Welcome to **ReconX V2.0.0**, the consolidated enterprise reconnaissance and orchestration platform. This guide will walk you through installing the core engine, setting up external dependencies, configuring APIs, and launching your first scan.

---

## 1. Prerequisites

ReconX is built on Python and JavaScript. To run the full platform including the dashboard, ensure you have:
- **Python 3.10+**
- **Node.js 18+** (for the Dashboard)
- **Go 1.20+** (for installing optional Go-based security binaries)
- **Git**

---

## 2. Core Installation

The installation process is fully automated. It will create an isolated virtual environment (`venv`), install all Python dependencies, and register the `reconx` global command-line launcher.

### On Linux / macOS
Open your terminal in the `Reconx_V_2.0.0` directory and run:
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### On Windows
Open PowerShell as Administrator in the `Reconx_V_2.0.0` directory and run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\scripts\install.ps1
```

> [!TIP]
> After installation, you must **restart your terminal** or run `source ~/.bashrc` (Linux) / `source ~/.zshrc` (Mac) to use the global `reconx` command.

---

## 3. External Security Tools (Optional but Recommended)

ReconX V2.0.0 integrates capabilities from 50 different tools. Many core features rely on external Go binaries (e.g., `naabu`, `katana`, `httpx`).

To install all missing Go tools automatically, run:
```bash
chmod +x scripts/install_tools.sh
./scripts/install_tools.sh
```
*Note: Ensure your Go workspace (`$HOME/go/bin` on Linux or `%USERPROFILE%\go\bin` on Windows) is added to your system `PATH`.*

---

## 4. Configuration

### A. Core Configuration (`config.yaml`)
The engine's default settings are located in `config.yaml` at the root of the project. 

```yaml
system:
  log_level: "INFO"               # Set to "DEBUG" for troubleshooting
  max_concurrent_tasks: 10        # Reduce if you experience system lag
  timeout_seconds: 3600           # Global maximum time for a workflow
  project_base_dir: "projects"

api:
  host: "127.0.0.1"               # The FastAPI binding address
  port: 8000
```
*You rarely need to change these unless deploying to a remote server.*

### B. Secrets & API Keys (`.env`)
To use advanced OSINT and AI features (like Shodan, GitHub integration, or LLM reporting), you must create an `.env` file.

1. Copy the template: `cp .env.example .env` (If `.env.example` does not exist, simply create `.env`).
2. Add your keys:
```env
# AI / LLM Keys
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="..."

# OSINT Keys
SHODAN_API_KEY="..."
GITHUB_TOKEN="ghp_..."
VIRUSTOTAL_API_KEY="..."
```
ReconX will automatically load these secrets securely into the plugin subprocesses when required.

---

## 5. Dashboard Setup

The React/Vite dashboard provides a beautiful visual interface for managing projects and viewing scan results. 

If it was not built during installation, you can build it manually:

```bash
cd dashboard
npm install
npm run build
cd ..
```
*ReconX's API gateway will automatically detect the `dashboard/dist/` folder and serve the frontend at `http://127.0.0.1:8000`.*

---

## 6. System Validation (Doctor)

Before running your first scan, use the built-in diagnostic tool to ensure everything is configured correctly:

```bash
reconx doctor
```
**Expected Output:**
- Python dependencies: `[PASS]`
- Directories (plugins, workflows): `[PASS]`
- Database Write Test: `[PASS]`
- External Tools: `[WARN]` (Warnings are fine; it just means an optional capability like `masscan` won't be used).

If any `[FAIL]` messages appear, read the hint provided to fix the issue.

---

## 7. Running Your First Scan

You are now ready to orchestrate a scan using the interactive CLI:

1. **Start the Interactive Menu**:
   ```bash
   reconx
   ```
2. **Create a Project**: Select "Projects" -> "Create Project" (e.g., `test_target`).
3. **Run a Workflow**: Select "Run Scan" -> Choose your project -> Choose the `basic.yaml` workflow -> Enter a target like `scanme.nmap.org`.

Alternatively, use the **Dashboard**:
1. Start the server:
   ```bash
   reconx dashboard
   ```
2. Open your browser to `http://127.0.0.1:8000`.
3. Create a project and launch a workflow visually!

---

## 8. Updating & Uninstalling

- **Update**: Pull the latest code and install new Python dependencies safely.
  ```bash
  ./scripts/update.sh
  ```
- **Uninstall**: Remove the virtual environment and global command link.
  ```bash
  ./scripts/uninstall.sh
  ```

> [!WARNING]
> Uninstalling does **not** delete your `projects/` database or your `outputs/`. Your historical scan data is safe.
