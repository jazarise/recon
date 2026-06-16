import json
import os

def generate_report(target: str, data: dict):
    """Exports structured intelligence to report.json and report.txt."""
    os.makedirs('reports', exist_ok=True)
    
    # JSON Export
    with open(f'reports/{target}_report.json', 'w') as f:
        json.dump(data, f, indent=4)
        
    # TXT Export
    with open(f'reports/{target}_report.txt', 'w') as f:
        f.write(f"Target: {target}\n")
        f.write(f"Subdomains: {len(data.get('subdomains', []))}\n")
        f.write(f"Live hosts: {len(data.get('live_hosts', []))}\n")
        f.write(f"Open services: {len(data.get('services', []))}\n")
        f.write(f"Risk indicators: {', '.join(data.get('risks', []))}\n")
