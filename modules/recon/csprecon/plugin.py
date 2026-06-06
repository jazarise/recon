from core.plugin_manager.interface import ReconXPlugin
from .collector import CspReconCollector

class Plugin(ReconXPlugin):
    def __init__(self):
        super().__init__()
        self.collector = CspReconCollector()

    def run(self, target: str, **kwargs) -> list:
        return self.collector.collect(target, **kwargs)
