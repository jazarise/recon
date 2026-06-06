import sys

def check_python_packages():
    packages = ["requests", "rich", "fastapi", "uvicorn", "sqlalchemy", "yaml", "pydantic", "aiohttp", "jinja2"]
    all_passed = True
    print("Python Dependencies:")
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"[PASS] {pkg}")
        except ImportError:
            print(f"[FAIL] {pkg}")
            all_passed = False
    return all_passed

def check_external_tools():
    import shutil
    tools = ["subfinder", "nuclei", "httpx", "nmap"]
    print("\\nExternal Tools:")
    for tool in tools:
        if shutil.which(tool):
            print(f"[PASS] {tool}")
        else:
            print(f"[WARN] {tool} (Missing but optional)")
    return True

def main():
    print("ReconX Environment Doctor\\n")
    print(f"[PASS] Python version: {sys.version.split()[0]}")
    pkg_ok = check_python_packages()
    check_external_tools()
    
    if not pkg_ok:
        print("\n[!] Environment unhealthy. Please run ./install.sh")
        sys.exit(1)
    else:
        print("\n[+] Environment healthy.")

if __name__ == "__main__":
    main()
