from core.plugin_manager.interface import ReconXPlugin
class ToolAdapter(ReconXPlugin):
    def validate(self, options):
        pass

    def prepare(self, target, options):
        pass

    def execute(self, target, options):
        pass

    def normalize(self, raw_output):
        pass

    def cleanup(self):
        pass
