import os
import re
import json
import hashlib
from collections import defaultdict

ALL_FILES_DIR = "e:/ReconX/allfiles"
OUTPUT_DIR = "e:/ReconX/intelligence"

CATEGORIES = {
    "Recon": ["subdomain", "asn", "dns", "crawl", "asset", "amass", "subfinder", "httpx"],
    "Web Scanning": ["nuclei", "dalfox", "fuzz", "dirb", "gobuster", "ffuf", "sqlmap"],
    "Cloud Security": ["aws", "azure", "gcp", "kubernetes", "docker", "s3", "boto3"],
    "API Security": ["graphql", "openapi", "swagger", "rest", "api"],
    "OSINT": ["phoneinfoga", "holehe", "social", "email", "osint"],
    "Exploitation": ["sqli", "ssrf", "xss", "bypass", "privesc", "exploit", "cve"],
    "AI Systems": ["agent", "planner", "reasoning", "llm", "openai", "anthropic", "langchain", "prompt"],
    "Reporting": ["report", "dashboard", "summary", "html", "pdf", "markdown", "jinja"],
    "Orchestration": ["workflow", "scheduler", "queue", "pipeline", "celery", "rabbitmq", "kafka", "airflow", "dag"],
    "Infrastructure": ["dockerfile", "runtime", "deploy", "config", "env", "terraform", "ansible"],
    "Plugin Systems": ["plugin", "registry", "adapter", "module", "extension"],
    "CTF Automation": ["ctf", "challenge", "solver", "pwn"],
    "Burp/MCP Integrations": ["burp", "mcp", "extension", "proxy"],
    "Intelligence/Correlation": ["graph", "relation", "risk", "score", "neo4j", "correlation"]
}

def get_hash(content: str) -> str:
    # simple hash ignoring whitespaces for near-duplicates
    normalized = re.sub(r'\s+', '', content)
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

def analyze():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
    tool_inventory = []
    capability_matrix = {cat: [] for cat in CATEGORIES.keys()}
    capability_matrix["Uncategorized"] = []
    
    file_hashes = defaultdict(list)
    dependency_graph = {
        "nodes": [],
        "edges": []
    }
    execution_entrypoints = []
    
    total_files = 0
    for root, _, files in os.walk(ALL_FILES_DIR):
        for file in files:
            total_files += 1
            path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception:
                continue
            
            # Hash
            h = get_hash(content)
            file_hashes[h].append(path)
            
            content_lower = content.lower()
            name_lower = file.lower()
            
            # Determine Categories
            matched_categories = []
            for cat, keywords in CATEGORIES.items():
                for kw in keywords:
                    if kw in content_lower or kw in name_lower:
                        matched_categories.append(cat)
                        break
            
            if not matched_categories:
                matched_categories = ["Uncategorized"]
                
            # Determine Language
            lang = ext if ext else "unknown"
            
            # Execution Role / Entrypoint
            exec_type = "library"
            if "if __name__ ==" in content or "def main" in content or "func main()" in content or ext in [".sh", ".bash"]:
                exec_type = "cli_entrypoint"
                execution_entrypoints.append({
                    "file": file,
                    "path": path,
                    "type": "cli",
                    "language": lang
                })
            elif "flask" in content_lower or "fastapi" in content_lower or "app.listen" in content_lower:
                exec_type = "api_server"
                execution_entrypoints.append({
                    "file": file,
                    "path": path,
                    "type": "api",
                    "language": lang
                })
                
            # Quick Dependencies (just python imports for now to show concept)
            deps = []
            if lang == ".py":
                imports = re.findall(r'^import (\S+)|^from (\S+) import', content, re.MULTILINE)
                for imp in imports:
                    deps.append(imp[0] or imp[1])
            elif lang == ".go":
                imports = re.findall(r'"([^"]+)"', content)
                deps.extend(imports)
                
            deps = list(set(deps))
            
            # Add to inventory
            tool_entry = {
                "filename": file,
                "path": path,
                "language": lang,
                "purpose": f"Matches categories: {', '.join(matched_categories)}",
                "category": matched_categories,
                "dependencies": deps,
                "execution_type": exec_type,
                "related_tools": [] # to be filled
            }
            tool_inventory.append(tool_entry)
            
            for cat in matched_categories:
                capability_matrix[cat].append(file)
                
            # Add deps
            if deps:
                dependency_graph["nodes"].append({"id": file, "group": lang})
                for d in deps:
                    dependency_graph["edges"].append({"source": file, "target": d})
                    
    # Format duplicate map
    duplicate_map = []
    for h, paths in file_hashes.items():
        if len(paths) > 1:
            duplicate_map.append({
                "hash": h,
                "count": len(paths),
                "files": paths
            })
            
    print(f"Processed {total_files} files.")
    print(f"Found {len(duplicate_map)} duplicate groups.")
    
    with open(os.path.join(OUTPUT_DIR, "tool_inventory.json"), 'w') as f:
        json.dump(tool_inventory, f, indent=2)
        
    with open(os.path.join(OUTPUT_DIR, "capability_matrix.json"), 'w') as f:
        json.dump(capability_matrix, f, indent=2)
        
    with open(os.path.join(OUTPUT_DIR, "duplicate_map.json"), 'w') as f:
        json.dump(duplicate_map, f, indent=2)
        
    with open(os.path.join(OUTPUT_DIR, "dependency_graph.json"), 'w') as f:
        json.dump(dependency_graph, f, indent=2)
        
    with open(os.path.join(OUTPUT_DIR, "execution_entrypoints.json"), 'w') as f:
        json.dump(execution_entrypoints, f, indent=2)
        
    print("Successfully generated JSON files in", OUTPUT_DIR)

if __name__ == "__main__":
    analyze()
