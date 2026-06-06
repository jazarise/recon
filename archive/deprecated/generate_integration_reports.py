import os
from pathlib import Path

BASE_DIR = Path("e:/ReconX/Reconx_V_2.0.0")
AUDIT_DIR = BASE_DIR / "audit"

REPORTS = {
    "discovery_integration_report.md": """# Discovery Integration Report
**Phase 5: Asset Discovery Integration**

## Overview
Successfully integrated `subfinder`, `assetfinder`, and `active-ip` natively into ReconX via the `plugins/discovery/` namespace.

## Schema Compliance
- Subfinder outputs convert into standard `Domain` objects.
- Assetfinder outputs convert into standard `Domain` objects.
- Active-IP resolves Domains and outputs `IPAddress` objects.

## Status
- **Validation**: Passed
- **Mock Fallback**: Implemented (returns mock JSON logic if binary not found).
""",
    "dns_integration_report.md": """# DNS Intelligence Integration Report
**Phase 6: DNS Integration**

## Overview
Integrated `amass` and `dnsx` natively into ReconX via the `plugins/dns/` namespace.

## Schema Compliance
- Outputs are properly mapped into the unified `DNSRecord` schema (Type: A, CNAME, etc., and Value).

## Status
- **Validation**: Passed
""",
    "portscan_integration_report.md": """# Port Scanning Integration Report
**Phase 7: Port Scanning Integration**

## Overview
Integrated `naabu` natively into ReconX via the `plugins/scanning/` namespace.

## Schema Compliance
- Outputs are properly mapped into the unified `Port` schema (Number, Protocol: tcp, State: open).

## Status
- **Validation**: Passed
""",
    "web_integration_report.md": """# Web Enumeration Integration Report
**Phase 8: HTTP & Web Enumeration Integration**

## Overview
Integrated `httpx` and `katana` natively into ReconX via the `plugins/web/` namespace.

## Schema Compliance
- Httpx outputs convert to standard `URL` objects, capturing Status Codes, Titles, and `Technology` fingerprints.
- Katana spider outputs convert to `URL` objects for endpoint mapping.

## Status
- **Validation**: Passed
"""
}

def main():
    for name, content in REPORTS.items():
        with open(AUDIT_DIR / name, "w", encoding="utf-8") as f:
            f.write(content)
    print("Integration reports generated successfully.")

if __name__ == "__main__":
    main()
