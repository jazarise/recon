import os
import csv
import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("e:/ReconX/Reconx_V_2.0.0")
AUDIT_DIR = BASE_DIR / "audit"
REPOS_DIR = BASE_DIR / "repositories"

def load_csv(filename):
    filepath = AUDIT_DIR / filename
    if not filepath.exists():
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(filename, fieldnames, data):
    with open(AUDIT_DIR / filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow({k: row.get(k, '') for k in fieldnames})

def main():
    recovery_matrix = load_csv("repository_recovery_matrix.csv")
    scorecard = load_csv("recovery_scorecard.csv")
    inventory = load_csv("repository_inventory.csv")

    repos_info = {}
    for inv in inventory:
        repos_info[inv['Repository']] = {
            'Location': inv['Location'],
            'Language': inv['Language']
        }
    for sc in scorecard:
        if sc['Repository'] in repos_info:
            repos_info[sc['Repository']]['Score'] = float(sc['Score (%)'])
            repos_info[sc['Repository']]['Status'] = sc['Status']

    # Classifications dictionary
    categories = {
        'subfinder': ('Asset Discovery', 'Subdomain Enumeration'),
        'amass': ('Asset Discovery', 'Subdomain Enumeration'),
        'active-ip': ('Asset Discovery', 'IP Enumeration'),
        'httpx': ('Web Enumeration', 'HTTP Probing'),
        'naabu': ('Port Scanning', 'Network Mapping'),
        'dalfox': ('Vulnerability Scanning', 'XSS Discovery'),
        'crlfi': ('Vulnerability Scanning', 'CRLF Injection'),
        'BigBountyRecon': ('OSINT', 'Recon Automation'),
        'AcquiFinder': ('OSINT', 'Corporate Assets'),
        'breach-check': ('OSINT', 'Credential Leaks'),
        'CyberDeck': ('Threat Intelligence', 'OSINT'),
        'Metatron': ('AI Agents', 'Data Analysis'),
        'Bug-Bounty-Agents': ('AI Agents', 'Automation'),
    }

    # Fallback classifications
    def classify_repo(name, location):
        if name in categories:
            return categories[name]
        loc = location.lower()
        if 'ai' in loc or 'agent' in loc or 'agent' in name.lower():
            return ('AI Agents', 'Automation')
        if 'web' in loc or 'crawl' in name.lower():
            return ('Web Enumeration', 'Content Discovery')
        if 'dns' in loc:
            return ('DNS Intelligence', 'Subdomain Enumeration')
        if 'vuln' in loc or 'scan' in name.lower() or 'check' in name.lower():
            return ('Vulnerability Scanning', 'Assessment')
        if 'osint' in loc:
            return ('OSINT', 'Data Gathering')
        return ('Utilities', 'Framework Components')

    # Phase 1: Repository Classification
    repo_classifications = []
    for repo, info in repos_info.items():
        primary, secondary = classify_repo(repo, info['Location'])
        repos_info[repo]['Primary'] = primary
        repos_info[repo]['Secondary'] = secondary
        repo_classifications.append({
            'Repository': repo,
            'Primary Category': primary,
            'Secondary Category': secondary,
            'Language': info['Language'],
            'Recovery Score': info.get('Score', 0),
            'Status': info.get('Status', 'Missing')
        })
    write_csv("repository_classification.csv", ['Repository', 'Primary Category', 'Secondary Category', 'Language', 'Recovery Score', 'Status'], repo_classifications)

    # Phase 2: Capability Mapping
    capabilities_matrix = []
    cap_map = defaultdict(list)
    for repo, info in repos_info.items():
        caps = [info['Primary'], info['Secondary']]
        for cap in set(caps):
            capabilities_matrix.append({
                'Capability': cap,
                'Repository': repo,
                'Priority': 'High' if info.get('Score', 0) > 50 else 'Medium',
                'Integration Value': 'High' if info.get('Score', 0) > 80 else 'Low'
            })
            cap_map[cap].append(repo)
    write_csv("capability_matrix.csv", ['Capability', 'Repository', 'Priority', 'Integration Value'], capabilities_matrix)

    # Phase 3: Dependency Analysis
    deps_analysis = []
    deps_graph = {}
    for repo, info in repos_info.items():
        lang = info['Language']
        reqs = 'None'
        if lang == 'Python': reqs = 'requirements.txt'
        elif lang == 'Go': reqs = 'go.mod'
        elif lang == 'NodeJS' or lang == 'JavaScript': reqs = 'package.json'
        
        deps_analysis.append({
            'Repository': repo,
            'Required Dependencies': reqs,
            'Optional Dependencies': 'Docker',
            'Conflicts': 'None',
            'Version Constraints': 'Latest'
        })
        deps_graph[repo] = {"language": lang, "manifest": reqs}
        
    write_csv("dependency_analysis.csv", ['Repository', 'Required Dependencies', 'Optional Dependencies', 'Conflicts', 'Version Constraints'], deps_analysis)
    with open(AUDIT_DIR / "dependency_graph.json", "w", encoding="utf-8") as f:
        json.dump(deps_graph, f, indent=4)

    # Phase 4: Duplicate Capability Detection
    overlap_analysis = []
    for cap, repos in cap_map.items():
        if len(repos) > 1:
            best_repo = max(repos, key=lambda r: repos_info[r].get('Score', 0))
            for repo in repos:
                rec = 'Keep' if repo == best_repo else 'Archive'
                overlap_analysis.append({
                    'Capability': cap,
                    'Repositories': repo,
                    'Recommendation': rec,
                    'Reason': 'Highest recovery score' if rec == 'Keep' else 'Duplicate/Lower score'
                })
    write_csv("overlap_analysis.csv", ['Capability', 'Repositories', 'Recommendation', 'Reason'], overlap_analysis)

    # Phase 5: Integration Complexity
    complexity = []
    for repo, info in repos_info.items():
        score = info.get('Score', 0)
        lang = info['Language']
        c = 'Medium'
        if score < 40: c = 'Extreme'
        elif lang not in ['Python', 'Go']: c = 'High'
        elif score > 80: c = 'Low'
        
        complexity.append({
            'Repository': repo,
            'Integration Difficulty': c,
            'Maintenance Cost': c,
            'Dependency Complexity': c,
            'Execution Complexity': c
        })
    write_csv("integration_complexity.csv", ['Repository', 'Integration Difficulty', 'Maintenance Cost', 'Dependency Complexity', 'Execution Complexity'], complexity)

    # Phase 6: Data Model Mapping
    data_models = []
    for repo, info in repos_info.items():
        cat = info['Primary']
        in_type, out_type = 'Domain', 'Finding'
        if 'Port' in cat or 'IP' in cat: in_type = 'IP'; out_type = 'Port'
        if 'Web' in cat: in_type = 'URL'; out_type = 'Technology'
        
        data_models.append({
            'Repository': repo,
            'Input Type': in_type,
            'Output Type': out_type,
            'Normalization Needed': 'Yes'
        })
    write_csv("data_model_mapping.csv", ['Repository', 'Input Type', 'Output Type', 'Normalization Needed'], data_models)

    # Phase 7: Integration Tiers
    tiers = []
    tier_lists = {1: [], 2: [], 3: [], 4: [], 5: []}
    for repo, info in repos_info.items():
        cat = info['Primary']
        score = info.get('Score', 0)
        
        if score < 20: tier = 5
        elif 'AI' in cat: tier = 4
        elif 'OSINT' in cat: tier = 3
        elif 'Vulnerability' in cat or 'Web' in cat: tier = 2
        else: tier = 1
        
        tier_lists[tier].append(repo)
        tiers.append({'Repository': repo, 'Tier': f'Tier {tier}'})
    write_csv("integration_tiers.csv", ['Repository', 'Tier'], tiers)

    # Phase 8: Integration Order Roadmap
    with open(AUDIT_DIR / "integration_roadmap.md", "w", encoding="utf-8") as f:
        f.write("# Integration Roadmap\n\n")
        f.write("## Stage 4: Tier 1 - Core Recon\n")
        for r in tier_lists[1]: f.write(f"- {r}\n")
        f.write("\n## Stage 5: Tier 2 - Web Security\n")
        for r in tier_lists[2]: f.write(f"- {r}\n")
        f.write("\n## Stage 6: Tier 3 - OSINT\n")
        for r in tier_lists[3]: f.write(f"- {r}\n")
        f.write("\n## Stage 7: Tier 4 - AI & Automation\n")
        for r in tier_lists[4]: f.write(f"- {r}\n")
        f.write("\n## Archival / Postponed: Tier 5 - Experimental\n")
        for r in tier_lists[5]: f.write(f"- {r}\n")

    # Phase 9: Archive Candidates
    archive = []
    for overlap in overlap_analysis:
        if overlap['Recommendation'] == 'Archive':
            archive.append({
                'Repository': overlap['Repositories'],
                'Reason': overlap['Reason'],
                'Replacement': [r for r in overlap_analysis if r['Capability'] == overlap['Capability'] and r['Recommendation'] == 'Keep'][0]['Repositories']
            })
    for repo, info in repos_info.items():
        if info.get('Score', 0) == 0 and not any(a['Repository'] == repo for a in archive):
            archive.append({'Repository': repo, 'Reason': 'Missing Source Code', 'Replacement': 'None'})
    write_csv("archive_candidates.csv", ['Repository', 'Reason', 'Replacement'], archive)

    # Phase 10: Strategic Value Assessment
    strat_value = []
    for repo, info in repos_info.items():
        s = info.get('Score', 0)
        val = max(1, min(10, int(s / 10)))
        strat_value.append({
            'Repository': repo,
            'Recon Value': val,
            'Bug Bounty Value': val,
            'Enterprise Value': max(1, val - 2),
            'Research Value': val,
            'Maintenance Cost': max(1, 10 - val)
        })
    write_csv("strategic_value_scorecard.csv", ['Repository', 'Recon Value', 'Bug Bounty Value', 'Enterprise Value', 'Research Value', 'Maintenance Cost'], strat_value)

    # Phase 11: Architecture Placement
    placement = []
    for repo, info in repos_info.items():
        cat = info['Primary']
        dest = 'plugins/discovery/'
        if 'DNS' in cat: dest = 'plugins/dns/'
        elif 'Web' in cat: dest = 'plugins/web/'
        elif 'Vulnerab' in cat: dest = 'plugins/vulnerabilities/'
        elif 'OSINT' in cat: dest = 'plugins/osint/'
        elif 'Cloud' in cat: dest = 'plugins/cloud/'
        elif 'AI' in cat: dest = 'plugins/ai/'
        elif 'Report' in cat: dest = 'plugins/reporting/'
        
        if any(a['Repository'] == repo for a in archive):
            dest = 'archive/'
            
        placement.append({
            'Repository': repo,
            'Destination': dest,
            'Reason': f'Mapped from {cat}' if dest != 'archive/' else 'Archived due to low score or duplication'
        })
    write_csv("architecture_placement.csv", ['Repository', 'Destination', 'Reason'], placement)

    # Phase 12: Stage 3 Completion Report
    total_repos = len(repos_info)
    core_repos = len(tier_lists[1])
    osint_repos = len(tier_lists[3])
    ai_repos = len(tier_lists[4])
    archive_repos = len(archive)
    
    total_caps = len(capabilities_matrix)
    unique_caps = len(cap_map)
    dup_caps = total_caps - unique_caps

    lang_counts = defaultdict(int)
    for i in repos_info.values():
        lang_counts[i['Language']] += 1

    with open(AUDIT_DIR / "STAGE3_COMPLETION_REPORT.md", "w", encoding="utf-8") as f:
        f.write("# STAGE 3 COMPLETION REPORT\n**Repository Classification & Integration Planning**\n\n")
        
        f.write("## Repository Summary\n")
        f.write(f"- Total Repositories: {total_repos}\n")
        f.write(f"- Core Repositories: {core_repos}\n")
        f.write(f"- OSINT Repositories: {osint_repos}\n")
        f.write(f"- AI Repositories: {ai_repos}\n")
        f.write(f"- Archive Candidates: {archive_repos}\n\n")
        
        f.write("## Capability Summary\n")
        f.write(f"- Total Capabilities: {total_caps}\n")
        f.write(f"- Duplicate Capabilities: {dup_caps}\n")
        f.write(f"- Unique Capabilities: {unique_caps}\n\n")
        
        f.write("## Dependency Summary\n")
        for l, c in lang_counts.items():
            f.write(f"- {l}: {c}\n")
        f.write("\n")
        
        f.write("## Integration Roadmap\n")
        f.write("1. Stage 4: Tier 1 (Core Recon)\n")
        f.write("2. Stage 5: Tier 2 (Web Security)\n")
        f.write("3. Stage 6: Tier 3 (OSINT)\n")
        f.write("4. Stage 7: Tier 4 (AI & Automation)\n\n")
        
        f.write("## Recommended Stage 4 Scope\n")
        f.write("The following highly scored core capabilities should be integrated first:\n")
        for r in tier_lists[1]:
            if repos_info[r].get('Score', 0) >= 80:
                f.write(f"- **{r}**\n")

    print("Stage 3 classification script completed successfully.")

if __name__ == "__main__":
    main()
