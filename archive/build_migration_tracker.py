import os
import csv
from pathlib import Path

audit_dir = Path("e:/ReconX/Reconx_V_2.0.0/audit/migration")
audit_dir.mkdir(parents=True, exist_ok=True)

tracker = [
    {"Repository": "BigBountyRecon-main", "CurrentStatus": "STUB", "TargetStatus": "NATIVE", "Priority": "HIGH", "Progress": "0%"},
    {"Repository": "CyberDeck-main", "CurrentStatus": "WRAPPER", "TargetStatus": "NATIVE", "Priority": "HIGH", "Progress": "0%"},
    {"Repository": "METATRON-main", "CurrentStatus": "STUB", "TargetStatus": "NATIVE", "Priority": "HIGH", "Progress": "0%"},
    {"Repository": "AcquiFinder-main", "CurrentStatus": "WRAPPER", "TargetStatus": "NATIVE", "Priority": "HIGH", "Progress": "0%"},
    {"Repository": "Bug-Bounty-Agents-main", "CurrentStatus": "STUB", "TargetStatus": "NATIVE", "Priority": "HIGH", "Progress": "0%"},
    {"Repository": "breach-check-main", "CurrentStatus": "STUB", "TargetStatus": "NATIVE", "Priority": "HIGH", "Progress": "0%"},
    {"Repository": "csprecon-main", "CurrentStatus": "STUB", "TargetStatus": "NATIVE", "Priority": "MEDIUM", "Progress": "0%"},
    {"Repository": "active-ip-main", "CurrentStatus": "STUB", "TargetStatus": "NATIVE", "Priority": "MEDIUM", "Progress": "0%"},
    {"Repository": "s3cXSSer-main", "CurrentStatus": "STUB", "TargetStatus": "NATIVE", "Priority": "MEDIUM", "Progress": "0%"},
    {"Repository": "deksterecon-main", "CurrentStatus": "STUB", "TargetStatus": "NATIVE", "Priority": "MEDIUM", "Progress": "0%"},
    {"Repository": "awesome-hacking-lists-main", "CurrentStatus": "STUB", "TargetStatus": "ARCHIVED", "Priority": "LOW", "Progress": "0%"},
]

def write_csv(name, data, cols):
    with open(audit_dir / name, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(data)

write_csv("migration_tracker.csv", tracker, ["Repository", "CurrentStatus", "TargetStatus", "Priority", "Progress"])
write_csv("migrated_modules.csv", [], ["Repository", "CurrentStatus", "TargetStatus", "Priority", "Progress"])
write_csv("pending_modules.csv", tracker, ["Repository", "CurrentStatus", "TargetStatus", "Priority", "Progress"])
write_csv("archived_modules.csv", [], ["Repository", "CurrentStatus", "TargetStatus", "Priority", "Progress"])

print("Migration trackers generated.")
