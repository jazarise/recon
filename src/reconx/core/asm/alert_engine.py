import json
from datetime import datetime
from reconx.core.events.event_stream import event_stream

class AlertEngine:
    def __init__(self):
        event_stream.subscribe(self.handle_event)

    def handle_event(self, payload: str):
        data = json.loads(payload)
        event_type = data.get("event")
        
        if event_type == "drift.detected":
            drift_data = data.get("data", {})
            if drift_data.get("type") == "NEW_ASSET":
                asset = drift_data.get("asset", {})
                alert = {
                    "severity": "INFO" if asset.get("type") == "SUBDOMAIN" else "HIGH",
                    "asset": asset.get("value"),
                    "finding": f"New asset discovered: {asset.get('value')}",
                    "timestamp": datetime.now().isoformat()
                }
                print(f"[ALERT] {alert['severity']} - {alert['finding']}")
                # Emit the alert to the UI via event stream
                event_stream.sync_emit("alert.generated", alert)

alert_engine = AlertEngine()
