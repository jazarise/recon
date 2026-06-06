from core.http.client import HttpClient
import asyncio
import json
from pathlib import Path
from datetime import datetime, timezone, timezone


class Plugin:
    name = 'whois'
    category = 'recon'
    async def get_whois(self, domain: str, server: str) -> dict:
        whois_result = {}
        try:
            reader, writer = await asyncio.open_connection(server, 43)
            writer.write((domain + "\r\n").encode())
            
            raw_resp = b""
            while True:
                chunk = await reader.read(4096)
                if not chunk:
                    break
                raw_resp += chunk
                
            writer.close()
            await writer.wait_closed()
            raw_result = raw_resp.decode(errors='ignore')
            
            if "No match for" in raw_result:
                return None
                
            res_parts = raw_result.split(">>>", 1)
            whois_result["whois"] = res_parts[0]
            return whois_result
        except Exception as e:
            return {"error": str(e)}

    def parse_whois(self, raw: str) -> dict:
        parsed = {}
        for line in raw.splitlines():
            line = line.strip()
            if ":" not in line:
                continue
            key, _, val = line.partition(":")
            key, val = key.strip(), val.strip()
            if not key or not val:
                continue
            parsed[key] = val
        return parsed

    async def run(target: str, context: dict) -> dict -> dict:
        target = context.get("target", "")
        if not target:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "No target", "description": "No target specified for WHOIS"}], "metadata": {}}

        # Parse tld
        parts = target.split('.')
        if len(parts) < 2:
            return {"assets": [], "findings": [], "metadata": {}}
        tld = parts[-1]

        db_path = Path(__file__).parent / "whois_servers.json"
        if not db_path.exists():
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "Missing DB", "description": "whois_servers.json not found"}], "metadata": {}}

        try:
            with open(db_path, "r", encoding='utf-8') as db_file:
                db_json = json.load(db_file)
        except Exception as e:
            return {"assets": [], "findings": [{"type": "error", "severity": "info", "title": "DB Load Error", "description": str(e)}], "metadata": {}}

        whois_sv = db_json.get(tld)
        if not whois_sv:
            return {"assets": [], "findings": [{"type": "unsupported_tld", "severity": "info", "title": "Unsupported TLD", "description": f"TLD {tld} not supported by local whois"}], "metadata": {}}

        whois_info = await self.get_whois(target, whois_sv)
        
        assets = []
        findings = []
        metadata = {"whois_server": whois_sv}

        if not whois_info:
            findings.append({"type": "whois_no_match", "severity": "info", "title": "No WHOIS match", "description": f"No WHOIS data for {target}"})
        elif "error" in whois_info:
            findings.append({"type": "whois_error", "severity": "info", "title": "WHOIS connection error", "description": whois_info["error"]})
        else:
            raw_text = whois_info["whois"]
            parsed_data = self.parse_whois(raw_text)
            metadata["parsed_whois"] = parsed_data
            metadata["raw_whois"] = raw_text

            # Create an asset for the registrar if available
            registrar = parsed_data.get("Registrar")
            if registrar:
                assets.append({
                    "type": "registrar",
                    "value": registrar,
                    "tags": ["whois", "infrastructure"]
                })
            
            # Create a finding if domain expires soon
            expiry = parsed_data.get("Registry Expiry Date")
            if expiry:
                try:
                    exp_date = datetime.fromisoformat(expiry.replace("Z", "+00:00"))
                    days = (exp_date - datetime.now(timezone.utc)).days
                    if days < 30:
                        findings.append({
                            "type": "domain_expiring",
                            "severity": "medium",
                            "title": "Domain expiring soon",
                            "description": f"Target domain expires in {days} days on {expiry}"
                        })
                except:
                    pass

        return {
            "assets": assets,
            "findings": findings,
            "metadata": metadata
        }
