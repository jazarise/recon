from reconx.core.plugin_base import standardize_output
import asyncio
import shutil
import json



class Plugin:
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [], "metadata": {}}

        nuclei_path = shutil.which("nuclei")
        if not nuclei_path:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "Nuclei Missing", "description": "Nuclei not installed"}], "metadata": {}}

        out_file = BASE_DIR / f"outputs/{target}_fingerprint.json"
        
        # Use nuclei's technology tag for fingerprinting (simulating scan4all's logic)
        cmd = [nuclei_path, "-u", target, "-tags", "tech", "-json-export", str(out_file), "-silent"]
        
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
                            tech_name = data.get("info", {}).get("name", "")
                            if tech_name:
                                assets.append({
                                    "type": "technology",
                                    "value": tech_name,
                                    "tags": ["scan4all", "fingerprinting", data.get("template-id", "")]
                                })
            return {"assets": assets, "findings": findings, "metadata": {"scan4all_module": "fingerprinting"}}
        except Exception as e:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "Fingerprint Error", "description": str(e)}], "metadata": {}}

# Auto-injected Metadata
PLUGIN_NAME = "fingerprinting"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for fingerprinting"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = ["nuclei"]
