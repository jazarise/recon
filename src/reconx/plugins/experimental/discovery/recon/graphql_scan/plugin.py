from reconx.core.plugin_base import standardize_output
from reconx.core.http.client import HttpClient
import os
import json
import urllib.request
import urllib.error
import ssl
from pathlib import Path



class Plugin:
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to graphql_scan")

        project_dir = OUTPUTS_DIR / "projects" / target
        input_file = project_dir / "alive_urls.txt"
        
        findings = []
        urls_to_check = set()
        
        if input_file.exists():
            with open(input_file, "r") as f:
                for line in f:
                    if line.strip(): urls_to_check.add(line.strip())
        else:
            urls_to_check.add(f"https://{target}")

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        payload = b'{"query":"query IntrospectionQuery { __schema { queryType { name } } }"}'
        
        for base_url in list(urls_to_check)[:20]:
            graphql_url = base_url.rstrip("/") + "/graphql"
            try:
                req = urllib.request.Request(graphql_url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5, context=ctx) as response:
                    resp_data = response.read().decode()
                    if "__schema" in resp_data or "queryType" in resp_data:
                        findings.append({
                            "type": "vulnerability",
                            "name": "GraphQL Introspection Enabled",
                            "severity": "info",
                            "url": graphql_url,
                            "proof": "Introspection query succeeded"
                        })
            except Exception:
                pass

        return {
            "plugin": "graphql_scan",
            "target": target,
            "findings": findings
        }

# Auto-injected Metadata
PLUGIN_NAME = "graphql_scan"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for graphql_scan"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = []
