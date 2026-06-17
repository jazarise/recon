from reconx.core.opsec import RiskScore

class Plugin:
    name = "port_scan"
    risk = RiskScore.HIGH

    async def run(self, target: str, mode: str = "normal"):
        if mode == "stealth":
            # Native plugin-level suppression fallback
            return {"ports": [], "_opsec": "Suppressed due to stealth mode"}
        
        # Simulated Port scan
        return {"ports": [80, 443]}
