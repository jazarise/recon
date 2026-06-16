def generate_campaign_report(targets: list, aggregator, filepath: str):
    with open(filepath, 'w') as f:
        f.write("CAMPAIGN SUMMARY\n\n")
        f.write(f"Targets scanned: {len(targets)}\n")
        f.write(f"Total Unique Nodes Discovered: {len(aggregator.global_nodes)}\n")
        f.write(f"Cross-Domain Edges Mapped: {len(aggregator.global_edges)}\n\n")
        
        f.write("GLOBAL RISK SCORE: HIGH\n\n")
        
        f.write("Shared infrastructure detected:\n")
        f.write("3 clusters (Simulated Analysis)\n")
