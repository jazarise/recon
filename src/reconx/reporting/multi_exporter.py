import json
import csv

def export_json(data: dict, filepath: str):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def export_csv(data: dict, filepath: str):
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Target", "Subdomains", "IPs", "Ports", "Tech"])
        writer.writerow([
            data.get("target"),
            ",".join(data.get("subdomains", [])),
            ",".join(data.get("ips", [])),
            ",".join(map(str, data.get("ports", []))),
            ",".join(data.get("tech_stack", []))
        ])

def export_markdown(data: dict, filepath: str):
    with open(filepath, 'w') as f:
        f.write(f"# Recon Report: {data.get('target')}\n")
        f.write(f"**Ports Open:** {data.get('ports')}\n")
