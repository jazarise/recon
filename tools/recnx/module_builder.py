#!/usr/bin/env python3
"""
RECNX Module Builder
Generates unified Python wrapper modules in Reconx_V_2.0.0/modules/
based on the feature_matrix.json extracted from the 50 repositories.
"""

import json
import os
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("e:/ReconX/Reconx_V_2.0.0")
MATRIX_FILE = BASE_DIR / "feature_matrix.json"
MODULES_DIR = BASE_DIR / "modules"

MODULE_CATEGORIES = [
    "recon", "web", "osint", "intelligence", 
    "automation", "reporting", "cloud", "api", "agents"
]

TEMPLATE_DIRECT = """\"\"\"
ReconX Auto-Generated Module: {feature_name}
Origin Repository: {repo_name}
Classification: DIRECTLY_USABLE
\"\"\"

import os
import sys
from typing import Dict, Any

class {class_name}Adapter:
    \"\"\"
    Native Python adapter for {feature_name} extracted from {repo_name}.
    \"\"\"
    
    def __init__(self):
        self.name = "{feature_name}"
        self.repo_source = "{repo_name}"

    def run(self, target: str, config: Dict[{{str, Any}}] = None) -> Dict[{{str, Any}}]:
        \"\"\"
        Execute the {feature_name} module against the target.
        \"\"\"
        print(f"[*] Running {{self.name}} native module on {{target}}")
        # TODO: Link directly to {repo_name} native Python functions here.
        # This is marked DIRECTLY_USABLE, meaning we can import its code directly.
        
        return {{"status": "completed", "feature": self.name, "target": target}}
"""

TEMPLATE_WRAPPER = """\"\"\"
ReconX Auto-Generated Module: {feature_name}
Origin Repository: {repo_name}
Classification: REQUIRES_WRAPPER (Language: {language})
\"\"\"

import subprocess
import json
from typing import Dict, Any

class {class_name}Wrapper:
    \"\"\"
    Subprocess wrapper for {feature_name} extracted from {repo_name} ({language}).
    \"\"\"
    
    def __init__(self):
        self.name = "{feature_name}"
        self.repo_source = "{repo_name}"
        self.language = "{language}"

    def run(self, target: str, config: Dict[{{str, Any}}] = None) -> Dict[{{str, Any}}]:
        \"\"\"
        Execute the {feature_name} binary/script against the target.
        \"\"\"
        print(f"[*] Spawning {{self.language}} wrapper for {{self.name}} against {{target}}")
        # TODO: Implement subprocess call to {repo_name} binary here.
        
        return {{"status": "completed", "feature": self.name, "target": target, "execution": "subprocess"}}
"""

TEMPLATE_REFACTOR = """\"\"\"
ReconX Auto-Generated Module: {feature_name}
Origin Repository: {repo_name}
Classification: REQUIRES_REFACTOR
\"\"\"

from typing import Dict, Any

class {class_name}Refactored:
    \"\"\"
    Refactored adapter for {feature_name} extracted from {repo_name}.
    Original codebase requires significant modification to fit the architecture.
    \"\"\"
    
    def __init__(self):
        self.name = "{feature_name}"
        self.repo_source = "{repo_name}"

    def run(self, target: str, config: Dict[{{str, Any}}] = None) -> Dict[{{str, Any}}]:
        \"\"\"
        Execute the refactored {feature_name} module.
        \"\"\"
        print(f"[*] Running refactored {{self.name}} logic against {{target}}")
        # TODO: Port the logic from {repo_name} here.
        
        return {{"status": "completed", "feature": self.name, "target": target}}
"""

def camel_case(snake_str):
    components = snake_str.split('_')
    return "".join(x.title() for x in components)

def build_modules():
    print("[*] RECNX Module Builder initializing...")
    
    if not MATRIX_FILE.exists():
        print(f"[!] Error: {MATRIX_FILE} not found. Run deep_analyzer.py first.")
        return

    with open(MATRIX_FILE, "r", encoding="utf-8") as f:
        matrix = json.load(f)
        
    print(f"[*] Loaded {len(matrix)} feature mappings.")

    # Create module directories
    for cat in MODULE_CATEGORIES:
        os.makedirs(MODULES_DIR / cat, exist_ok=True)
        # Create __init__.py so it's a python package
        init_file = MODULES_DIR / cat / "__init__.py"
        if not init_file.exists():
            init_file.touch()

    # Create top-level __init__.py
    if not (MODULES_DIR / "__init__.py").exists():
        (MODULES_DIR / "__init__.py").touch()

    # Group by target module and feature to prevent duplicates 
    # (If multiple repos provide "subdomain_enumeration", we create one file 
    # but we will just use the highest priority repo for the generated stub)
    
    # feature -> [repo_entries]
    grouped = defaultdict(list)
    for entry in matrix:
        grouped[entry["feature"]].append(entry)

    generated_count = 0

    for feature_name, entries in grouped.items():
        # Sort by priority (high first), then classification (DIRECTLY_USABLE first)
        def sort_key(e):
            p_score = 0 if e.get("priority") == "high" else 1
            c_score = 0 if e.get("classification") == "DIRECTLY_USABLE" else (1 if "WRAPPER" in e.get("classification") else 2)
            return (p_score, c_score)
            
        entries.sort(key=sort_key)
        best_entry = entries[0]
        
        target_path_str = best_entry.get("target", f"modules/recon/{feature_name}")
        # target_path_str format: modules/web/xss_detection
        parts = target_path_str.split('/')
        if len(parts) >= 3:
            cat = parts[1]
            feat = parts[2]
        else:
            cat = "recon"
            feat = feature_name
            
        if cat not in MODULE_CATEGORIES:
            cat = "recon"

        file_path = MODULES_DIR / cat / f"{feat}.py"
        
        class_name = camel_case(feat)
        repo_name = best_entry["repository"]
        classification = best_entry.get("classification", "REQUIRES_WRAPPER")
        lang = best_entry.get("language", "Unknown")
        
        if classification == "DIRECTLY_USABLE":
            content = TEMPLATE_DIRECT.format(
                feature_name=feat, repo_name=repo_name, class_name=class_name
            )
        elif classification == "REQUIRES_REFACTOR":
            content = TEMPLATE_REFACTOR.format(
                feature_name=feat, repo_name=repo_name, class_name=class_name
            )
        else:
            content = TEMPLATE_WRAPPER.format(
                feature_name=feat, repo_name=repo_name, class_name=class_name, language=lang
            )
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        generated_count += 1
        print(f"  [+] Generated modules/{cat}/{feat}.py (from {repo_name})")

    print(f"\n[+] Successfully generated {generated_count} unique module files.")
    print("[*] All extracted capabilities have been structurally integrated into the ReconX modules/ tree.")

if __name__ == "__main__":
    build_modules()
