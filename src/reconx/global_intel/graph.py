class NetworkGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_relationship(self, source_ip: str, domain: str):
        self.nodes.add(source_ip)
        self.nodes.add(domain)
        self.edges.add(f"{source_ip} <-> {domain}")
