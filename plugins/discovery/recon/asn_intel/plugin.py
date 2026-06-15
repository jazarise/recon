from core.plugin_base import standardize_output
from core.http.client import HttpClient
import os
import json
import socket
import asyncio
import urllib.request
import shutil
from pathlib import Path



class Plugin:
    name = 'asn_intel'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to asn_intel")

        project_dir = OUTPUTS_DIR / "projects" / target
        project_dir.mkdir(parents=True, exist_ok=True)
        out_file = project_dir / "asn_intel.json"
        
        findings = []
        ip = None
        
        # 1. Resolve IP
        try:
            ip = socket.gethostbyname(target)
            findings.append({"type": "ip", "ip": ip, "domain": target})
        except Exception as e:
            import logging
            logging.getLogger("asn_intel").warning(f"Could not resolve target IP: {e}")

        # 2. Try Metabigor if available
        if ip and shutil.which("metabigor"):
            try:
                cmd = ["metabigor", "net", "--org", target]
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, _ = await proc.communicate()
                for line in stdout.decode().splitlines():
                    if line.strip():
                        findings.append({"type": "cidr", "cidr": line.strip()})
            except Exception as e:
                import logging
                logging.getLogger("asn_intel").error(f"Error running metabigor: {e}")

        # 3. Fallback to free IP-API for ASN info
        if ip:
            try:
                # Basic public API, no key required
                req = urllib.request.Request(f"http://ip-api.com/json/{ip}", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    if data.get("status") == "success":
                        asn = data.get("as", "").split(" ")[0] # e.g. "AS15169 Google LLC" -> "AS15169"
                        org = data.get("org")
                        if asn:
                            findings.append({"type": "asn", "asn": asn, "org": org, "ip": ip})
            except Exception as e:
                import logging
                logging.getLogger("asn_intel").error(f"Error calling IP-API: {e}")

        with open(out_file, "w") as f:
            json.dump(findings, f)

        return {
            "plugin": "asn_intel",
            "target": target,
            "findings": findings
        }

# Auto-injected Metadata
PLUGIN_NAME = "asn_intel"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for asn_intel"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = []
