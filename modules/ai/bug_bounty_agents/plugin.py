from core.plugin_manager.interface import ReconXPlugin
from .collector import BugBountyAgentsCollector

class Plugin(ReconXPlugin):
    def __init__(self):
        super().__init__()
        self.collector = BugBountyAgentsCollector()

    def run(self, target: str, **kwargs) -> list:
        return self.collector.collect(target, **kwargs)
