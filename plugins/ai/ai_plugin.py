from core.plugin_manager.interface import ReconXPlugin
from core.engine.correlation_engine import CorrelationEngine
from core.engine.ai_engine import AIEngine

class AIPlugin(ReconXPlugin):
    name = "ai_analyzer"
    version = "1.0.0"
    description = "AI Analysis and Correlation Engine"

    def run(self, target: str, **kwargs):
        context = kwargs.get('context', {})
        results = context.get('all_results', [])
        
        engine = CorrelationEngine()
        engine.ingest(results, org_name=target)
        profiles = engine.get_profiles()
        
        ai_engine = AIEngine()
        for p in profiles:
            ai_engine.process_organization(p)
            
        # Re-inject back to context or return
        return {"profiles": [p.model_dump() for p in profiles]}
        
    def normalize(self, results):
        return []
