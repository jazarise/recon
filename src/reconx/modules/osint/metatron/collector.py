import subprocess
from reconx.core.models import Finding
from typing import List

class MetatronCollector:
    def __init__(self):
        self.tools = {
            "nmap": ["nmap", "-sV", "-sC", "-T4", "--open"],
            "whois": ["whois"],
            "whatweb": ["whatweb", "-a", "3"],
            "curl_http": ["curl", "-sI", "--max-time", "10", "--location"],
            "curl_https": ["curl", "-sI", "--max-time", "10", "--location", "-k"],
            "dig_A": ["dig", "+short", "A"],
            "dig_MX": ["dig", "+short", "MX"],
            "dig_NS": ["dig", "+short", "NS"],
            "dig_TXT": ["dig", "+short", "TXT"]
        }

    def _run_tool(self, name: str, command: List[str], target: str) -> str:
        cmd = command.copy()
        if name == "curl_http":
            cmd.append(f"http://{target}")
        elif name == "curl_https":
            cmd.append(f"https://{target}")
        else:
            cmd.append(target)
            
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            out = result.stdout.strip()
            err = result.stderr.strip()
            if out: return out
            if err: return err
            return "[!] No output"
        except FileNotFoundError:
            return f"[!] Tool not found: {cmd[0]}"
        except Exception as e:
            return f"[!] Error running {cmd[0]}: {e}"

    def collect(self, target: str, **kwargs) -> list:
        findings = []
        for name, cmd in self.tools.items():
            output = self._run_tool(name, cmd, target)
            finding = Finding(
                category="metatron_recon",
                source="metatron",
                value=output,
                metadata={"tool": name}
            )
            findings.append(finding)
        return findings
