from core.plugin_manager.interface import ReconXPlugin
from .collector import S3cXSSerCollector

class Plugin(ReconXPlugin):
    def __init__(self):
        super().__init__()
        self.collector = S3cXSSerCollector()

    def run(self, target: str, **kwargs) -> list:
        return self.collector.collect(target, **kwargs)
