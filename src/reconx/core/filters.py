def deduplicate_results(results: list) -> list:
    """Removes duplicate domain/IP mappings."""
    seen = set()
    cleaned = []
    for item in results:
        # Assume item is dict with 'target' key
        target = item.get("target")
        if target not in seen:
            seen.add(target)
            cleaned.append(item)
    return cleaned

def drop_dead_hosts(results: list) -> list:
    """Drops 404, 5xx, or NXDOMAIN indicators."""
    return [res for res in results if res.get("status_code", 200) not in (404, 500, 502, 503, 504)]
