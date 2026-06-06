import os
import re
from pathlib import Path

TARGET_VARS = ['BASE_DIR', 'OUTPUTS_DIR', 'RESULTS_DIR', 'LOGS_DIR', 'WORKFLOWS_DIR', 'PLUGINS_DIR', 'REPORTS_DIR', 'CONFIG_DIR']

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The block looks like:
    # try:
    #     try: ...
    #     except ImportError: ...
    #     CONFIG_DIR = BASE_DIR / "config"
    # except ImportError:
    #     ...
    #     CONFIG_DIR = BASE_DIR / "config"
    
    # Let's find all instances of BASE_DIR = Path(__file__).resolve().parent
    # and remove the entire enclosing try/except block.
    
    # A robust regex for the block:
    # Matches 'try:\n' followed by anything up to 'CONFIG_DIR = BASE_DIR / "config"\n'
    # with possible nesting.
    # Actually, we can use a simpler approach.
    
    pattern1 = re.compile(r'try:\s*\n\s*from core\.paths import.*?\n\s*except ImportError:\s*\n\s*from pathlib import Path\s*\n\s*BASE_DIR = Path\(__file__\)\.resolve\(\)\.parent.*?CONFIG_DIR = BASE_DIR / "config"\n', re.DOTALL)
    pattern2 = re.compile(r'try:\s*\n\s*try:\s*\n\s*from core\.paths import.*?\n\s*except ImportError:\s*\n\s*from pathlib import Path\s*\n\s*BASE_DIR = Path\(__file__\)\.resolve\(\)\.parent.*?CONFIG_DIR = BASE_DIR / "config"\n\s*except ImportError:\s*\n\s*from pathlib import Path\s*\n\s*BASE_DIR = Path\(__file__\)\.resolve\(\)\.parent.*?CONFIG_DIR = BASE_DIR / "config"\n', re.DOTALL)
    
    pattern3 = re.compile(r'try:\s*\n\s*from core\.paths import BASE_DIR.*?\n\s*except ImportError:\s*\n\s*from pathlib import Path\s*\n\s*BASE_DIR = Path\(__file__\)\.resolve\(\)\.parent.*?CONFIG_DIR = BASE_DIR / "config"\n', re.DOTALL)

    # Some are just the except block (like in reconx.py inline)
    pattern4 = re.compile(r'try:\s*\n\s*from core\.paths import BASE_DIR\s*\n\s*except ImportError:\s*\n\s*from pathlib import Path\s*\n\s*BASE_DIR = Path\(__file__\)\.resolve\(\)\.parent.*?CONFIG_DIR = BASE_DIR / "config"\n', re.DOTALL)

    pattern_generic = re.compile(r'^[ \t]*try:\n[ \t]*try:\n.*?CONFIG_DIR = BASE_DIR / "config"\n[ \t]*except ImportError:\n.*?CONFIG_DIR = BASE_DIR / "config"\n', re.MULTILINE | re.DOTALL)
    
    pattern_generic2 = re.compile(r'^[ \t]*try:\n[ \t]*from core\.paths import.*?\n[ \t]*except ImportError:\n[ \t]*from pathlib import Path\n[ \t]*BASE_DIR = Path\(__file__\).*?CONFIG_DIR = BASE_DIR / "config"\n', re.MULTILINE | re.DOTALL)

    original_content = content

    content = pattern_generic.sub('', content)
    content = pattern_generic2.sub('', content)

    if content != original_content:
        # Determine used variables
        used_vars = []
        for var in TARGET_VARS:
            # check if var is used outside of import statements
            # simple string match is usually enough if we just check var in content
            if var in content:
                used_vars.append(var)
        
        if used_vars:
            import_stmt = f"from core.paths import {', '.join(used_vars)}\n"
            # Add import at the top (after docstring if any)
            # Find the best place to insert it.
            # If it was inline (like in reconx.py), we need to put it at the top of the file.
            # Let's just put it near the top, after imports.
            # Actually, the prompt says "Replace the entire try/except block and replace it with a single clean import... Replace all of them with the single import above at the top of reconx.py."
            pass

    # Better logic:
    # 1. Strip all try/except path boilerplate blocks.
    # 2. Collect used TARGET_VARS.
    # 3. Add `from core.paths import ...` at the top of the file if used.

def remove_boilerplate(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Regex to match the try/except boilerplate:
    # We look for "BASE_DIR = Path(__file__).resolve().parent" and "CONFIG_DIR = BASE_DIR / \"config\""
    # and find the enclosing try...except.

    # Remove nested one first (e.g. plugin_loader)
    content = re.sub(r'^[ \t]*try:\n[ \t]*try:\n[ \t]*from core\.paths import.*?\n[ \t]*except ImportError:\n.*?CONFIG_DIR = BASE_DIR / "config"\n\n[ \t]*except ImportError:\n.*?CONFIG_DIR = BASE_DIR / "config"\n', '', content, flags=re.MULTILINE | re.DOTALL)

    # Remove standard one
    content = re.sub(r'^[ \t]*try:\n[ \t]*from core\.paths import.*?\n[ \t]*except ImportError:\n.*?CONFIG_DIR = BASE_DIR / "config"\n', '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Remove one in reconx.py where the import is just "from core.paths import BASE_DIR"
    content = re.sub(r'^[ \t]*try:\n[ \t]*from core\.paths import BASE_DIR\n[ \t]*except ImportError:\n.*?CONFIG_DIR = BASE_DIR / "config"\n', '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Remove one in reconx.py where the import is "from core.paths import WORKFLOWS_DIR"
    content = re.sub(r'^[ \t]*try:\n[ \t]*from core\.paths import WORKFLOWS_DIR\n[ \t]*except ImportError:\n.*?CONFIG_DIR = BASE_DIR / "config"\n', '', content, flags=re.MULTILINE | re.DOTALL)

    if content == original_content:
        return False # No changes

    # Determine used variables
    used_vars = []
    for var in TARGET_VARS:
        # Check if used. \bVAR\b
        if re.search(r'\b' + var + r'\b', content):
            used_vars.append(var)

    if used_vars:
        import_stmt = f"from core.paths import {', '.join(used_vars)}\n"
        
        # Insert import at the top of the file
        # Find first non-comment, non-docstring line.
        # Actually, just inserting it after the docstring or at line 1.
        lines = content.split('\n')
        insert_idx = 0
        in_docstring = False
        for i, line in enumerate(lines):
            if line.startswith('"""') or line.startswith("'''"):
                if not in_docstring:
                    in_docstring = True
                    if line.count('"""') == 2 or line.count("'''") == 2:
                        in_docstring = False # single line docstring
                else:
                    in_docstring = False
                    insert_idx = i + 1
                    break
            elif not in_docstring and not line.startswith('#') and line.strip():
                insert_idx = i
                break
        
        if insert_idx == 0 and lines[0].startswith('"""'):
            pass # already handled by loop if docstring is proper
        elif insert_idx == 0 and lines[0].startswith('#!'):
            insert_idx = 1
            
        lines.insert(insert_idx, import_stmt)
        content = '\n'.join(lines)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")
    return True

base = Path("e:/ReconX/Reconx_V_2.0.0")
for p in base.rglob("*.py"):
    if "core/paths.py" in str(p).replace("\\", "/"):
        continue
    remove_boilerplate(p)
