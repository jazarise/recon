from core.http.client import HttpClient
import asyncio
import shutil
import json
from pathlib import Path



class Plugin:
    name = 'workflows'
    category = 'vulnerabilities'
    async def run(target: str, context: dict) -> dict -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        nuclei_path = shutil.which("nuclei")
        if not nuclei_path:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "Nuclei Missing", "description": "Nuclei not installed"}], "metadata": {}}

        out_file = BASE_DIR / f"outputs/{target}_workflows.json"
        
        # Use nuclei's workflows (simulating scan4all's logic)
        cmd = [nuclei_path, "-u", target, "-w", "workflows/", "-json-export", str(out_file), "-silent"]
        
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
                            findings.append({
                                "type": "vulnerability",
                                "severity": data.get("info", {}).get("severity", "info"),
                                "title": data.get("info", {}).get("name", "Unknown Vuln"),
                                "description": data.get("info", {}).get("description", ""),
                                "tags": ["scan4all", "workflow", data.get("template-id", "")]
                            })
            return {"assets": assets, "findings": findings, "metadata": {"scan4all_module": "workflows"}}
        except Exception as e:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "Workflows Error", "description": str(e)}], "metadata": {}}
