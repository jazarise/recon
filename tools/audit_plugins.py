import os
import ast
import csv
import json
import importlib.util
import time
import multiprocessing
import unittest.mock
from pathlib import Path
from collections import defaultdict

# Setup Paths
base_dir = Path("e:/ReconX/Reconx_V_2.0.0")
plugins_dir = base_dir / "plugins"
audit_dir = base_dir / "audit" / "plugins"
audit_dir.mkdir(parents=True, exist_ok=True)

# 1. Classification Functions
def check_static_status(content):
    try:
        ast.parse(content)
    except SyntaxError:
        return "BROKEN", "SyntaxError"
    
    # Stub Check
    if "pass" in content or "NotImplementedError" in content or "TODO" in content.upper():
        return "STUB", "Placeholder code detected"
    if 'return {"status": "success"}' in content.replace("'", '"') or 'return {"status":"success"}' in content.replace("'", '"'):
        return "STUB", "Hardcoded success return"
    if 'print("Executing")' in content:
        return "STUB", "Print placeholder"
        
    # Wrapper Check
    indicators = ["subprocess.run", "subprocess.Popen", "os.system", "shutil.which"]
    if any(ind in content for ind in indicators):
        return "WRAPPER", "Launcher only"
        
    return "NATIVE", "Integrated"

def execute_plugin(plugin_path_str):
    """
    Attempt to load and execute the plugin with example.com.
    We mock subprocess/os to prevent actual system calls and hangs.
    """
    plugin_path = Path(plugin_path_str)
    try:
        spec = importlib.util.spec_from_file_location("plugin_mod", plugin_path)
        mod = importlib.util.module_from_spec(spec)
        # Mocking to prevent actual scans
        with unittest.mock.patch('subprocess.run') as m_run, \
             unittest.mock.patch('subprocess.Popen') as m_popen, \
             unittest.mock.patch('os.system') as m_os:
            spec.loader.exec_module(mod)
            if hasattr(mod, "Plugin"):
                plugin_instance = mod.Plugin()
                if hasattr(plugin_instance, "execute"):
                    # Pass context as empty dict if needed
                    try:
                        plugin_instance.execute("example.com", {})
                        return "PASS"
                    except Exception as e:
                        if isinstance(e, NotImplementedError):
                            return "FAIL"
                        return "ERROR"
            return "FAIL"
    except Exception:
        return "ERROR"

def run_with_timeout(func, args, timeout=0.5):
    pool = multiprocessing.Pool(processes=1)
    try:
        res = pool.apply_async(func, args)
        return res.get(timeout=timeout)
    except multiprocessing.context.TimeoutError:
        return "ERROR"
    except Exception:
        return "ERROR"
    finally:
        pool.terminate()

def main():
    print("[+] Starting Stage 4 Plugin Audit...")
    inventory = []
    execution_results = []
    
    # Metrics for Scorecard
    scorecard_data = []
    coverage_data = []
    duplicate_hash = defaultdict(list)
    repo_mapping = []

    total_files = 0
    # Walk directory
    for root, dirs, files in os.walk(plugins_dir):
        for f in files:
            if f in ["plugin.py", "adapter.py"]:
                total_files += 1
                full_path = Path(root) / f
                rel_path = full_path.relative_to(plugins_dir)
                category = rel_path.parts[0] if len(rel_path.parts) > 1 else "misc"
                repo_name = rel_path.parts[1] if len(rel_path.parts) > 2 else rel_path.parent.name
                plugin_name = repo_name.replace("-main", "").replace("_master", "").lower()
                
                content = full_path.read_text(encoding="utf-8", errors="ignore")
                
                # 1. Static Classification
                status, notes = check_static_status(content)
                
                # 2. Duplicate Analysis (naive length/hash)
                content_hash = hash(content)
                duplicate_hash[content_hash].append(plugin_name)
                if len(duplicate_hash[content_hash]) > 1:
                    if status != "STUB" and status != "BROKEN":
                        status = "DUPLICATE"
                        notes = f"Duplicate of {duplicate_hash[content_hash][0]}"
                
                # 3. Dynamic Execution
                # We'll only execute a subset or use strict timeout to avoid 80min runtime
                # Actually, running pool for 2400 is slow. We'll do direct call with mocks.
                try:
                    exec_res = execute_plugin(str(full_path))
                except Exception:
                    exec_res = "ERROR"
                    
                # 4. Record
                inventory.append({
                    "Plugin": plugin_name,
                    "Category": category,
                    "Repository": repo_name,
                    "FileCount": len(os.listdir(root)),
                    "Status": status,
                    "Notes": notes
                })
                
                execution_results.append({
                    "Plugin": plugin_name,
                    "ExecutionResult": exec_res
                })
                
                # Scorecard logic
                func_score = 5 if status == "NATIVE" else (3 if status == "WRAPPER" else 0)
                stab_score = 5 if exec_res == "PASS" else 0
                int_score = 5 if status == "NATIVE" else 0
                maint_score = 5 if status == "NATIVE" else 1
                total = func_score + stab_score + int_score + maint_score
                
                scorecard_data.append(f"{plugin_name} | {func_score} | {stab_score} | {int_score} | {maint_score} | {total}/20")
                
                # Repository mapping
                migration = "100% migrated" if status == "NATIVE" else ("not migrated" if status in ["STUB", "BROKEN"] else "partially migrated")
                repo_mapping.append(f"- {repo_name} -> plugins/{category}/{repo_name} ({migration})")
                
                # Coverage
                coverage_data.append(f"{category.capitalize()} | {plugin_name} | {status}")

    print(f"[+] Scanned {total_files} plugins.")

    # Generate CSVs
    def write_csv(filename, headers, rows):
        with open(audit_dir / filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

    print("[+] Writing CSV deliverables...")
    write_csv("plugin_inventory.csv", ["Plugin", "Category", "Repository", "FileCount", "Status", "Notes"], inventory)
    
    native = [i for i in inventory if i["Status"] == "NATIVE"]
    wrapper = [i for i in inventory if i["Status"] == "WRAPPER"]
    stub = [i for i in inventory if i["Status"] == "STUB"]
    broken = [i for i in inventory if i["Status"] == "BROKEN"]
    duplicate = [i for i in inventory if i["Status"] == "DUPLICATE"]
    
    write_csv("native_plugins.csv", ["Plugin", "Category", "Repository", "FileCount", "Status", "Notes"], native)
    write_csv("wrapper_plugins.csv", ["Plugin", "Category", "Repository", "FileCount", "Status", "Notes"], wrapper)
    write_csv("stub_plugins.csv", ["Plugin", "Category", "Repository", "FileCount", "Status", "Notes"], stub)
    write_csv("broken_plugins.csv", ["Plugin", "Category", "Repository", "FileCount", "Status", "Notes"], broken)
    write_csv("duplicate_plugins.csv", ["Plugin", "Category", "Repository", "FileCount", "Status", "Notes"], duplicate)
    
    with open(audit_dir / "execution_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Plugin", "ExecutionResult"])
        for r in execution_results:
            writer.writerow([r["Plugin"], r["ExecutionResult"]])
            
    # Migration candidates (HIGH priority for wrappers/stubs)
    mig_cands = []
    for i in wrapper + stub:
        mig_cands.append({"Plugin": i["Repository"], "Status": i["Status"], "Priority": "HIGH"})
    write_csv("migration_candidates.csv", ["Plugin", "Status", "Priority"], mig_cands)

    # Generate MDs
    print("[+] Writing Markdown deliverables...")
    with open(audit_dir / "plugin_scorecard.md", "w", encoding="utf-8") as f:
        f.write("# Plugin Scorecard\\n\\n")
        f.write("Plugin | Functionality | Stability | Integration | Maintainability | Total\\n")
        f.write("--- | --- | --- | --- | --- | ---\\n")
        f.write("\\n".join(scorecard_data[:100]))
        f.write("\\n... (truncated for brevity)")

    with open(audit_dir / "repository_mapping.md", "w", encoding="utf-8") as f:
        f.write("# Repository Mapping\\n\\n")
        f.write("\\n".join(repo_mapping[:200]))
        f.write("\\n... (truncated for brevity)")
        
    with open(audit_dir / "coverage_matrix.md", "w", encoding="utf-8") as f:
        f.write("# Functional Coverage Audit\\n\\n")
        f.write("Capability | Plugin | Status\\n")
        f.write("--- | --- | ---\\n")
        f.write("\\n".join(coverage_data[:200]))
        f.write("\\n... (truncated for brevity)")
        
    with open(audit_dir / "duplicate_analysis.md", "w", encoding="utf-8") as f:
        f.write("# Duplicate Analysis\\n\\n")
        f.write("Detected duplicate logic clusters:\\n")
        for k, v in duplicate_hash.items():
            if len(v) > 1:
                f.write(f"- Duplicate group ({len(v)} plugins): {', '.join(v[:5])}... -> MERGE\\n")

    print("[+] Stage 4 Audit Complete!")

if __name__ == "__main__":
    main()
