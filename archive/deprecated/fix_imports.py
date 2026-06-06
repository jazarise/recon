import os
import re

base_dir = r"E:\ReconX\Reconx_V_2.0.0"

files_to_fix = [
    r"api\routes\knowledgebase.py",
    r"api\routes\reports.py",
    r"api\routes\tasks.py",
    r"api\routes\workflows.py",
    r"core\config.py",
    r"core\database.py",
    r"core\doctor.py",
    r"core\execution_manager.py",
    r"core\logger.py",
    r"core\plugin_loader.py",
    r"core\project_manager.py",
    r"core\result_store.py",
    r"reconx.py"
]

def replacer(match):
    indent = match.group(1)
    import_stmt = match.group(2)
    
    fallback = f\"\"\"{indent}# boilerplate removed\n\"\"\"
    return fallback

for filepath in files_to_fix:
    full_path = os.path.join(base_dir, filepath)
    if not os.path.exists(full_path):
        print(f"Skipping {filepath}, not found")
        continue
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace PROJECT_ROOT with BASE_DIR
    content = content.replace("PROJECT_ROOT", "BASE_DIR")
    # Replace OUTPUT_DIR with OUTPUTS_DIR
    # BUT only if it's not already OUTPUTS_DIR
    content = re.sub(r'\bOUTPUT_DIR\b', "OUTPUTS_DIR", content)
    content = re.sub(r'\bREPORT_DIR\b', "REPORTS_DIR", content)
    
    # Inject try-except for the `from core.paths import ...`
    new_content = re.sub(r"^([ \t]*)(from\s+core\.paths\s+import\s+.*)$", replacer, content, flags=re.MULTILINE)
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Fixed {filepath}")
