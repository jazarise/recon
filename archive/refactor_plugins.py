import os
import re
from pathlib import Path

plugins_dir = Path("e:/ReconX/Reconx_V_2.0.0/plugins")

def refactor_plugin(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        changed = False

        # If it doesn't have ToolAdapter, ignore
        if "class ToolAdapter" not in content:
            return

        # 1. Add import if needed
        if "ReconXPlugin" not in content:
            content = "from core.plugin_manager.interface import ReconXPlugin\n" + content
            changed = True

        # 2. Change class inheritance
        if "class ToolAdapter:" in content:
            content = content.replace("class ToolAdapter:", "class ToolAdapter(ReconXPlugin):")
            changed = True
        elif "class ToolAdapter(" in content and "ReconXPlugin" not in content:
            # Replace whatever it inherits from with ReconXPlugin
            content = re.sub(r"class ToolAdapter\([^)]+\):", "class ToolAdapter(ReconXPlugin):", content)
            changed = True

        # 3. Rename run/scan/launch/start to execute
        methods_to_replace = ["def run(", "def scan(", "def launch(", "def start("]
        for m in methods_to_replace:
            if m in content:
                content = content.replace(m, "def execute(")
                changed = True

        if changed:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

count = 0
for root, _, files in os.walk(plugins_dir):
    for f in files:
        if f.endswith(".py"):
            refactor_plugin(Path(root) / f)
            count += 1

print(f"Refactored {count} plugins.")
