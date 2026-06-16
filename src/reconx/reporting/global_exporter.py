import json

def export_global_analytics(diffs: list, predictions: list, filepath: str):
    with open(filepath, 'w') as f:
        f.write("GLOBAL CONTINUOUS INTELLIGENCE REPORT\n")
        f.write("="*40 + "\n\n")
        
        f.write("RECENT ATTACK SURFACE CHANGES:\n")
        for diff in diffs:
            f.write(f"- [{diff['time']}] {diff['event']}\n")
            
        f.write("\nPREDICTIVE THREAT MODELING:\n")
        if not predictions:
            f.write("- No immediate predictive threats modeled.\n")
        for pred in predictions:
            f.write(f"- {pred}\n")
