from reconx.core.plugin_base import standardize_output
import os
import json
import asyncio
import shutil



class Plugin:
    name = 'nuclei'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to nuclei plugin")

        nuclei_path = shutil.which("nuclei")
        if not nuclei_path:
            raise FileNotFoundError("nuclei binary not found in PATH")

        project_dir = OUTPUTS_DIR / "projects" / target
        input_file = project_dir / "alive_urls.txt"
        
        # If no alive urls from httpx, fallback to subdomains or target
        if not input_file.exists():
            input_file = project_dir / "subdomains.txt"
        if not input_file.exists():
            input_file = project_dir / "target.txt"
            with open(input_file, "w") as f:
                f.write(f"{target}\n")

        out_file = project_dir / "nuclei.json"

        # Execute nuclei: -l input_file -json-export out_file -silent
        cmd = [
            nuclei_path,
            "-l", str(input_file),
            "-json-export", str(out_file),
            "-silent"
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0 and process.returncode is not None:
            # Nuclei might exit non-zero if findings are found, so we check if outfile exists
            if not out_file.exists() or os.path.getsize(out_file) == 0:
                raise RuntimeError(f"Nuclei failed: {stderr.decode()}")

        findings = []

        if out_file.exists():
            with open(out_file, "r") as f:
                for line in f:
                    if not line.strip(): continue
                    try:
                        data = json.loads(line)
                        if isinstance(data, list):
                            items = data
                        elif isinstance(data, dict):
                            items = [data]
                        else:
                            continue
                            
                        for item in items:
                            if not isinstance(item, dict): 
                                continue
                            info = item.get("info", {})
                            findings.append({
                                "type": "vulnerability",
                                "name": info.get("name", item.get("name")),
                                "severity": info.get("severity", item.get("severity")),
                                "host": item.get("host", item.get("target")),
                                "matched_at": item.get("matched-at", item.get("matched_at")),
                                "template_id": item.get("template-id", item.get("template_id"))
                            })
                    except Exception as e:
                        import logging
                        logging.getLogger("nuclei_adapter").error(f"Error parsing nuclei output: {e}")
                        continue

        return {
            "plugin": "nuclei",
            "target": target,
            "vulnerabilities_found": len(findings),
            "findings": findings
        }

# Auto-injected Metadata
PLUGIN_NAME = "nuclei"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for nuclei"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = ["nuclei"]
