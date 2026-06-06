# ReconX Changelog

## v1.0.0 — Final Release

### Core Fixes
- **PluginLoader** — Fixed two-level directory traversal so `plugins/golden/*` plugins
  are discovered automatically alongside flat `plugins/*/` layouts
- **CorrelationEngine** — Fixed `AttributeError: 'list' object has no attribute 'items'`
  crash; updated to match actual golden plugin output schema
- **API Gateway** — Wired all six REST route modules (projects, workflows, findings,
  reports, tasks, agents) and the WebSocket event stream; added dashboard SPA
- **WebSocket stream** — Replaced broken implementation with clean
  broadcast-to-all-connections pattern with connection lifecycle management

### New Modules
- **`core/project_manager.py`** — Full project CRUD: create, list, get, update,
  delete; per-project directory tree with metadata JSON and dedicated SQLite DB
- **`core/doctor.py`** — 27+ health checks across Python version, packages,
  external tools, directory structure, workflows, plugins, config, and DB write
- **`reconx.py`** (complete rewrite) — Full interactive TUI menu matching the
  Master Product Spec; all sub-commands: `scan`, `dashboard`, `doctor`,
  `projects`, `status`, `report`, `update`; `--profile`, `--target`, `--project` flags

### Plugins
- **`llm_analysis`** (rewritten) — OpenAI-powered analysis when `OPENAI_API_KEY`
  is set; zero-dependency rule-based fallback with port/tech/DNS risk scoring
  when API key is absent — scans never fail due to missing AI credentials
- **`reporting`** (rewritten) — Generates four formats per scan: Markdown, JSON,
  CSV, dark-themed HTML; complete stat cards, risk badges, recommendations table

### API Routes (new)
- `GET/POST /api/v1/projects/` — list and create projects
- `GET /api/v1/projects/{name}` — project detail
- `DELETE /api/v1/projects/{name}` — delete project
- `POST /api/v1/workflows/run` — trigger workflow
- `GET /api/v1/workflows/` — list available workflows
- `GET /api/v1/findings/` — query assets from project DB
- `GET /api/v1/reports/` — list generated reports
- `GET /api/v1/tasks/` — list recent job results
- `GET /api/v1/agents/` — list registered plugins
- `GET /api/v1/doctor` — JSON health check
- `WS  /ws/events` — live workflow event stream

### Testing
- **`smoke_test.py`** (rewritten) — 7-section, 27-assertion suite covering core
  imports, plugin loading, doctor, project manager, workflow YAML parsing,
  end-to-end workflow execution, and report generation

### Files Added / Updated
```
reconx.py                              rewritten — full interactive CLI
core/plugin_loader.py                  fixed — nested plugin discovery
core/correlation_engine.py             fixed — output schema alignment
core/project_manager.py                new
core/doctor.py                         new
plugins/golden/llm_analysis/adapter.py rewritten — OpenAI + rule-based
plugins/golden/reporting/adapter.py    rewritten — 4-format output
api/gateway/main.py                    rewritten — full FastAPI app
api/websocket/stream.py                fixed — broadcast pattern
api/routes/projects.py                 new
api/routes/workflows.py                new
api/routes/findings.py                 new
api/routes/reports.py                  new
api/routes/tasks.py                    new
api/routes/agents.py                   new
smoke_test.py                          rewritten — 27 assertions
requirements.txt                       updated
README.md                              complete
scripts/install.sh                     new
.env.example                           new
CHANGELOG.md                           new
```
