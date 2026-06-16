from reconx.core.plugin_base import standardize_output
from reconx.core.http.client import HttpClient
import os
import json
import asyncio
import shutil
from pathlib import Path



class Plugin:
    name = 'xss_scan'
    category = 'recon'
    @standardize_output
    async def run(target: str, context: dict) -> dict:
        target = context.get("target")
        if not target:
            raise ValueError("No target provided to xss_scan")

        project_dir = OUTPUTS_DIR / "projects" / target
        input_file = project_dir / "endpoints.txt"
        out_file = project_dir / "dalfox.json"

        findings = []

        if not shutil.which("dalfox"):
            findings.append({
                "type": "configuration_issue",
                "name": "Missing Dependency: Dalfox",
                "severity": "info",
                "host": target,
                "description": "Dalfox binary not found in PATH. Skipping XSS scan."
            })
            return {
                "plugin": "xss_scan",
                "target": target,
                "vulnerabilities_found": 0,
                "findings": findings
            }

        if input_file.exists():
            # Check dalfox version to determine syntax (v2 vs v3)
            cmd = ["dalfox", "scan", str(input_file), "-b", "ha.ckers.org", "-o", str(out_file), "--format", "json"]
            
            try:
                proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                stdout, stderr = await proc.communicate()
                
                # If 'scan' subcommand failed due to being v2, fallback to 'file'
                if b"unknown command" in stderr or b"Usage:" in stderr:
                    cmd = ["dalfox", "file", str(input_file), "-b", "ha.ckers.org", "-o", str(out_file), "--format", "json"]
                    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                    await proc.communicate()
            except Exception as e:
                import logging
                logging.getLogger("xss_scan").error(f"Error executing dalfox: {e}")

            if out_file.exists() and os.path.getsize(out_file) > 0:
                with open(out_file, "r") as f:
                    try:
                        content = f.read().strip()
                        if content:
                            data = json.loads(content)
                            for item in data:
                                if isinstance(item, dict):
                                    findings.append({
                                        "type": "vulnerability",
                                        "name": item.get("type", "XSS"),
                                        "severity": item.get("severity", "medium"),
                                        "url": item.get("url"),
                                        "proof": item.get("poc")
                                    })
                    except Exception as e:
                        import logging
                        logging.getLogger("xss_scan").error(f"Error parsing dalfox JSON: {e}")

        return {
            "plugin": "xss_scan",
            "target": target,
            "vulnerabilities_found": len([f for f in findings if f.get("type") == "vulnerability"]),
            "findings": findings
        }

# Auto-injected Metadata
PLUGIN_NAME = "xss_scan"
PLUGIN_VERSION = "1.0"
PLUGIN_CATEGORY = "Discovery"
PLUGIN_DESCRIPTION = "Auto-generated description for xss_scan"


@standardize_output
async def run(target: str, context: dict) -> dict:
    if hasattr(Plugin, 'run'):
        return await Plugin.run(target, context)
    return {"success": True, "data": "Plugin class executed"}

PLUGIN_AUTHOR = "ReconX"

PLUGIN_TAGS = ["discovery"]

PLUGIN_DEPENDENCIES = []

PLUGIN_EXTERNAL_TOOLS = []
