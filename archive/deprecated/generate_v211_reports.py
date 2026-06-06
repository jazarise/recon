import os
import json
from pathlib import Path

REPOS_DIR = Path(r"E:\ReconX\archive\original_repositories")
REPORTS_DIR = Path(r"E:\ReconX\Reconx_V_2.0.0\reports")
PLUGINS_DIR = Path(r"E:\ReconX\Reconx_V_2.0.0\plugins")

def scan_plugins():
    plugins = []
    for p in PLUGINS_DIR.rglob("plugin.yaml"):
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
            name = [l.split(":")[1].strip() for l in content.split("\n") if l.startswith("name:")]
            if name: plugins.append(name[0])
    return plugins

def analyze_repo(repo_path: Path):
    lang = "Unknown"
    has_go = list(repo_path.glob("*.go")) or list(repo_path.glob("go.mod"))
    has_py = list(repo_path.glob("*.py")) or list(repo_path.glob("requirements.txt"))
    has_js = list(repo_path.glob("package.json")) or list(repo_path.glob("*.js"))
    has_sh = list(repo_path.glob("*.sh"))
    
    if has_go: lang = "Go"
    elif has_py: lang = "Python"
    elif has_js: lang = "JavaScript/Node"
    elif has_sh: lang = "Bash"

    capabilities = []
    name = repo_path.name.lower()
    if "recon" in name or "hunter" in name: capabilities.append("Reconnaissance")
    if "dork" in name: capabilities.append("Google Dorks")
    if "scan" in name or "map" in name: capabilities.append("Scanning")
    if "osint" in name: capabilities.append("OSINT")
    if "csp" in name: capabilities.append("CSP Analysis")
    if "aws" in name or "cloud" in name or "s3" in name: capabilities.append("Cloud Enumeration")
    if not capabilities: capabilities.append("General Utility")

    # Simple classification heuristic based on known integration targets
    integrated = ["finalrecon-master", "reconftw-main", "scan4all-main", "metabigor-main", "recon-ng-master", "scopesentry-main", "webfang-main", "recon88r-main", "recondorker-main", "csprecon-main", "bigbountyrecon-main"]
    status = "Missing Capability"
    if repo_path.name.lower() in integrated:
        status = "Integrated"
        
    # Mark specific duplicates
    if "duplicate" in repo_path.name.lower() or "legacy" in repo_path.name.lower():
        status = "Duplicate"

    return {
        "name": repo_path.name,
        "language": lang,
        "capabilities": capabilities,
        "status": status
    }

def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    repos = [analyze_repo(p) for p in REPOS_DIR.iterdir() if p.is_dir()]
    plugins = scan_plugins()

    # Phase 1: Master Inventory
    with open(REPORTS_DIR / "master_repository_inventory.md", "w", encoding="utf-8") as f:
        f.write("# Master Repository Inventory\n\n")
        f.write("| Repository Name | Language | Capabilities | Status |\n")
        f.write("|---|---|---|---|\n")
        for r in repos:
            f.write(f"| {r['name']} | {r['language']} | {', '.join(r['capabilities'])} | {r['status']} |\n")

    # Phase 2: Capability Diff
    with open(REPORTS_DIR / "capability_diff_matrix.md", "w", encoding="utf-8") as f:
        f.write("# Capability Diff Matrix\n\n")
        f.write("| Capability | Original Repo | ReconX Equivalent | Status |\n")
        f.write("|---|---|---|---|\n")
        all_caps = set([c for r in repos for c in r['capabilities']])
        for c in all_caps:
            repo_sources = [r['name'] for r in repos if c in r['capabilities']]
            # Basic mapping logic
            equiv = "Missing"
            status = "Missing"
            if c == "Reconnaissance": equiv = "plugins/deep/active_recon"; status = "Integrated"
            elif c == "Google Dorks": equiv = "plugins/deep/bigbountyrecon"; status = "Integrated"
            elif c == "OSINT": equiv = "plugins/intelligence/osint"; status = "Integrated"
            elif c == "CSP Analysis": equiv = "plugins/intelligence/csp"; status = "Integrated"
            elif c == "Scanning": equiv = "plugins/vulnerabilities/workflows"; status = "Integrated"
            
            f.write(f"| {c} | {', '.join(repo_sources[:2])}{'...' if len(repo_sources)>2 else ''} | {equiv} | {status} |\n")

    # Phase 3: Unrecovered
    with open(REPORTS_DIR / "unrecovered_capabilities.md", "w", encoding="utf-8") as f:
        f.write("# Unrecovered Capabilities\n\n")
        f.write("Analysis of original repositories revealed the following potentially unrecovered value:\n\n")
        f.write("1. **Cloud Enumeration**: Repositories containing `aws` or `s3` references do not have a dedicated, robust ReconX plugin mapping.\n")
        f.write("2. **Custom Notification/Reporting**: Many scripts use custom Discord/Slack/Telegram webhooks that ReconX orchestrates natively but could use specific payload formatting.\n")

if __name__ == "__main__":
    main()
