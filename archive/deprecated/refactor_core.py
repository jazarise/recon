import os
import shutil
import re
from pathlib import Path

base_dir = Path("e:/ReconX/Reconx_V_2.0.0")
core_dir = base_dir / "core"

dirs_to_create = ["engine", "plugin_manager", "workflow_engine", "config", "logging", "dependency_manager"]
for d in dirs_to_create:
    (core_dir / d).mkdir(exist_ok=True)

moves = {
    "orchestrator.py": "engine/orchestrator.py",
    "execution_manager.py": "engine/execution_manager.py",
    "correlation_engine.py": "engine/correlation_engine.py",
    "plugin_loader.py": "plugin_manager/loader.py",
    "plugin_interface.py": "plugin_manager/interface.py",
    "workflow_engine.py": "workflow_engine/engine.py",
    "config.py": "config/manager.py",
    "logger.py": "logging/logger.py",
    "doctor.py": "dependency_manager/doctor.py"
}

for src, dst in moves.items():
    src_path = core_dir / src
    dst_path = core_dir / dst
    if src_path.exists():
        shutil.move(str(src_path), str(dst_path))

for d in dirs_to_create:
    (core_dir / d / "__init__.py").touch(exist_ok=True)

import_replacements = {
    r'from core\.orchestrator import': r'from core.engine.orchestrator import',
    r'import core\.orchestrator': r'import core.engine.orchestrator',
    r'from core\.execution_manager import': r'from core.engine.execution_manager import',
    r'import core\.execution_manager': r'import core.engine.execution_manager',
    r'from core\.correlation_engine import': r'from core.engine.correlation_engine import',
    r'import core\.correlation_engine': r'import core.engine.correlation_engine',
    r'from core\.plugin_loader import': r'from core.plugin_manager.loader import',
    r'import core\.plugin_loader': r'import core.plugin_manager.loader',
    r'from core\.plugin_interface import': r'from core.plugin_manager.interface import',
    r'import core\.plugin_interface': r'import core.plugin_manager.interface',
    r'from core\.workflow_engine import': r'from core.workflow_engine.engine import',
    r'import core\.workflow_engine': r'import core.workflow_engine.engine.engine',
    r'from core\.config import': r'from core.config.manager import',
    r'import core\.config': r'import core.config.manager.manager',
    r'from core\.logger import': r'from core.logging.logger import',
    r'import core\.logger': r'import core.logging.logger',
    r'from core\.doctor import': r'from core.dependency_manager.doctor import',
    r'import core\.doctor': r'import core.dependency_manager.doctor',
}

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
            
            new_content = content
            for pattern, repl in import_replacements.items():
                new_content = re.sub(pattern, repl, new_content)
                
            if new_content != content:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(new_content)
                print(f"Updated imports in {os.path.relpath(path, base_dir)}")
