#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.dependency_manager.doctor import Doctor

d = Doctor()
checks = d.run_all()
s = d.summary()

for c in checks:
    if c["status"] is True:
        tag = "PASS"
    elif c["status"] is False:
        tag = "FAIL"
    else:
        tag = "WARN"
    fix_hint = f"  -> {c['fix']}" if c.get("fix") else ""
    print(f"[{tag}] {c['name']}: {c['detail']}{fix_hint}")

print()
print(f"Total: {s['passed']} passed, {s['failed']} failed, {s['warned']} warned")
