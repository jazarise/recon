from typing import Dict
from reconx.core.events.event_stream import event_stream
from reconx.core.models import AdapterResult


class DriftDetector:
    def __init__(self):
        # target -> set of asset values
        self.state: Dict[str, set] = {}

    def process_result(self, target: str, result: AdapterResult):
        """Compares new result against previous state to detect drift."""
        if target not in self.state:
            self.state[target] = set()

        current_assets = self.state[target]
        new_assets = set(a.value for a in result.assets)

        # Detect new assets
        added = new_assets - current_assets
        for asset_val in added:
            # Find the actual asset object
            asset_obj = next((a for a in result.assets if a.value == asset_val), None)
            if asset_obj:
                print(f"[ASM] Drift Detected: NEW_ASSET -> {asset_val}")
                event_stream.sync_emit(
                    "drift.detected",
                    {"type": "NEW_ASSET", "target": target, "asset": asset_obj.dict()},
                )

        # Update state
        self.state[target] = self.state[target].union(new_assets)


drift_detector = DriftDetector()
