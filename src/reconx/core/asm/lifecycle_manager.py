import json
from typing import Dict, Any
from reconx.core.events.event_stream import event_stream
from reconx.core.asm.timeline_engine import timeline_engine

class LifecycleManager:
    def __init__(self):
        # Asset ID -> Current Version Info
        self.asset_versions: Dict[str, dict] = {}
        event_stream.subscribe(self.handle_event)
        
    def handle_event(self, payload: str):
        data = json.loads(payload)
        event_type = data.get("event")
        
        if event_type == "drift.detected":
            drift_data = data.get("data", {})
            drift_type = drift_data.get("type")
            asset = drift_data.get("asset", {})
            asset_id = asset.get("id")
            asset_value = asset.get("value")
            target = "system" # In real system, deduce target from asset graph
            
            if drift_type == "NEW_ASSET":
                self.asset_versions[asset_id] = {
                    "version": 1,
                    "value": asset_value,
                    "status": "active"
                }
                timeline_engine.log_change(target, "ASSET_CREATED", f"Discovered new asset: {asset_value}")
                
            elif drift_type == "MODIFIED_ASSET":
                if asset_id in self.asset_versions:
                    self.asset_versions[asset_id]["version"] += 1
                    new_version = self.asset_versions[asset_id]["version"]
                    old_value = self.asset_versions[asset_id]["value"]
                    
                    timeline_engine.log_change(
                        target, 
                        "ASSET_MODIFIED", 
                        f"Asset updated to v{new_version}. Was {old_value}, now {asset_value}"
                    )
                    self.asset_versions[asset_id]["value"] = asset_value

lifecycle_manager = LifecycleManager()
