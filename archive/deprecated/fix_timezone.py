import os
import re
from pathlib import Path

base_dir = Path("e:/ReconX/Reconx_V_2.0.0")

for root, _, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".py") and "venv" not in root:
            file_path = Path(root) / f
            try:
                content = file_path.read_text(encoding="utf-8")
            except:
                continue
                
            if "timezone.utc" in content and "from datetime import timezone" not in content and "import timezone" not in content:
                new_content = re.sub(r'(from datetime import [^\n]+)', r'\1, timezone', content)
                if new_content == content:
                    new_content = "from datetime import timezone\n" + content
                file_path.write_text(new_content, encoding="utf-8")
                print(f"Fixed timezone import in {file_path}")
