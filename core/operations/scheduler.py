from typing import Dict

class ScheduledWorkflow:
    def __init__(self, name: str, interval: str, target: str):
        self.name = name
        self.interval = interval
        self.target = target
        self.last_run = None
        self.status = "Scheduled"

class JobScheduler:
    def __init__(self):
        self.jobs: Dict[str, ScheduledWorkflow] = {}

    def create_schedule(self, name: str, interval: str, target: str):
        self.jobs[name] = ScheduledWorkflow(name, interval, target)
        return self.jobs[name]

    def list_schedules(self):
        return list(self.jobs.values())
