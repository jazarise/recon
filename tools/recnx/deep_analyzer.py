#!/usr/bin/env python3
"""
RECNX Deep Repository Intelligence Analyzer
Reads source code, READMEs, and configs from all 50 repositories
to extract actual features and capabilities.
"""
import os
import json
import re
from pathlib import Path
from collections import defaultdict

REPOS_DIR = Path("e:/ReconX/Repos")
OUTPUTS_DIR = Path("e:/ReconX/Reconx_V_2.0.0")

# Known capability keywords to search for in source and docs
CAPABILITY_PATTERNS = {
    "subdomain_enumeration": [r"subdomain", r"sublist3r", r"subfinder", r"amass", r"crt\.sh", r"virustotal.*domain"],
    "port_scanning": [r"port.?scan", r"nmap", r"naabu", r"masscan", r"socket.*connect"],
    "web_crawling": [r"crawl", r"spider", r"katana", r"hakrawler", r"scrapy"],
    "xss_detection": [r"xss", r"cross.?site.?script", r"reflected", r"stored.?xss", r"dom.?xss"],
    "sqli_detection": [r"sql.?inject", r"sqli", r"blind.?sql", r"union.?select"],
    "directory_bruteforce": [r"dir.?brut", r"gobuster", r"ffuf", r"dirsearch", r"content.?discovery"],
    "dns_enumeration": [r"dns.?enum", r"dnsx", r"dig\b", r"dns.?record", r"zone.?transfer"],
    "http_probing": [r"httpx", r"http.?prob", r"alive.?check", r"status.?code"],
    "url_collection": [r"wayback", r"gau\b", r"url.?collect", r"url.?gather", r"archive\.org"],
    "javascript_analysis": [r"js.?scan", r"js.?hunt", r"js.?enum", r"javascript.*secret", r"endpoint.*extract"],
    "technology_detection": [r"wappalyzer", r"whatweb", r"tech.?detect", r"fingerprint", r"cms.?detect"],
    "screenshot_capture": [r"screenshot", r"gowitness", r"aquatone", r"headless.*chrome"],
    "vulnerability_scanning": [r"nuclei", r"vuln.?scan", r"cve", r"exploit", r"vulnerability"],
    "api_testing": [r"api.?test", r"graphql", r"swagger", r"openapi", r"rest.?api.*test"],
    "osint_collection": [r"osint", r"shodan", r"censys", r"recon.?ng", r"passive.?recon"],
    "reporting": [r"report.?gen", r"markdown.*report", r"html.*report", r"pdf.*report", r"output.*format"],
    "workflow_automation": [r"workflow", r"automat", r"pipeline", r"chain", r"orchestrat"],
    "parameter_fuzzing": [r"fuzz", r"param.?fuzz", r"prototype.?pollut", r"parameter.*inject"],
    "secret_detection": [r"secret", r"api.?key", r"token.*leak", r"credential", r"password.*detect"],
    "cors_testing": [r"cors", r"cross.?origin", r"origin.*reflect"],
    "crlf_injection": [r"crlf", r"header.?inject", r"\\r\\n"],
    "csp_analysis": [r"csp", r"content.?security.?policy", r"csp.?bypass"],
    "dorking": [r"dork", r"google.*dork", r"search.*engine", r"bing.*dork"],
    "asset_discovery": [r"asset.?find", r"asset.?discover", r"acquisition", r"recon.*target"],
    "ip_analysis": [r"ip.?range", r"cidr", r"active.?ip", r"ip.*resolv", r"reverse.?dns"],
    "cloud_security": [r"s3.?bucket", r"cloud.*scan", r"aws", r"azure", r"gcp.*enum"],
    "breach_detection": [r"breach", r"leak", r"haveibeenpwned", r"dehashed", r"credential.*dump"],
    "header_analysis": [r"header.*analy", r"security.*header", r"hsts", r"x-frame"],
    "whois_lookup": [r"whois", r"domain.*registr", r"registrar"],
    "ssl_analysis": [r"ssl", r"tls", r"certificate", r"cert.*analy"],
    "agent_framework": [r"agent", r"llm.*agent", r"ai.*agent", r"autonomous", r"multi.?agent"],
    "burp_extension": [r"burp", r"extension", r"passive.*scan", r"active.*scan.*burp"],
}

MODULE_MAPPING = {
    "subdomain_enumeration": "recon",
    "port_scanning": "recon",
    "web_crawling": "web",
    "xss_detection": "web",
    "sqli_detection": "web",
    "directory_bruteforce": "web",
    "dns_enumeration": "recon",
    "http_probing": "recon",
    "url_collection": "recon",
    "javascript_analysis": "web",
    "technology_detection": "recon",
    "screenshot_capture": "recon",
    "vulnerability_scanning": "web",
    "api_testing": "api",
    "osint_collection": "osint",
    "reporting": "reporting",
    "workflow_automation": "automation",
    "parameter_fuzzing": "web",
    "secret_detection": "intelligence",
    "cors_testing": "web",
    "crlf_injection": "web",
    "csp_analysis": "web",
    "dorking": "osint",
    "asset_discovery": "recon",
    "ip_analysis": "recon",
    "cloud_security": "cloud",
    "breach_detection": "intelligence",
    "header_analysis": "web",
    "whois_lookup": "recon",
    "ssl_analysis": "recon",
    "agent_framework": "agents",
    "burp_extension": "web",
}


def read_file_safe(path, max_bytes=50000):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(max_bytes)
    except Exception:
        return ""


def detect_language(repo_path):
    exts = defaultdict(int)
    for root, _, files in os.walk(repo_path):
        if ".git" in root or "node_modules" in root or "vendor" in root:
            continue
        for f in files:
            ext = Path(f).suffix.lower()
            if ext:
                exts[ext] += 1
    
    lang_map = {
        ".py": "Python", ".go": "Go", ".js": "JavaScript", ".ts": "TypeScript",
        ".sh": "Shell", ".rb": "Ruby", ".rs": "Rust", ".java": "Java",
        ".jsx": "JavaScript", ".tsx": "TypeScript",
    }
    
    scored = {}
    for ext, count in exts.items():
        if ext in lang_map:
            scored[lang_map[ext]] = scored.get(lang_map[ext], 0) + count
    
    if not scored:
        return "Unknown"
    return max(scored, key=scored.get)


def find_entrypoints(repo_path):
    entries = []
    for pattern in ["main.py", "app.py", "cli.py", "run.py", "main.go", "cmd/main.go",
                     "*.sh", "setup.py", "Makefile", "Dockerfile"]:
        for match in repo_path.glob(pattern):
            entries.append(str(match.relative_to(repo_path)))
    # Also check for __main__.py
    for match in repo_path.rglob("__main__.py"):
        entries.append(str(match.relative_to(repo_path)))
    return entries[:10]


def find_dependencies(repo_path):
    deps = []
    for dep_file in ["requirements.txt", "go.mod", "package.json", "Cargo.toml", "Gemfile", "setup.py", "pyproject.toml"]:
        p = repo_path / dep_file
        if p.exists():
            content = read_file_safe(p, 5000)
            deps.append({"file": dep_file, "content_preview": content[:500]})
    return deps


def extract_features(repo_path):
    """Scan all source files and README for capability patterns."""
    all_text = ""
    
    # Read README
    for readme in ["README.md", "readme.md", "README.rst", "README.txt", "README"]:
        rp = repo_path / readme
        if rp.exists():
            all_text += read_file_safe(rp) + "\n"
    
    # Read source files (limited scan)
    file_count = 0
    for root, _, files in os.walk(repo_path):
        if ".git" in root or "node_modules" in root or "vendor" in root:
            continue
        for f in files:
            if f.endswith((".py", ".go", ".sh", ".js", ".ts", ".rb", ".rs")):
                all_text += read_file_safe(Path(root) / f, 10000) + "\n"
                file_count += 1
                if file_count > 50:
                    break
        if file_count > 50:
            break
    
    all_lower = all_text.lower()
    
    detected = {}
    for feature, patterns in CAPABILITY_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, all_lower):
                detected[feature] = True
                break
    
    return list(detected.keys()), all_text[:2000]  # Return features + preview


def classify_repo(features, language):
    if not features:
        return "ARCHIVE_ONLY"
    if language == "Python":
        return "DIRECTLY_USABLE"
    if language in ("Go", "Rust"):
        return "REQUIRES_WRAPPER"
    if language == "Shell":
        return "REQUIRES_WRAPPER"
    if language in ("JavaScript", "TypeScript"):
        return "REQUIRES_WRAPPER"
    return "REQUIRES_REFACTOR"


def determine_purpose(name, features, readme_preview):
    """Determine a short purpose from features and readme."""
    name_lower = name.lower()
    
    purposes = {
        "reconftw": "Automated reconnaissance framework orchestrating multiple tools",
        "recon-ng": "Full-featured web reconnaissance framework with module system",
        "dalfox": "Advanced XSS scanning and parameter analysis tool",
        "finalrecon": "All-in-one OSINT and web reconnaissance tool",
        "gxss": "Reflected parameter and XSS candidate discovery",
        "jshunter": "JavaScript file analysis for secrets and endpoints",
        "bug-bounty-agents": "AI-powered autonomous bug bounty agent workflows",
        "red-team-osint": "Red team OSINT collection and correlation toolkit",
        "acquifinder": "Acquisition and asset discovery tool",
        "bigbountyrecon": "Large-scale bug bounty reconnaissance automation",
        "cyberdeck": "Cybersecurity toolkit and dashboard",
        "dirx": "Directory brute-forcing and content discovery",
        "garud": "Automated reconnaissance pipeline",
        "ghostrecon": "Stealth reconnaissance and information gathering",
        "infeagle-recon": "Information gathering and reconnaissance",
        "jsfsscan": "JavaScript file scanning for security issues",
        "metatron": "Metadata extraction and analysis",
        "mottahunter": "Bug bounty hunting automation",
        "probe": "HTTP probing and alive host detection",
        "recon88r": "Reconnaissance automation toolkit",
        "recondorker": "Google dorking automation",
        "reconky": "Automated bash-based reconnaissance",
        "recomation": "Reconnaissance automation workflow",
        "scopesentry": "Bug bounty scope monitoring",
        "webfang": "Web application fingerprinting and analysis",
        "web-recon-automation": "Automated web reconnaissance pipeline",
        "active-ip": "Active IP range scanning and discovery",
        "breach-check": "Credential breach checking and monitoring",
        "crlfi": "CRLF injection detection and testing",
        "csprecon": "Content Security Policy analysis and bypass detection",
        "deksterecon": "Automated reconnaissance toolkit",
        "go-dork": "Google dorking tool written in Go",
        "inql": "GraphQL introspection and security testing (Burp extension)",
        "magicrecon": "Automated bug bounty reconnaissance",
        "metabigor": "OSINT tool for ASN, IP, and domain intelligence",
        "metlo": "API security testing platform",
        "pccc": "Pre-commit configuration checker",
        "portwave": "Port scanning and wave-based discovery",
        "ppfuzz": "Prototype pollution fuzzer",
        "ppmap": "Prototype pollution mapping and detection",
        "programs-watcher": "Bug bounty program monitoring",
        "bchacktool": "Blockchain security and hacking toolkit",
        "scan4all": "Comprehensive vulnerability scanner aggregator",
        "secfiles": "Security file collection and wordlists",
        "shortscan": "IIS short filename vulnerability scanner",
        "s3cxsser": "XSS detection and exploitation tool",
        "yataf": "Yet Another Tool for Android Forensics",
    }
    
    for key, purpose in purposes.items():
        if key in name_lower.replace("-", "").replace("_", ""):
            return purpose
    
    # Fallback: derive from features
    if features:
        return f"Security tool providing: {', '.join(features[:3])}"
    return "Security reference material or utility"


def analyze_all_repos():
    print("[*] RECNX Deep Repository Intelligence Analyzer")
    print(f"[*] Scanning {REPOS_DIR}...\n")
    
    profiles = []
    feature_matrix = []
    
    repos = sorted([d for d in REPOS_DIR.iterdir() if d.is_dir()])
    
    for i, repo_path in enumerate(repos, 1):
        name = repo_path.name
        print(f"[{i:02d}/50] Analyzing {name}...")
        
        language = detect_language(repo_path)
        entrypoints = find_entrypoints(repo_path)
        dependencies = find_dependencies(repo_path)
        features, readme_preview = extract_features(repo_path)
        classification = classify_repo(features, language)
        purpose = determine_purpose(name, features, readme_preview)
        
        # Determine unique features (features not commonly found)
        common = {"reporting", "workflow_automation"}
        unique = [f for f in features if f not in common]
        
        profile = {
            "repository_name": name,
            "purpose": purpose,
            "language": language,
            "dependencies": [d["file"] for d in dependencies],
            "entrypoints": entrypoints,
            "architecture": f"{language}-based {'CLI' if any(e.endswith(('.py','.go','.sh')) for e in entrypoints) else 'library'}",
            "core_features": features,
            "unique_features": unique[:5],
            "reusable_components": [],
            "classification": classification,
            "migration_recommendation": "",
        }
        
        # Determine reusable components
        if "subdomain_enumeration" in features:
            profile["reusable_components"].append("Subdomain discovery engine")
        if "xss_detection" in features:
            profile["reusable_components"].append("XSS scanner engine")
        if "vulnerability_scanning" in features:
            profile["reusable_components"].append("Vulnerability detection logic")
        if "javascript_analysis" in features:
            profile["reusable_components"].append("JS analysis engine")
        if "osint_collection" in features:
            profile["reusable_components"].append("OSINT data collector")
        if "workflow_automation" in features:
            profile["reusable_components"].append("Automation pipeline")
        if "api_testing" in features:
            profile["reusable_components"].append("API security testing")
        if "agent_framework" in features:
            profile["reusable_components"].append("AI agent framework")
        if "dorking" in features:
            profile["reusable_components"].append("Search engine dorking")
        if "breach_detection" in features:
            profile["reusable_components"].append("Breach intelligence")
        if "parameter_fuzzing" in features:
            profile["reusable_components"].append("Parameter fuzzing engine")
        
        # Migration recommendation
        if classification == "DIRECTLY_USABLE":
            profile["migration_recommendation"] = f"Import as Python module adapter in modules/{MODULE_MAPPING.get(features[0], 'recon') if features else 'recon'}/"
        elif classification == "REQUIRES_WRAPPER":
            profile["migration_recommendation"] = f"Create subprocess wrapper in modules/{MODULE_MAPPING.get(features[0], 'recon') if features else 'recon'}/"
        elif classification == "ARCHIVE_ONLY":
            profile["migration_recommendation"] = "Reference material only — no executable features to extract"
        else:
            profile["migration_recommendation"] = f"Refactor core logic into modules/{MODULE_MAPPING.get(features[0], 'recon') if features else 'recon'}/"
        
        profiles.append(profile)
        
        # Build feature matrix entries
        for feat in features:
            module = MODULE_MAPPING.get(feat, "recon")
            priority = "high" if feat in unique[:3] else "medium"
            feature_matrix.append({
                "repository": name,
                "feature": feat,
                "target": f"modules/{module}/{feat}",
                "priority": priority,
                "language": language,
                "classification": classification,
            })
    
    # Save profiles
    profiles_path = OUTPUTS_DIR / "repository_profiles.json"
    with open(profiles_path, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)
    print(f"\n[+] Saved {profiles_path} ({len(profiles)} profiles)")
    
    # Save feature matrix
    matrix_path = OUTPUTS_DIR / "feature_matrix.json"
    with open(matrix_path, "w", encoding="utf-8") as f:
        json.dump(feature_matrix, f, indent=2)
    print(f"[+] Saved {matrix_path} ({len(feature_matrix)} feature entries)")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"REPOSITORY INTELLIGENCE SUMMARY")
    print(f"{'='*60}")
    
    by_class = defaultdict(list)
    for p in profiles:
        by_class[p["classification"]].append(p["repository_name"])
    
    for cls, repos_list in by_class.items():
        print(f"\n{cls} ({len(repos_list)}):")
        for r in repos_list:
            print(f"  - {r}")
    
    # Feature coverage
    all_features = defaultdict(int)
    for entry in feature_matrix:
        all_features[entry["feature"]] += 1
    
    print(f"\n{'='*60}")
    print(f"FEATURE COVERAGE")
    print(f"{'='*60}")
    for feat, count in sorted(all_features.items(), key=lambda x: -x[1]):
        module = MODULE_MAPPING.get(feat, "recon")
        print(f"  {feat:<30} {count:>3} repos  -> modules/{module}/")
    
    return profiles, feature_matrix


if __name__ == "__main__":
    analyze_all_repos()
