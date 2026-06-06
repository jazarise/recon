import os
from pathlib import Path
import re

base_dir = Path("e:/ReconX/Reconx_V_2.0.0")

for root, _, files in os.walk(base_dir):
    if "venv" in root or ".git" in root or "__pycache__" in root:
        continue
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
            except Exception:
                continue
            
            new_content = re.sub(r'\bPluginLoader\b', 'PluginManager', content)
            
            if new_content != content:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(new_content)
                print(f"Replaced PluginManager in {os.path.relpath(path, base_dir)}")
