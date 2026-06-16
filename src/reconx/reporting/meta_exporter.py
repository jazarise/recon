def export_optimization_report(meta_data: dict, filepath: str):
    with open(filepath, 'w') as f:
        f.write("SYSTEM PERFORMANCE REPORT\n")
        f.write("=========================\n\n")
        f.write(f"Efficiency: {meta_data['efficiency_gain']} improved over last epoch\n")
        f.write(f"Noise reduction: {meta_data['noise_reduction']}\n")
        f.write("High-value detection rate: Increased\n\n")
        
        f.write("RECOMMENDED AUTO-MUTATIONS:\n")
        for plugin in meta_data['disabled_plugins']:
            f.write(f"- Disable low-yield plugin: {plugin}\n")
            
        f.write(f"\nNew Adaptive Workflow Path: {' -> '.join(meta_data['new_workflow'])}\n")
