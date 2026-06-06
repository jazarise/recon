import os
import re
from pathlib import Path

base_dir = Path("e:/ReconX/Reconx_V_2.0.0/core")

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
            
            # Replace 'except:' with 'except Exception as e:'
            # Be careful about indentation, using a simple string replacement
            new_content = re.sub(r'(\s+)except:\s*\n', r'\1except Exception as e:\n\1    logger.error(f"Unexpected error: {e}", exc_info=True)\n', content)
            
            if new_content != content:
                # Make sure logger is imported if not already
                if "import logging" not in new_content and "core.logging.logger import setup_logger" not in new_content:
                    new_content = "from core.logging.logger import setup_logger\nlogger = setup_logger(__name__)\n\n" + new_content
                with open(path, "w", encoding="utf-8") as file:
                    file.write(new_content)
                print(f"Updated exceptions in {os.path.relpath(path, base_dir)}")
