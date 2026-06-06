import os
import sys
import venv
import subprocess
from pathlib import Path

def setup_environment():
    print("[*] ReconX V2.0.0 Automated Installer")
    base_dir = Path(__file__).resolve().parent.parent
    venv_dir = base_dir / "venv"
    
    print("[*] Creating virtual environment...")
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(venv_dir)
    
    # Path to pip
    if os.name == 'nt':
        pip_exe = venv_dir / "Scripts" / "pip.exe"
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        pip_exe = venv_dir / "bin" / "pip"
        python_exe = venv_dir / "bin" / "python"
        
    print("[*] Installing dependencies...")
    reqs = base_dir / "requirements.txt"
    if reqs.exists():
        subprocess.check_call([str(pip_exe), "install", "-r", str(reqs)])
    else:
        print("[-] requirements.txt not found, skipping pip install.")
        
    print("[*] Installing optional dependencies...")
    subprocess.check_call([str(pip_exe), "install", "aiohttp", "uvicorn", "psutil"])
        
    # Generate Launchers
    print("[*] Generating CLI launchers...")
    installers_dir = base_dir / "installers"
    installers_dir.mkdir(exist_ok=True)
    
    # Windows Bat
    bat_path = installers_dir / "reconx.bat"
    with open(bat_path, "w") as f:
        f.write(f'@echo off\n"{python_exe}" "{base_dir / "reconx.py"}" %*\n')
        
    # Shell Script
    sh_path = installers_dir / "reconx"
    with open(sh_path, "w") as f:
        f.write(f'#!/usr/bin/env bash\n"{python_exe}" "{base_dir / "reconx.py"}" "$@"\n')
        
    if os.name != 'nt':
        os.chmod(sh_path, 0o755)
        
    print("[*] Registering CLI to PATH...")
    # For this simulation we will just echo instructions
    print(f"\n[+] SUCCESS! Add {installers_dir} to your system PATH to use the 'reconx' command globally.")
    
    print("[*] Running basic validation tests...")
    test_script = base_dir / "smoke_test.py"
    if test_script.exists():
        subprocess.check_call([str(python_exe), str(test_script)])
    else:
        print("[-] smoke_test.py not found, skipping validation.")

if __name__ == "__main__":
    setup_environment()
