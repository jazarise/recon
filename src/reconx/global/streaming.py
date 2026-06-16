import asyncio
import logging
from src.reconx.global.timeline import TimelineEngine
from src.reconx.global.confidence import NoiseController
from src.reconx.global.predictive import PredictiveEngine

logger = logging.getLogger("reconx")

class StreamingPipeline:
    def __init__(self):
        self.timeline = TimelineEngine()
        self.predictive = PredictiveEngine()

    async def ingest_event(self, source: str, target: str, payload: list):
        logger.info(f"[STREAM] Ingesting telemetry for {target} from {source}")
        
        # 1. Noise Control
        filtered_payload = [item for item in payload if NoiseController.filter_noise(source, item)]
        
        # 2. Timeline Diffs
        diffs = self.timeline.detect_changes(target, filtered_payload)
        
        # 3. Predictive Analysis
        predictions = self.predictive.analyze_trends(diffs)
        for pred in predictions:
            logger.critical(f"[AI PREDICTION] {pred}")

        return diffs, predictions
