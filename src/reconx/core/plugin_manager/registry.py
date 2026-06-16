class PluginRegistry:
    def __init__(self):
        self.plugins = {}

    def search(self, query: str):
        return [p for p in self.plugins if query in p]

    def install(self, name: str):
        pass
