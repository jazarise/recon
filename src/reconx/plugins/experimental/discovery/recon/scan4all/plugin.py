from reconx.core.plugin_base import standardize_output
from reconx.core.http.client import HttpClient
import asyncio
import os
import shutil



class Plugin:
    name = 'scan4all'
    category = 'recon'
    async def run_nuclei(self, target: str) -> list:
        # Replaces scan4all's nuclei embedding with native subprocess logic
        nuclei_path = shutil.which("nuclei")
        if not nuclei_path:
            return [{"error": "Nuclei not installed"}]
            
        out_file = BASE_DIR / f"outputs/{target}_nuclei.json"
        
        cmd = [
            nuclei_path,
            "-u", target,
            "-json-export", str(out_file),
            "-silent"
        ]
        
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()
            
            if out_file.exists():
                import json
                findings = []
                with open(out_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            findings.append(json.loads(line))
                return findings
        except Exception as e:
            return [{"error": str(e)}]
        return []

    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        results = await self.run_nuclei(target)
        
        assets = []
        findings = []
        metadata = {}

        if results and "error" in results[0]:
            findings.append({"type": "error", "severity": "info", "title": "Scan4All Error", "description": results[0]["error"]})
        else:
            for r in results:
                findings.append({
                    "type": "vulnerability",
                    "severity": r.get("info", {}).get("severity", "info"),
                    "title": r.get("info", {}).get("name", "Unknown Vuln"),
                    "description": r.get("info", {}).get("description", ""),
                    "tags": ["scan4all", "nuclei", r.get("template-id", "")]
                })
            metadata["scan4all_results"] = len(results)

        return {
            "assets": assets,
            "findings": findings,
            "metadata": metadata
        }

# Auto-injected Metadata
PLUGIN_NAME = "scan4all"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for scan4all"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = ["nuclei"]
