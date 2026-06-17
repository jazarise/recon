
def export_intelligence_report(report_data: dict, filepath: str):
    """Outputs the structured AI reasoning report."""
    with open(filepath, 'w') as f:
        f.write(f"TARGET: {report_data['target']}\n\n")
        
        f.write("ATTACK SURFACE SUMMARY:\n")
        f.write(f"- High-risk endpoints: {len(report_data['attack_surface']['high_risk'])}\n")
        f.write(f"- Medium-risk endpoints: {len(report_data['attack_surface']['medium_risk'])}\n")
        f.write(f"- Low-risk noise (Ignored): {len(report_data['attack_surface']['low_risk'])}\n\n")
        
        f.write("PRIORITY TARGETS:\n")
        for idx, t in enumerate(report_data['attack_surface']['high_risk']):
            f.write(f"{idx+1}. {t} (HIGH)\n")
            
        f.write("\nRECOMMENDED NEXT ACTIONS:\n")
        for action in report_data['recommendations']:
            f.write(f"- {action}\n")
