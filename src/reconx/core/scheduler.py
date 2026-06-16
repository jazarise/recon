import schedule
import time
import threading
from reconx.core.logger import logger

class Scheduler:
    def __init__(self):
        self.running = False
        self._thread = None

    def _run_pending(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._run_pending, daemon=True)
        self._thread.start()
        logger.info("Scheduler started.")

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join()
        logger.info("Scheduler stopped.")

    def schedule_daily(self, job_func, time_str="00:00"):
        schedule.every().day.at(time_str).do(job_func)
        logger.info(f"Scheduled daily job at {time_str}")

scheduler = Scheduler()
