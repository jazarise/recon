import json
from datetime import datetime
from core.events.event_stream import event_stream

class AlertSystem:
    def __init__(self):
        event_stream.subscribe(self.handle_event)
        self.alerts = []

    def handle_event(self, payload: str):
        data = json.loads(payload)
        event_type = data.get("event")
        
        # We process drift and new exposures
        if event_type == "drift.detected":
            drift_data = data.get("data", {})
            if drift_data.get("type") == "NEW_ASSET":
                asset = drift_data.get("asset", {})
                
                severity = "INFO"
                value = asset.get("value", "")
                
                # Basic alert classification rules
                if "admin" in value:
                    severity = "CRITICAL"
                elif "api" in value or asset.get("type") == "API_ENDPOINT":
                    severity = "HIGH"
                elif asset.get("type") == "SECRET":
                    severity = "CRITICAL"
                    
                alert = {
                    "severity": severity,
                    "asset": value,
                    "reason": f"New exposed {asset.get('type')} detected",
                    "timestamp": datetime.now().isoformat()
                }
                
                self.alerts.append(alert)
                print(f"[ASM ALERT] {alert['severity']} - {alert['reason']} -> {alert['asset']}")
                event_stream.sync_emit("alert.generated", alert)

alert_system = AlertSystem()
