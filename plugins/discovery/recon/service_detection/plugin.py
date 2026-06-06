from core.http.client import HttpClient
import asyncio
import shutil
import json
from pathlib import Path



class Plugin:
    async def run(target: str, context: dict) -> dict -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        nuclei_path = shutil.which("nuclei")
        if not nuclei_path:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "Nuclei Missing", "description": "Nuclei not installed"}], "metadata": {}}

        out_file = BASE_DIR / f"outputs/{target}_services.json"
        
        # Use nuclei's network templates for service detection (simulating scan4all's logic)
        cmd = [nuclei_path, "-u", target, "-t", "network", "-json-export", str(out_file), "-silent"]
        
        try:
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await proc.communicate()
            
            assets = []
            findings = []
            if out_file.exists():
                with open(out_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            service_name = data.get("info", {}).get("name", "")
                            if service_name:
                                assets.append({
                                    "type": "service",
                                    "value": service_name,
                                    "tags": ["scan4all", "service_detection", data.get("template-id", "")]
                                })
            return {"assets": assets, "findings": findings, "metadata": {"scan4all_module": "service_detection"}}
        except Exception as e:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "Service Detection Error", "description": str(e)}], "metadata": {}}
