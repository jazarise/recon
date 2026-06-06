import json
import asyncio
from core.events.event_stream import event_stream

class PolicyEngine:
    def __init__(self):
        event_stream.subscribe(self.evaluate_policy)

    def evaluate_policy(self, payload: str):
        data = json.loads(payload)
        event_type = data.get("event")
        
        if event_type == "drift.detected":
            drift_data = data.get("data", {})
            if drift_data.get("type") == "NEW_ASSET":
                asset = drift_data.get("asset", {})
                
                # Rule: IF new_subdomain THEN web.probe
                if asset.get("type") == "SUBDOMAIN":
                    target = asset.get("value")
                    print(f"[POLICY] Policy triggered: new subdomain -> launching web.probe on {target}")
                    # Launch asynchronously so we don't block the event loop
                    from core.capabilities import capability_manager
                    loop = asyncio.get_running_loop()
                    loop.run_in_executor(None, capability_manager.run, "web.probe", target)

policy_engine = PolicyEngine()
