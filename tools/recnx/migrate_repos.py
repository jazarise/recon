import os
import json
from pathlib import Path

def setup_repo_modules():
    workspace = Path("e:/ReconX")
    repos_dir = workspace / "Repos"
    modules_dir = workspace / "Reconx_V_2.0.0" / "modules"
    modules_dir.mkdir(parents=True, exist_ok=True)
    
    # Load catalog
    catalog_file = workspace / "repository_catalog.json"
    if not catalog_file.exists():
        print("[-] repository_catalog.json not found!")
        return
        
    with open(catalog_file, "r") as f:
        catalog = json.load(f)
        
    # Standard Module Wrapper Template
    wrapper_template = '''"""
ReconX V2.0.0 Module Wrapper
Repository: {repo_name}
Language: {lang}
"""

import subprocess
from core.engine.execution_manager import ExecutionManager

class {class_name}Module:
    def __init__(self, execution_manager: ExecutionManager = None):
        self.exec_mgr = execution_manager
        self.repo_path = "Repos/{repo_name}"
        
    def execute(self, target: str, **kwargs):
        # TODO: Implement parameter mapping for {repo_name}
        print(f"[*] Executing {repo_name} module on {{target}}")
        return {{"status": "success", "module": "{repo_name}"}}
'''
    
    print("[*] Building module wrappers for repositories...")
    created = 0
    for repo in catalog:
        if repo["Classification"] != "ARCHIVE_ONLY":
            repo_name = repo["Repository Name"]
            lang = repo["Language"]
            
            # Module category mappings (simplified)
            mod_category = "recon"
            if "sec" in repo_name.lower(): mod_category = "web"
            if "ai" in repo_name.lower() or "llm" in repo_name.lower(): mod_category = "ai"
            
            cat_dir = modules_dir / mod_category
            cat_dir.mkdir(exist_ok=True)
            
            # Create wrapper file
            clean_name = repo_name.replace("-", "_").replace(".", "_")
            class_name = "".join(word.title() for word in clean_name.split("_"))
            
            wrapper_file = cat_dir / f"{clean_name.lower()}_wrapper.py"
            with open(wrapper_file, "w") as f:
                f.write(wrapper_template.format(
                    repo_name=repo_name,
                    lang=lang,
                    class_name=class_name
                ))
            
            # Ensure __init__.py exists
            init_file = cat_dir / "__init__.py"
            if not init_file.exists():
                init_file.touch()
                
            created += 1

    # Main __init__.py
    (modules_dir / "__init__.py").touch()
    
    print(f"[+] Created {created} module wrappers in {modules_dir}")

if __name__ == "__main__":
    setup_repo_modules()
