import os
from pathlib import Path
import re

base_dir = Path("e:/ReconX/Reconx_V_2.0.0")

for root, _, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".py") and "venv" not in root:
            file_path = Path(root) / f
            try:
                content = file_path.read_text(encoding="utf-8")
            except:
                continue
                
            if "utcnow" in content:
                # Replace datetime.now(timezone.utc) -> datetime.now(timezone.utc)
                new_content = re.sub(r'datetime\.utcnow\(\)', 'datetime.now(timezone.utc)', content)
                # Replace datetime.datetime.now(timezone.utc) -> datetime.datetime.now(timezone.utc)
                new_content = re.sub(r'datetime\.datetime\.utcnow\(\)', 'datetime.datetime.now(timezone.utc)', new_content)
                # Replace lambda: datetime.now(timezone.utc) -> datetime.now(timezone.utc) without parens (e.g. for default kwargs)
                new_content = re.sub(r'(?<!\.)datetime\.utcnow(?!\()', 'lambda: datetime.now(timezone.utc)', new_content)
                new_content = re.sub(r'datetime\.datetime\.utcnow(?!\()', 'lambda: datetime.datetime.now(timezone.utc)', new_content)
                
                if new_content != content:
                    if "timezone" not in new_content:
                        # try to find 'from datetime import' and append timezone
                        if "from datetime import " in new_content:
                            new_content = re.sub(r'(from datetime import [^\n]+)', r'\1, timezone', new_content)
                        else:
                            new_content = "from datetime import timezone\n" + new_content
                    file_path.write_text(new_content, encoding="utf-8")
                    print(f"Fixed {file_path}")
