import os
import re

base_dir = r"E:\ReconX\Reconx_V_2.0.0"

def replacer(match):
    indent = match.group(1)
    import_stmt = match.group(2)
    
    fallback = f\"\"\"{indent}# boilerplate removed\n\"\"\"
    return fallback

for root, _, files in os.walk(base_dir):
    if 'venv' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith('.py') and file != 'paths.py' and file != 'fix_imports.py':
            full_path = os.path.join(root, file)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                original_content = content
                
                # Replace BASE_DIR with BASE_DIR
                content = content.replace("BASE_DIR", "BASE_DIR")
                # Replace OUTPUTS_DIR with OUTPUTS_DIR
                content = re.sub(r'\bOUTPUT_DIR\b', "OUTPUTS_DIR", content)
                content = re.sub(r'\bREPORT_DIR\b', "REPORTS_DIR", content)
                
                # Inject try-except for the `from core.paths import ...`
                if "from core.paths import" in content and "except ImportError:" not in content:
                    content = re.sub(r"^([ \t]*)(from\s+core\.paths\s+import\s+.*)$", replacer, content, flags=re.MULTILINE)
                
                if content != original_content:
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Fixed {full_path}")
            except Exception as e:
                print(f"Error processing {full_path}: {e}")
