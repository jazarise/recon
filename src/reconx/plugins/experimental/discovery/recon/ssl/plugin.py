from reconx.core.plugin_base import standardize_output
from datetime import timezone
from reconx.core.http.client import HttpClient
import ssl
import socket
import datetime


class Plugin:
    def get_ssl_info(self, hostname: str) -> dict:
        context = ssl.create_default_context()
        try:
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    return cert
        except Exception as e:
            return {"error": str(e)}

    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        # Remove http/https scheme if present
        if target.startswith("http"):
            target = target.split("//")[1].split("/")[0]

        cert_data = self.get_ssl_info(target)
        
        assets = []
        findings = []
        
        if "error" in cert_data:
            findings.append({"type": "error", "severity": "info", "title": "SSL Error", "description": cert_data["error"]})
        else:
            # Extract issuer and subject
            issuer = dict(x[0] for x in cert_data.get("issuer", []))
            subject = dict(x[0] for x in cert_data.get("subject", []))
            
            assets.append({
                "type": "technology",
                "value": f"SSL: {issuer.get('organizationName', 'Unknown')}",
                "tags": ["ssl", "issuer"]
            })
            
            # Check expiration
            not_after = cert_data.get("notAfter")
            if not_after:
                try:
                    exp_date = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                    days_left = (exp_date - datetime.datetime.now(timezone.utc)).days
                    if days_left < 30:
                        findings.append({
                            "type": "ssl_expiring",
                            "severity": "medium",
                            "title": "SSL Certificate Expiring Soon",
                            "description": f"The SSL certificate for {target} expires in {days_left} days."
                        })
                except:
                    pass

        return {
            "assets": assets,
            "findings": findings,
            "metadata": {"cert": cert_data}
        }

# Auto-injected Metadata
PLUGIN_NAME = "ssl"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for ssl"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = []
