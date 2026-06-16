from reconx.core.plugin_manager.interface import ReconXPlugin
from .collector import BigBountyReconCollector

class Plugin(ReconXPlugin):
    def __init__(self):
        super().__init__()
        self.collector = BigBountyReconCollector()

    def run(self, target: str, **kwargs) -> list:
        return self.execute(target, kwargs)

    def execute(self, target: str, options: dict) -> list:
        # Executes the OSINT dork generation for the given target
        return self.collector.collect(target)
