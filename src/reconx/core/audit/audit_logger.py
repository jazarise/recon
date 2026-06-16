import json
from datetime import datetime
import os

class AuditLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.log_file = os.path.join(self.log_dir, "audit.jsonl")

    def log(self, user: str, action: str, target: str, status: str = "SUCCESS", details: str = ""):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "action": action,
            "target": target,
            "status": status,
            "details": details
        }
        
        # Write to JSONL file
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
        print(f"[AUDIT] {user} executed {action} against {target} ({status})")

audit_logger = AuditLogger()
