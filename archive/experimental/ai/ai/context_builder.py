class ContextBuilder:
    def build(self, event_data: dict) -> dict:
        """Constructs a reasoning context from an event."""
        # For this MVP, we treat the incoming asset/finding as the primary context
        return {
            "target": event_data.get("target", "unknown"),
            "asset": event_data.get("asset", {}),
            "finding": event_data.get("finding", {}),
            "historical_risk": [] # Placeholder for DB data
        }

context_builder = ContextBuilder()
