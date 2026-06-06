# ReconX — Unified Reconnaissance Orchestration Platform

> **For authorized security testing and educational purposes only.**

---

## What is ReconX?

ReconX is a modular, production-grade reconnaissance platform that combines
asset discovery, DNS intelligence, port scanning, web fingerprinting, AI-powered
analysis, and multi-format reporting into a single interactive workflow.

```
reconx
```

Launches a full interactive CLI. One command. Complete operator experience.

---

## Quick Start

```bash
# Clone / extract ReconX
cd ReconX

# Install Python dependencies
pip install -r requirements.txt

# (Optional) Install system tools for full capability
# apt install nmap naabu httpx nuclei -y   # Kali/Debian

# Run interactive mode
python3 reconx.py

# Or use the install script to get the `reconx` command globally
bash scripts/install.sh
```

---

## Usage

### Interactive Mode (recommended)
```bash
python3 reconx.py
```
Full menu-driven experience: create projects, select scan profiles, view results.

### CLI Mode
```bash
# Run scan on an existing project
python3 reconx.py scan myproject --target example.com --profile 2

# Launch dashboard (web UI at http://localhost:8000)
python3 reconx.py dashboard

# System health check
python3 reconx.py doctor

# List projects
python3 reconx.py projects

# Recent scan jobs
python3 reconx.py status

# View reports for a project
python3 reconx.py report myproject

# Check tool availability
python3 reconx.py update
```

---

## Scan Profiles

| Profile  | CLI Flag   | Description                          | Est. Time     |
|----------|------------|--------------------------------------|---------------|
| Basic    | `--profile 1` | DNS + port scan + HTTP probe      | 5–15 min      |
| Medium   | `--profile 2` | Basic + LLM analysis              | 15–60 min     |
| Deep     | `--profile 3` | Full depth + all plugins          | 1–6+ hours    |

---

## Project Structure

```
ReconX/
├── reconx.py              # Main entry point
├── requirements.txt
├── config.yaml            # Global configuration
├── .env                   # API keys (gitignored)
│
├── core/                  # Engine layer
│   ├── orchestrator.py    # Top-level workflow runner
│   ├── workflow_engine.py # YAML workflow loader/executor
│   ├── execution_manager.py # Isolated subprocess execution
│   ├── plugin_loader.py   # Plugin auto-discovery
│   ├── correlation_engine.py # Asset deduplication + DB population
│   ├── result_store.py    # Persist results (filesystem + SQLite)
│   ├── project_manager.py # Project CRUD
│   ├── doctor.py          # Health checks
│   ├── database.py        # SQLAlchemy SQLite manager
│   ├── models.py          # Asset, Service, Vulnerability ORM models
│   ├── config.py          # YAML config manager
│   └── paths.py           # Central path constants
│
├── plugins/golden/        # Production-ready plugins
│   ├── dns_intelligence/  # DNS A/CNAME/MX resolution
│   ├── network_discovery/ # Async TCP port scanner
│   ├── web_recon/         # HTTP fingerprinting + tech detection
│   ├── llm_analysis/      # AI risk analysis (OpenAI + rule-based fallback)
│   └── reporting/         # MD, JSON, CSV, HTML report generation
│
├── events/
│   └── event_bus.py       # Async pub/sub event system
│
├── api/                   # REST API + WebSocket
│   ├── gateway/main.py    # FastAPI app + dashboard
│   └── routes/            # projects, workflows, findings, reports, tasks
│
├── workflows/             # YAML workflow definitions
│   ├── basic.yaml
│   ├── medium.yaml
│   └── deep.yaml
│
├── projects/              # Per-project data (auto-created)
├── outputs/               # Generated reports
└── scripts/
    └── install.sh
```

---

## Dashboard

```bash
python3 reconx.py dashboard
```

Opens at **http://localhost:8000** — full API documentation at `/docs`.

---

## API Keys (Optional)

Copy `.env.example` to `.env` and add your keys for enhanced capabilities:

```env
OPENAI_API_KEY=sk-...          # AI analysis (falls back to rule-based if absent)
SHODAN_API_KEY=...             # Shodan integration
VIRUSTOTAL_API_KEY=...         # VirusTotal lookups
```

---

## Writing a Custom Plugin

```python
# plugins/my_category/my_plugin/adapter.py
from core.plugin_interface import PluginInterface

class ToolAdapter(PluginInterface):
    async def execute(self, config: dict, context: dict) -> dict:
        target = context.get("target")
        # ... your logic ...
        return {
            "plugin": "my_plugin",
            "findings": [],
        }
```

Add to a workflow YAML:
```yaml
- id: s_custom
  plugin: my_plugin
  plugin_path: plugins/my_category/my_plugin
  timeout: 120
```

---

## Disclaimer

ReconX is for **authorized security testing and educational use only**.
Do not use against systems you do not own or have explicit written permission to test.
