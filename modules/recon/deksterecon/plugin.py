from core.plugin_manager.interface import ReconXPlugin
from .collector import DekstereconCollector

class Plugin(ReconXPlugin):
    def __init__(self):
        super().__init__()
        self.collector = DekstereconCollector()

    def run(self, target: str, **kwargs) -> list:
        return self.collector.collect(target, **kwargs)
