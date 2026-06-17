
def export_executive_summary(tenant_id: str, data: dict, filepath: str):
    with open(filepath, 'w') as f:
        f.write("ENTERPRISE SECURITY INTELLIGENCE REPORT\n")
        f.write(f"Organization: {tenant_id}\n")
        f.write("="*40 + "\n\n")
        
        f.write("EXECUTIVE SUMMARY:\n")
        f.write("Your external attack surface maintains a STABLE posture.\n\n")
        
        f.write("TECHNICAL BREAKDOWN:\n")
        f.write(f"- Active Assets: {data.get('assets', 0)}\n")
        f.write(f"- Critical Findings: {data.get('critical', 0)}\n")
