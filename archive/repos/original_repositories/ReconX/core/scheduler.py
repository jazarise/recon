from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from core.logger import setup_logger

logger = setup_logger("Scheduler")

class ReconScheduler:
    """Enterprise scheduling system for recurring ReconX workflows."""
    
    def __init__(self, orchestrator):
        self.scheduler = AsyncIOScheduler()
        self.orchestrator = orchestrator

    def start(self):
        self.scheduler.start()
        logger.info("Scheduler started successfully.")

    def add_recurring_scan(self, job_id: str, cron_expr: str, workflow_path: str, target: str, project_name: str = "default"):
        """
        Add a scheduled scan based on a cron expression.
        e.g., cron_expr="0 0 * * *" for daily at midnight.
        """
        try:
            trigger = CronTrigger.from_crontab(cron_expr)
            self.scheduler.add_job(
                func=self._execute_scan,
                trigger=trigger,
                args=[workflow_path, target, project_name],
                id=job_id,
                replace_existing=True
            )
            logger.info(f"Scheduled scan '{job_id}' added for target {target} with cron: {cron_expr}")
            return True
        except Exception as e:
            logger.error(f"Failed to schedule scan: {e}")
            return False

    async def _execute_scan(self, workflow_path: str, target: str, project_name: str):
        logger.info(f"Executing scheduled scan for {target} on project {project_name}")
        try:
            await self.orchestrator.run_workflow(workflow_path, target, project_name=project_name)
        except Exception as e:
            logger.error(f"Scheduled scan failed: {e}")
