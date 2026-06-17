# ReconX: Complete Platform Setup Guide

Welcome to the ReconX Stage 20 Setup Guide. This document provides step-by-step instructions to get the platform running from absolutely scratch, assuming a bare-metal or VM environment.

---

## 1. System Prerequisites

Before touching any code, ensure your environment has the following installed:
- **Python 3.11+**: Required for the FastAPI gateway and asynchronous subprocess features.
- **Node.js 18+ & npm**: Required to build and run the React frontend.
- **Git**: For version control.
- **Nmap**: Required locally for the `network_discovery` golden plugin.
- **Docker & Docker Compose (Optional)**: If you prefer the containerized release bundle.

---

## 2. Environment Configuration

The ReconX platform relies on strict environment isolation for security.
1. Navigate to the root directory `e:/ReconX/`.
2. Copy the example environment template:
   - **Linux/Mac**: `cp release/env_templates/.env.example .env`
   - **Windows**: `Copy-Item release\env_templates\.env.example -Destination .env`
3. Edit the `.env` file to include your actual API keys:
   - `SHODAN_API_KEY`
   - `VIRUSTOTAL_API_KEY`
   - `OPENAI_API_KEY`

> [!NOTE]
> The `SecretsManager` securely maps these global `.env` variables *only* to the specific isolated plugin subprocesses that require them, preventing global credential leaks.

---

## 3. Backend API Setup

ReconX's core orchestration spine runs on FastAPI.
1. Open a terminal and navigate to `e:/ReconX/`.
2. It is highly recommended to create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```
3. Install the core dependencies AND the golden plugin dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This will install `fastapi`, `uvicorn`, `PyYAML`, `requests`, `beautifulsoup4`, `dnspython`, `python-nmap`, and `openai`.*

4. Verify the `outputs/` and `audit/` directories exist (the startup script will handle this automatically).

---

## 4. Frontend Dashboard Setup

The Live Operations Dashboard is built on React and Vite.
1. Open a **new** terminal window (keep the backend one free).
2. Navigate to the frontend directory:
   ```bash
   cd e:/ReconX/dashboard/frontend/
   ```
3. Install the Node modules:
   ```bash
   npm install
   ```

---

## 5. Launching ReconX (Bare-Metal)

We provide automated bootstrapping scripts in the `release/startup_scripts/` directory.

### Starting the Platform
**On Windows PowerShell:**
```powershell
cd e:\ReconX
.\release\startup_scripts\start.ps1
```

**On Linux/Bash:**
```bash
cd /e/ReconX
chmod +x release/startup_scripts/start.sh
./release/startup_scripts/start.sh
```

This will boot the API Gateway, Orchestrator, and EventBus on `http://127.0.0.1:8000`.

### Starting the Dashboard
In your frontend terminal (`e:/ReconX/dashboard/frontend/`), run:
```bash
npm run dev
```
The console will output a local URL (e.g., `http://localhost:5173/`). Open this in your browser to view the Live Operations Dashboard.

---

## 6. Launching ReconX (Docker/Containerized)

If you have Docker installed and prefer the packaged release:
1. Navigate to the root directory `e:/ReconX/`.
2. Run the deployment bundle:
   ```bash
   docker-compose -f release/deployment_bundle/docker-compose.yml up --build
   ```
This will automatically build the `Dockerfile.api` and the frontend, bridging them via a local Docker network.

---

## 7. Verification & Your First Workflow

1. Open your browser to the Dashboard URL.
2. Ensure the **System Health** widget shows "WebSocket: Connected".
3. Navigate to the **Workflow Control** tab.
4. Enter a target domain (e.g., `example.com`) and click **Launch Golden Workflow**.
5. Switch to the **Live Monitor** tab immediately. You should see a live terminal stream of `plugin_started`, `plugin_progress`, and `plugin_completed` events streaming across the WebSocket.
6. Once the workflow is complete, navigate to the **Report Center** to download the generated Markdown intelligence report.

---

## Troubleshooting

- **Subprocess failures**: If you see `Subprocess failed with code 1` with a `ModuleNotFoundError`, double-check that you have activated your `venv` and run `pip install -r requirements.txt`.
- **WebSocket disconnects**: Ensure the FastAPI server is running. The dashboard will automatically attempt to reconnect every 3 seconds.
- **Nmap errors**: If the `network_discovery` plugin fails, ensure the `nmap` executable is installed at the OS level and added to your System PATH.
