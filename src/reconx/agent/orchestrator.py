import asyncio
import logging
from src.reconx.agent.state import AgentState
from src.reconx.agent.planner import PlannerAgent
from src.reconx.agent.executor import ExecutionAgent
from src.reconx.agent.analyzer import AnalysisAgent

logger = logging.getLogger("reconx")

class AgentOrchestrator:
    def __init__(self):
        self.state = AgentState()
        self.planner = PlannerAgent()
        self.executor = ExecutionAgent()
        self.analyzer = AnalysisAgent()

    async def run(self, target: str, goal: str):
        logger.warning(f"Initializing Autonomous Agent against {target} with Goal: '{goal}'")
        
        plan = self.planner.generate_plan(goal)
        logger.info(f"Generated Strategic Plan: {plan}")

        for cycle, step in enumerate(plan, 1):
            if self.state.should_stop() or cycle > self.state.max_cycles:
                logger.critical(f"AUTO-STOP TRIGGERED: Diminishing returns detected after {cycle} cycles.")
                break
                
            assets_found = await self.executor.execute_step(step)
            self.state.update_findings(assets_found)
            
            analysis = self.analyzer.evaluate(assets_found, self.state)
            logger.debug(f"[ANALYSIS] {analysis}")
            
            logger.warning(f"Agent State: Coverage: {self.state.coverage_percent}% | Unique Assets: {self.state.unique_assets} | Diminishing Return Counter: {self.state.cycles_without_findings}/3")
            
        logger.warning("Autonomous execution completed.")
        return self.state
