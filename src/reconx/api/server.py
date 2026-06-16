import json
import uuid
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from src.reconx.db.storage import DatabaseLayer
from src.reconx.api.auth import RBACLayer
from src.reconx.core.guardrails import ScopeEnforcer
from src.reconx.api.webhooks import WebhookDispatcher

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
