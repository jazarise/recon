import os
import shutil
import glob

base_dir = "e:/ReconX/ReconXv3.0"
reports_dir = os.path.join(base_dir, "workspace", "reports")
os.makedirs(reports_dir, exist_ok=True)

deleted_files = []
plugin_cleanup_log = []


def delete_path(path, reason):
    full_path = os.path.join(base_dir, path)
    if os.path.exists(full_path):
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            os.remove(full_path)
        deleted_files.append(f"- `{path}` ({reason})")


# Step 4: Plugin Pollution Cleanup
plugin_dir = os.path.join(
    base_dir, "src", "reconx", "plugins", "cloud", "cloud_security"
)
review_queue_dir = os.path.join(base_dir, "review_queue", "cloud_security_plugins")

if os.path.exists(plugin_dir):
    os.makedirs(review_queue_dir, exist_ok=True)
    keep_plugins = {
        "amass",
        "subfinder",
        "assetfinder",
        "katana",
        "nuclei",
        "dalfox",
        "httpx",
        "ffuf",
    }
    delete_patterns = [
        "README*",
        "CHANGELOG*",
        "Dockerfile*",
        "LICENSE*",
        "CONTRIBUTING*",
    ]
    delete_strings = [
        "wechat",
        "sponsor",
        "CyberStrikeAI",
        "QR",
        "zh-CN",
        "CyberStrikeAITab",
        "cyberstrikeai",
    ]

    for item in os.listdir(plugin_dir):
        item_path = os.path.join(plugin_dir, item)
        rel_item = f"src/reconx/plugins/cloud/cloud_security/{item}"

        # Check patterns
        matched_pattern = False
        for pat in delete_patterns:
            if glob.fnmatch.fnmatch(item, pat):
                matched_pattern = True
                break

        # Check strings (case-insensitive for broad coverage)
        matched_string = False
        for s in delete_strings:
            if s.lower() in item.lower():
                matched_string = True
                break

        if matched_pattern or matched_string:
            delete_path(rel_item, "Scraped/Junk plugin artifact")
            plugin_cleanup_log.append(f"- Deleted: `{item}`")
        elif item in keep_plugins:
            plugin_cleanup_log.append(f"- Kept: `{item}` (Valid security integration)")
        else:
            # Move to review queue
            shutil.move(item_path, os.path.join(review_queue_dir, item))
            plugin_cleanup_log.append(f"- Moved to review queue: `{item}`")

# Step 5: Remove Stale Reports
delete_path("docs/reports/bandit_report.json", "Stale report")
delete_path("workspace/reports/import_validation.md", "Stale report")

# Step 6: Remove Empty Test Scaffolding
for test_file in [
    "tests/test_plugins.py",
    "tests/test_ai_engine.py",
    "tests/test_meta_brain.py",
    "tests/test_timeline.py",
]:
    full_path = os.path.join(base_dir, test_file)
    if os.path.exists(full_path) and os.path.getsize(full_path) == 0:
        delete_path(test_file, "Empty test scaffolding")

# Step 7: Remove Empty Core Modules
src_dir = os.path.join(base_dir, "src", "reconx")
placeholders = {
    os.path.normpath(os.path.join(src_dir, p, "__init__.py"))
    for p in ["core", "api", "cli", "database", "security", "plugins"]
}

empty_files_count = 0
inventory = {"KEEP": [], "DELETE": []}
if os.path.exists(src_dir):
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            full_path = os.path.join(root, f)
            norm_path = os.path.normpath(full_path)
            if os.path.getsize(full_path) == 0:
                rel_path = os.path.relpath(full_path, base_dir)
                if norm_path in placeholders:
                    inventory["KEEP"].append(rel_path)
                else:
                    inventory["DELETE"].append(rel_path)
                    delete_path(rel_path, "Empty core module")
                    empty_files_count += 1
            else:
                rel_path = os.path.relpath(full_path, base_dir)
                inventory["KEEP"].append(rel_path)

# Step 8: Dependency Cleanup
if os.path.exists(os.path.join(base_dir, "pyproject.toml")):
    delete_path("requirements.txt", "Redundant dependency source")

# Step 9: Frontend Cleanup
frontend_dir = "src/reconx/dashboard/frontend"
for target in ["node_modules", "dist", "build"]:
    delete_path(f"{frontend_dir}/{target}", "Frontend build artifact")

# Write Reports
with open(os.path.join(reports_dir, "deleted_files.md"), "w") as f:
    f.write("# Deleted Files Log\n\n")
    f.write("\n".join(deleted_files) if deleted_files else "No files deleted.")

with open(os.path.join(reports_dir, "plugin_cleanup.md"), "w") as f:
    f.write("# Plugin Cleanup Log\n\n")
    f.write(
        "\n".join(plugin_cleanup_log) if plugin_cleanup_log else "No plugins processed."
    )

with open(os.path.join(reports_dir, "inventory.md"), "w") as f:
    f.write("# Source Module Inventory\n\n## KEPT\n")
    for item in inventory["KEEP"]:
        f.write(f"- `{item}`\n")
    f.write("\n## DELETED (Empty)\n")
    for item in inventory["DELETE"]:
        f.write(f"- `{item}`\n")

# Architecture map placeholder
with open(os.path.join(reports_dir, "architecture_map.md"), "w") as f:
    f.write("# Architecture Map\n\n(Generated after cleanup)\n")
    f.write(
        "- src/reconx/\n  - core/\n  - api/\n  - cli/\n  - database/\n  - security/\n  - plugins/\n"
    )

print(
    f"Cleanup script completed. {len(deleted_files)} files/dirs deleted. {empty_files_count} empty files removed."
)
