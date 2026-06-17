import os

base_dir = "e:/ReconX/ReconXv3.0/src/reconx"
report_file = "e:/ReconX/ReconXv3.0/workspace/reports/config_audit.md"

secret_keywords = ["password", "secret", "token", "apikey", "jwt"]
url_keywords = ["localhost", "127.0.0.1", "192.168."]
cred_keywords = ["admin", "root", "password123"]

findings = {"secrets": [], "urls": [], "creds": []}

for root, _, files in os.walk(base_dir):
    for f in files:
        if not f.endswith(".py"):
            continue
        path = os.path.join(root, f)
        rel_path = os.path.relpath(path, base_dir)
        with open(path, "r", encoding="utf-8") as file:
            try:
                for line_no, line in enumerate(file, 1):
                    # We skip some obvious files to avoid false positives (e.g. testing files or the validators themselves)
                    if (
                        "secrets.py" in rel_path
                        or "passwords.py" in rel_path
                        or "redaction.py" in rel_path
                        or "settings.py" in rel_path
                    ):
                        continue

                    lower_line = line.lower()

                    # Secrets (ignore imports and variable definitions without string literals)
                    if any(k in lower_line for k in secret_keywords) and (
                        '"' in line or "'" in line
                    ):
                        # Filter out logging redaction
                        if "********" not in line:
                            findings["secrets"].append(
                                f"- {rel_path}:{line_no} -> `{line.strip()}`"
                            )

                    # URLs
                    if any(k in lower_line for k in url_keywords):
                        findings["urls"].append(
                            f"- {rel_path}:{line_no} -> `{line.strip()}`"
                        )

                    # Credentials
                    if any(k in lower_line for k in cred_keywords) and (
                        '"' in line or "'" in line
                    ):
                        findings["creds"].append(
                            f"- {rel_path}:{line_no} -> `{line.strip()}`"
                        )
            except Exception:
                pass

with open(report_file, "w", encoding="utf-8") as r:
    r.write("# Configuration Audit\n\n")
    r.write("## Hardcoded Secrets\n")
    if findings["secrets"]:
        r.write("\n".join(findings["secrets"]) + "\n\n")
    else:
        r.write("None found.\n\n")

    r.write("## Hardcoded URLs\n")
    if findings["urls"]:
        r.write("\n".join(findings["urls"]) + "\n\n")
    else:
        r.write("None found.\n\n")

    r.write("## Hardcoded Credentials\n")
    if findings["creds"]:
        r.write("\n".join(findings["creds"]) + "\n\n")
    else:
        r.write("None found.\n\n")
