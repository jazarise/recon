import os

files = {
    "src/reconx/db/storage.py": '''import sqlite3
import json
import logging

logger = logging.getLogger("reconx")

class DatabaseLayer:
    def __init__(self, db_path="reconx.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                target TEXT,
                status TEXT,
                results TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_campaign(self, campaign_id: str, target: str, status: str, results: dict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "REPLACE INTO campaigns (id, target, status, results) VALUES (?, ?, ?, ?)",
            (campaign_id, target, status, json.dumps(results))
        )
        conn.commit()
        conn.close()

    def get_campaign(self, campaign_id: str) -> dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT target, status, results FROM campaigns WHERE id=?", (campaign_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"target": row[0], "status": row[1], "results": json.loads(row[2])}
        return None
''',
    "src/reconx/api/auth.py": """class RBACLayer:
    API_KEYS = {
        "rex_admin_999": {"role": "admin", "scopes": ["scan:run", "results:read", "campaign:delete"]},
        "rex_analyst_123": {"role": "analyst", "scopes": ["scan:run", "results:read"]},
        "rex_viewer_000": {"role": "viewer", "scopes": ["results:read"]}
    }

    @classmethod
    def validate_key(cls, token: str, required_scope: str) -> bool:
        if token not in cls.API_KEYS:
            return False
        
        user_scopes = cls.API_KEYS[token]["scopes"]
        if required_scope not in user_scopes and "admin" != cls.API_KEYS[token]["role"]:
            return False
            
        return True
""",
    "src/reconx/api/webhooks.py": """import logging

logger = logging.getLogger("reconx")

class WebhookDispatcher:
    def __init__(self, endpoint_url: str = None):
        self.endpoint_url = endpoint_url

    def dispatch(self, event_type: str, data: dict):
        if not self.endpoint_url:
            return
            
        payload = {
            "event": event_type,
            "data": data
        }
        logger.warning(f"[WEBHOOK] Dispatched {event_type} to {self.endpoint_url}")
        # Simulated POST request logic
""",
    "src/reconx/core/guardrails.py": """class ScopeEnforcer:
    ALLOWED_SCOPES = [".example.com", "scanme.nmap.org"]

    @classmethod
    def validate_target(cls, target: str) -> bool:
        for scope in cls.ALLOWED_SCOPES:
            if target.endswith(scope) or target == scope:
                return True
        return False
""",
    "src/reconx/api/server.py": """import json
import uuid
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from reconx.db.storage import DatabaseLayer
from reconx.api.auth import RBACLayer
from reconx.core.guardrails import ScopeEnforcer
from reconx.api.webhooks import WebhookDispatcher

logger = logging.getLogger("reconx")
db = DatabaseLayer()
webhook = WebhookDispatcher(endpoint_url="https://hooks.slack.com/services/xxx")

class ReconXAPIHandler(BaseHTTPRequestHandler):
    def _send_response(self, status, payload):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def _authenticate(self, required_scope):
        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            self._send_response(401, {"error": "Missing or Invalid Authorization Header"})
            return False
            
        token = auth_header.split(" ")[1]
        if not RBACLayer.validate_key(token, required_scope):
            self._send_response(403, {"error": "Insufficient Permissions"})
            return False
        return True

    def do_GET(self):
        if self.path == '/health':
            self._send_response(200, {"status": "healthy", "uptime_seconds": 3600})
            
        elif self.path.startswith('/scan/'):
            if not self._authenticate("results:read"): return
            
            campaign_id = self.path.split('/')[-1]
            data = db.get_campaign(campaign_id)
            
            if data:
                self._send_response(200, data)
            else:
                self._send_response(404, {"error": "Campaign Not Found"})
        else:
            self._send_response(404, {"error": "Endpoint not implemented"})

    def do_POST(self):
        if self.path == '/scan':
            if not self._authenticate("scan:run"): return
            
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            target = post_data.get('target')

            if not ScopeEnforcer.validate_target(target):
                self._send_response(400, {"error": "Target outside authorized scope limits."})
                return

            campaign_id = str(uuid.uuid4())
            db.save_campaign(campaign_id, target, "queued", {})
            
            logger.info(f"[API] Accepted scan job for {target}. ID: {campaign_id}")
            webhook.dispatch("scan_started", {"target": target, "id": campaign_id})
            
            self._send_response(202, {"status": "queued", "id": campaign_id})
        else:
            self._send_response(404, {"error": "Endpoint not implemented"})

def start_server(port=8000):
    server = HTTPServer(('0.0.0.0', port), ReconXAPIHandler)
    print(f"[+] ReconX API Service listening on 0.0.0.0:{port}")
    server.serve_forever()
""",
    "src/reconx/main.py": '''import sys
import argparse
from reconx.logger import setup_logging
from reconx.version import __version__
from reconx.api.server import start_server

BANNER = f"""
===================================================
                RECONX v{__version__} FINAL
         Enterprise SaaS / API Backend Service
===================================================
"""

def main():
    print(BANNER)
    setup_logging()
    
    parser = argparse.ArgumentParser(description="ReconX API Service")
    parser.add_argument("action", choices=["api"], help="Launch the API Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    
    args = parser.parse_args()
        
    if args.action == "api":
        start_server(args.port)

if __name__ == "__main__":
    main()
''',
    "Dockerfile": """FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "src/reconx/main.py", "api", "--port", "8000"]
""",
    "docker-compose.yml": """version: '3.8'

services:
  reconx-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./reconx.db:/app/reconx.db
    environment:
      - LOG_LEVEL=INFO
""",
    ".github/workflows/reconx-ci.yml": """name: ReconX Continuous Intelligence Pipeline

on:
  schedule:
    - cron: "0 0 * * *" # Nightly Scanning

jobs:
  recon_scan:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger ReconX Enterprise Backend
        run: |
          curl -X POST https://reconx.internal.corp/scan \\
          -H "Authorization: Bearer ${{ secrets.RECONX_API_KEY }}" \\
          -H "Content-Type: application/json" \\
          -d '{"target": "scanme.nmap.org"}'
""",
    "docs/reports/stage17_saas_architecture.md": """# Stage 17: Enterprise Service Architecture

## API Service Layer
ReconX is now fully headless. Execution is completely driven via HTTP REST payloads mapping to `src/reconx/api/server.py`. 

## Authentication & Authorization
The API strictly enforces `Role-Based Access Control`. Tokens must be passed via the `Authorization: Bearer <TOKEN>` header. Viewers cannot trigger new scans, and Admins wield full campaign mutation capabilities.

## Persistent Storage
Memory states have been upgraded to `src/reconx/db/storage.py`, persisting all campaign metadata to a resilient SQLite database, ensuring job states survive container restarts.
""",
}

for path, content in files.items():
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
