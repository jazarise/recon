def generate_graph(relationships: list) -> dict:
    nodes = set()
    links = []
    
    for r in relationships:
        nodes.add(r.source)
        nodes.add(r.target)
        links.append({
            "source": r.source,
            "target": r.target,
            "label": r.relation
        })
        
    return {
        "nodes": [{"id": n} for n in nodes],
        "links": links
    }
