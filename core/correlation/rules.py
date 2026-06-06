def deduplicate_findings(findings: list) -> list:
    seen = set()
    unique_findings = []
    for f in findings:
        key = f"{f.category}:{f.value}:{getattr(f, 'source', 'unknown')}"
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)
    return unique_findings
