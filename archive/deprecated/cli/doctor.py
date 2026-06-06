import platform
from core.platform_adapter import PlatformAdapter

REQUIRED_BINARIES = [
    "python", "node", "npm", "git", "docker", "sqlite3", "ollama",
    "nmap", "nuclei", "subfinder"
]

def run_doctor():
    print("==================================================")
    print("RECONX DOCTOR - Dependency Validation")
    print("==================================================")
    print(f"OS: {platform.system()} {platform.release()} ({PlatformAdapter.detect_os()})")
    print("-" * 50)
    
    all_passed = True
    for binary in REQUIRED_BINARIES:
        if PlatformAdapter.dependency_check(binary):
            print(f"[✓] {binary.ljust(15)} : Installed")
        else:
            print(f"[✗] {binary.ljust(15)} : Missing")
            all_passed = False
            
    print("-" * 50)
    if all_passed:
        print("[+] All dependencies met. ReconX is ready.")
    else:
        print("[-] Missing dependencies detected. Please install them to ensure full functionality.")
        if PlatformAdapter.detect_os() == "linux":
            print("    Recommendation: run 'sudo apt install <package>' or check installation guide.")
        else:
            print("    Recommendation: Please install the missing binaries and add them to your PATH.")
