import json
from core.events.event_stream import event_stream
from core.ai.context_builder import context_builder
from core.ai.risk_engine import risk_engine
from core.ai.reasoning_engine import reasoning_engine
from core.ai.action_planner import action_planner

class IntelligenceEngine:
    def __init__(self):
        event_stream.subscribe(self.handle_event)
        self.ai_insights = {}

    def handle_event(self, payload: str):
        data = json.loads(payload)
        event_type = data.get("event")
        
        # We process drift.detected to evaluate new assets
        if event_type == "drift.detected" and data.get("data", {}).get("type") == "NEW_ASSET":
            drift_data = data.get("data", {})
            asset = drift_data.get("asset", {})
            target = drift_data.get("target", "unknown")
            
            # 1. Build Context
            finding = drift_data.get("finding", {})
            context = context_builder.build({"target": target, "asset": asset, "finding": finding})
            
            # 2. Compute Risk
            risk_score = risk_engine.calculate_risk(context)
            
            # 3. Generate Reasoning & Attack Path
            reasoning = reasoning_engine.evaluate(context, risk_score)
            attack_path = reasoning_engine.generate_attack_path(context)
            
            # 4. Generate Action Plan
            plan = action_planner.plan(context, risk_score)
            
            insight = {
                "asset": asset.get("value"),
                "risk_score": risk_score,
                "reasoning": reasoning,
                "attack_path": attack_path,
                "recommended_actions": plan
            }
            
            self.ai_insights[asset.get("value")] = insight
            
            print(f"[AI CORE] Evaluated {asset.get('value')} -> Risk: {risk_score} | Plan: {len(plan)} actions")
            
            # Push insight to the UI
            event_stream.sync_emit("ai.insight_generated", insight)

intelligence_engine = IntelligenceEngine()
