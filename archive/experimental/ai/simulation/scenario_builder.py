from reconx.core.attack_paths.pathfinder import pathfinder
from reconx.core.mitre_mapping.mapper import mitre_mapper
from reconx.core.defense_analysis.validator import defense_validator
from typing import List

class ScenarioBuilder:
    """Orchestrates the Ethical Red Team Simulation Engine."""
    
    def execute_simulation(self, target: str, assets: List, relationships: List):
        print(f"\n[=========================================]")
        print(f"[RECONX STAGE 13] THREAT SIMULATION ENGINE")
        print(f"[=========================================]")
        print(f"[*] Target: {target}")
        
        # 1. Generate Theoretical Attack Paths
        print(f"[*] Generating Theoretical Attack Paths...")
        paths = pathfinder.generate_paths(assets, relationships)
        
        if not paths:
            print("[+] No viable attack paths found. Defense is solid.")
            return
            
        print(f"[!] Found {len(paths)} potential attack paths!")
        
        # 2. Map to MITRE and Validate Defense
        report = []
        for path in paths:
            entry = path["entry_node"]
            
            # Map MITRE
            mitre_data = mitre_mapper.map_asset_to_technique(entry.type, entry.value)
            
            # Validate Defense
            defense = defense_validator.evaluate_path(path)
            
            report.append({
                "path": path,
                "mitre": mitre_data,
                "defense": defense
            })
            
        self._print_executive_report(target, report)
        self._print_technical_report(report)
        
    def _print_executive_report(self, target: str, report: List[dict]):
        print(f"\n--- EXECUTIVE REPORT ---")
        criticals = len([r for r in report if r["path"]["severity"] == "CRITICAL"])
        highs = len([r for r in report if r["path"]["severity"] == "HIGH"])
        
        overall_risk = "CRITICAL" if criticals > 0 else ("HIGH" if highs > 0 else "MEDIUM")
        print(f"System Risk: {overall_risk}")
        print(f"Total Attack Vectors Identified: {len(report)}")
        
        print("Top Recommended Actions:")
        actions = set()
        for r in report:
            for mitigation in r["defense"]["recommended_mitigations"]:
                actions.add(mitigation)
        for act in actions:
            print(f"  - {act}")

    def _print_technical_report(self, report: List[dict]):
        print(f"\n--- TECHNICAL REPORT ---")
        for r in report:
            path = r["path"]
            entry = path["entry_node"]
            mitre = r["mitre"]
            defense = r["defense"]
            
            print(f"\n[PATH_ID: {path['path_id']}]")
            print(f"  Target Asset  : [{entry.type.value}] {entry.value}")
            print(f"  Vulnerability : {path['vulnerability']}")
            print(f"  Impact        : {path['impact']} (Severity: {path['severity']})")
            
            if mitre:
                print(f"  MITRE ATT&CK  : {mitre['id']} - {mitre['name']}")
                
            print(f"  Defense Status: {defense['defense_status']}")

scenario_builder = ScenarioBuilder()
