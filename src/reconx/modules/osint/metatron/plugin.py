from reconx.core.plugin_manager.interface import ReconXPlugin
from .collector import MetatronCollector

class Plugin(ReconXPlugin):
    def __init__(self):
        super().__init__()
        self.collector = MetatronCollector()

    def run(self, target: str, **kwargs) -> list:
        return self.collector.collect(target, **kwargs)
