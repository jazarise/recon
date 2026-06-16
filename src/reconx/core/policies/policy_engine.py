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
                target = asset.get("value")
                asset_type = asset.get("type", "")
                
                # YAML-like policy rules implemented in Python for this MVP
                # IF new_subdomain -> web.probe
                if asset_type == "SUBDOMAIN":
                    print(f"[ASM POLICY] Policy matched: new subdomain -> launching web.probe on {target}")
                    self._launch_capability("web.probe", target)
                    
                # IF new js_file -> discovery.javascript
                elif asset_type == "JS_FILE":
                    print(f"[ASM POLICY] Policy matched: new JS file -> launching JS Extractor on {target}")
                    # self._launch_capability("discovery.javascript", target)
                    
                # IF new api endpoint -> discovery.api
                elif asset_type == "API_ENDPOINT":
                    print(f"[ASM POLICY] Policy matched: new API -> launching API Prober on {target}")
                    # self._launch_capability("discovery.api", target)

    def _launch_capability(self, capability: str, target: str):
        from core.capabilities import capability_manager
        loop = asyncio.get_running_loop()
        if loop.is_running():
            loop.run_in_executor(None, capability_manager.run, capability, target)
        else:
            capability_manager.run(capability, target)

policy_engine = PolicyEngine()
