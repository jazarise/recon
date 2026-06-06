from core.http.client import HttpClient
import asyncio
import shutil
import json
from pathlib import Path



class Plugin:
    name = 'subdomains'
    category = 'recon'
    async def run(target: str, context: dict) -> dict -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        subfinder_path = shutil.which("subfinder")
        if not subfinder_path:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "Subfinder Missing", "description": "Subfinder not installed"}], "metadata": {}}

        out_file = BASE_DIR / f"outputs/{target}_recon88r_subs.json"
        
        # Subfinder execution to simulate Recon88r's passive subdomain phase
        cmd = [subfinder_path, "-d", target, "-all", "-oJ", "-o", str(out_file), "-silent"]
        
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
                            domain = data.get("host", "")
                            if domain:
                                assets.append({
                                    "type": "subdomain",
                                    "value": domain,
                                    "tags": ["recon88r", "subfinder"]
                                })
            return {"assets": assets, "findings": findings, "metadata": {"recon88r_module": "subdomains", "count": len(assets)}}
        except Exception as e:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "Recon88r Subdomain Error", "description": str(e)}], "metadata": {}}
