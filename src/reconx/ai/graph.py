
class AttackGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_relationship(self, source: str, target: str):
        self.nodes.add(source)
        self.nodes.add(target)
        self.edges.add(f"{source} -> {target}")

    def export(self):
        return {
            "nodes": list(self.nodes),
            "edges": list(self.edges)
        }
