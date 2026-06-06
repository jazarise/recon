import os
import csv
import json
from pathlib import Path

BASE_DIR = Path("e:/ReconX/Reconx_V_2.0.0")
AUDIT_DIR = BASE_DIR / "audit"
REPOS_DIR = BASE_DIR / "repositories"
INVENTORY_FILE = AUDIT_DIR / "repository_inventory.csv"

# Extensions mapping
SOURCE_EXTS = {'.py', '.go', '.rs', '.js', '.ts', '.cs', '.sh', '.c', '.cpp', '.h', '.rb', '.java'}
DOC_FILES = {'readme.md', 'readme', 'license', 'changelog.md', 'contributing.md'}
CONFIG_FILES = {'config.yaml', 'settings.yaml', 'settings.json', '.env.example', 'requirements.txt', 'package.json', 'go.mod', 'cargo.toml', 'dockerfile'}

# File classification helper
def classify_file(filepath: Path):
    name = filepath.name.lower()
    ext = filepath.suffix.lower()
    
    if ext in SOURCE_EXTS:
        if 'test' in name:
            return 'Test'
        if name in {'adapter.py', 'wrapper.py', 'plugin.py'}:
            return 'Wrapper'
        return 'Source'
    if ext == '.md' or name in DOC_FILES or 'docs' in filepath.parts:
        return 'Documentation'
    if name in CONFIG_FILES or ext in {'.yaml', '.yml', '.json', '.toml', '.xml'}:
        if name in {'plugin.yaml', 'tool.yaml'}:
            return 'Metadata'
        return 'Configuration'
    if 'test' in filepath.parts or ext == '.py' and 'test' in name:
        return 'Test'
    if ext in {'.txt', '.png', '.jpg', '.jpeg', '.svg', '.html', '.css', '.ico', '.pdf', '.sql'} or 'static' in filepath.parts or 'assets' in filepath.parts or 'templates' in filepath.parts or 'wordlists' in filepath.parts or 'signatures' in filepath.parts or 'payloads' in filepath.parts:
        if ext == '.txt' and name == 'requirements.txt':
            return 'Configuration'
        return 'Asset'
    
    return 'Unknown'

def main():
    REPOS_DIR.mkdir(parents=True, exist_ok=True)
    
    if not INVENTORY_FILE.exists():
        print(f"Inventory file not found: {INVENTORY_FILE}")
        return

    repositories = []
    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            repositories.append(row)

    # Initialize data structures for CSVs
    source_code_inventory = []
    documentation_inventory = []
    test_inventory = []
    config_inventory = []
    asset_inventory = []
    
    recovery_status_list = []
    missing_components_list = []
    scorecard_list = []
    
    repo_stats = {}

    for repo in repositories:
        repo_name = repo['Repository']
        repo_loc = BASE_DIR / repo['Location']
        
        stats = {
            'Source': 0,
            'Wrapper': 0,
            'Metadata': 0,
            'Documentation': 0,
            'Test': 0,
            'Configuration': 0,
            'Asset': 0,
            'Unknown': 0,
            'Files': []
        }
        
        if repo_loc.exists() and repo_loc.is_dir():
            for root, _, files in os.walk(repo_loc):
                if '__pycache__' in root or '.git' in root:
                    continue
                for file in files:
                    filepath = Path(root) / file
                    classification = classify_file(filepath)
                    stats[classification] += 1
                    
                    rel_path = str(filepath.relative_to(BASE_DIR))
                    
                    if classification == 'Source':
                        source_code_inventory.append({
                            'File': rel_path,
                            'Repository': repo_name,
                            'Language': filepath.suffix,
                            'Purpose': 'Core Tool Logic',
                            'Status': 'Recovered'
                        })
                    elif classification == 'Documentation':
                        documentation_inventory.append({
                            'Repository': repo_name,
                            'Documentation Type': 'Usage/Info',
                            'File': rel_path,
                            'Status': 'Recovered'
                        })
                    elif classification == 'Test':
                        test_inventory.append({
                            'Repository': repo_name,
                            'Test Type': 'Unit/Integration',
                            'File': rel_path,
                            'Status': 'Recovered'
                        })
                    elif classification == 'Configuration':
                        config_inventory.append({
                            'Repository': repo_name,
                            'Config Type': 'Settings/Dependencies',
                            'File': rel_path,
                            'Status': 'Recovered'
                        })
                    elif classification == 'Asset':
                        asset_inventory.append({
                            'Repository': repo_name,
                            'Asset Type': 'Misc',
                            'File': rel_path,
                            'Status': 'Recovered'
                        })

        repo_stats[repo_name] = stats
        
        # Determine Status
        if stats['Source'] > 5 and stats['Documentation'] > 0 and stats['Test'] > 0:
            status = "Fully Recovered"
        elif stats['Source'] > 0:
            status = "Partially Recovered"
        elif stats['Wrapper'] > 0 and stats['Source'] == 0:
            status = "Wrapper Only"
        elif stats['Metadata'] > 0 and stats['Wrapper'] == 0 and stats['Source'] == 0:
            status = "Metadata Only"
        else:
            status = "Missing"
            
        recovery_status_list.append({
            'Repository': repo_name,
            'Status': status
        })
        
        # Missing Components
        expected = ['Source', 'Documentation', 'Test', 'Configuration']
        recovered = []
        missing = []
        for comp in expected:
            if stats[comp] > 0:
                recovered.append(comp)
            else:
                missing.append(comp)
                
        if stats['Wrapper'] > 0:
            recovered.append('Wrapper')
            
        missing_components_list.append({
            'Repository': repo_name,
            'Expected Components': ', '.join(expected),
            'Recovered Components': ', '.join(recovered) if recovered else 'None',
            'Missing Components': ', '.join(missing) if missing else 'None'
        })
        
        # Scoring
        score = 0
        if stats['Source'] > 0: score += 40
        if stats['Documentation'] > 0: score += 15
        if stats['Test'] > 0: score += 15
        if stats['Configuration'] > 0: score += 10
        if stats['Asset'] > 0: score += 10
        # Dependencies (assuming config implies deps here)
        if stats['Configuration'] > 0: score += 10
        
        scorecard_list.append({
            'Repository': repo_name,
            'Score (%)': score,
            'Status': status
        })
        
        # Preservation Manifest
        manifest_dir = REPOS_DIR / repo_name
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_data = {
            "name": repo_name,
            "language": repo['Language'],
            "source_files": stats['Source'],
            "docs": stats['Documentation'],
            "tests": stats['Test'],
            "configs": stats['Configuration'],
            "assets": stats['Asset'],
            "status": status,
            "recovery_score": score
        }
        with open(manifest_dir / "repository_manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=4)

    # Generate CSVs
    def write_csv(filename, fieldnames, data):
        with open(AUDIT_DIR / filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                # filter keys to only match fieldnames
                writer.writerow({k: row.get(k, '') for k in fieldnames})

    # recovery_matrix
    matrix_data = []
    for repo in repositories:
        name = repo['Repository']
        st = repo_stats[name]
        matrix_data.append({
            'Repository Name': name,
            'Repository Location': repo['Location'],
            'Source Code Present': 'Yes' if st['Source'] > 0 else 'No',
            'Documentation Present': 'Yes' if st['Documentation'] > 0 else 'No',
            'Tests Present': 'Yes' if st['Test'] > 0 else 'No',
            'Configs Present': 'Yes' if st['Configuration'] > 0 else 'No',
            'Assets Present': 'Yes' if st['Asset'] > 0 else 'No'
        })
    write_csv('repository_recovery_matrix.csv', ['Repository Name', 'Repository Location', 'Source Code Present', 'Documentation Present', 'Tests Present', 'Configs Present', 'Assets Present'], matrix_data)
    
    write_csv('source_code_inventory.csv', ['File', 'Repository', 'Language', 'Purpose', 'Status'], source_code_inventory)
    write_csv('recovery_status.csv', ['Repository', 'Status'], recovery_status_list)
    write_csv('documentation_inventory.csv', ['Repository', 'Documentation Type', 'File', 'Status'], documentation_inventory)
    
    # Compress test inventory to counts
    test_summary = []
    for repo in repositories:
        name = repo['Repository']
        count = repo_stats[name]['Test']
        test_summary.append({
            'Repository': name,
            'Test Count': count,
            'Coverage Estimate': 'Unknown',
            'Status': 'Recovered' if count > 0 else 'Missing'
        })
    write_csv('test_inventory.csv', ['Repository', 'Test Count', 'Coverage Estimate', 'Status'], test_summary)
    
    write_csv('config_inventory.csv', ['Repository', 'Config Type', 'File', 'Status'], config_inventory)
    
    # Asset summary
    asset_summary = []
    for repo in repositories:
        name = repo['Repository']
        count = repo_stats[name]['Asset']
        if count > 0:
            asset_summary.append({
                'Repository': name,
                'Asset Type': 'Mixed',
                'Count': count,
                'Status': 'Recovered'
            })
    write_csv('asset_inventory.csv', ['Repository', 'Asset Type', 'Count', 'Status'], asset_summary)
    
    write_csv('missing_components.csv', ['Repository', 'Expected Components', 'Recovered Components', 'Missing Components'], missing_components_list)
    write_csv('recovery_scorecard.csv', ['Repository', 'Score (%)', 'Status'], scorecard_list)

    # Generate STAGE2_GAP_ANALYSIS.md
    with open(AUDIT_DIR / "STAGE2_GAP_ANALYSIS.md", "w", encoding="utf-8") as f:
        f.write("# STAGE 2 RECOVERY GAP ANALYSIS\n\n")
        
        categories = {
            "Ready For Integration": [],
            "Needs Recovery": [],
            "Needs Reconstruction": [],
            "Missing Repository": []
        }
        
        for repo in scorecard_list:
            score = repo['Score (%)']
            name = repo['Repository']
            if score >= 80:
                categories["Ready For Integration"].append(repo)
            elif score >= 40:
                categories["Needs Recovery"].append(repo)
            elif score > 0:
                categories["Needs Reconstruction"].append(repo)
            else:
                categories["Missing Repository"].append(repo)
                
        for cat_name, items in categories.items():
            f.write(f"## {cat_name}\n")
            if not items:
                f.write("No repositories in this category.\n\n")
            for item in items:
                name = item['Repository']
                score = item['Score (%)']
                mc = next(m for m in missing_components_list if m['Repository'] == name)
                
                f.write(f"### {name}\n")
                f.write(f"- **Recovery Percentage:** {score}%\n")
                f.write(f"- **What Exists:** {mc['Recovered Components']}\n")
                f.write(f"- **What Is Missing:** {mc['Missing Components']}\n")
                if cat_name == "Ready For Integration":
                    f.write(f"- **Recommended Actions:** Proceed to Stage 3 Integration.\n\n")
                elif cat_name == "Missing Repository":
                    f.write(f"- **Recommended Actions:** Locate original source repository or rewrite from scratch.\n\n")
                else:
                    f.write(f"- **Recommended Actions:** Recover missing components before full integration.\n\n")

    # Generate STAGE2_COMPLETION_REPORT.md
    total_repos = len(repositories)
    statuses = [s['Status'] for s in recovery_status_list]
    
    total_source = sum(s['Source'] for s in repo_stats.values())
    total_tests = sum(s['Test'] for s in repo_stats.values())
    total_docs = sum(s['Documentation'] for s in repo_stats.values())
    total_assets = sum(s['Asset'] for s in repo_stats.values())
    avg_score = sum(s['Score (%)'] for s in scorecard_list) / total_repos if total_repos > 0 else 0
    
    top_missing = sorted([s for s in scorecard_list if s['Score (%)'] < 100], key=lambda x: x['Score (%)'])[:10]
    ready_for_integration = [s['Repository'] for s in scorecard_list if s['Score (%)'] >= 80]
    
    with open(AUDIT_DIR / "STAGE2_COMPLETION_REPORT.md", "w", encoding="utf-8") as f:
        f.write("# STAGE 2 COMPLETION REPORT\n**Repository Recovery & Source Code Restoration**\n\n")
        
        f.write("## 1. Repository Statistics\n")
        f.write(f"- **Total Repositories:** {total_repos}\n")
        f.write(f"- **Fully Recovered:** {statuses.count('Fully Recovered')}\n")
        f.write(f"- **Partially Recovered:** {statuses.count('Partially Recovered')}\n")
        f.write(f"- **Wrapper Only:** {statuses.count('Wrapper Only')}\n")
        f.write(f"- **Metadata Only:** {statuses.count('Metadata Only')}\n")
        f.write(f"- **Missing:** {statuses.count('Missing')}\n\n")
        
        f.write("## 2. Code Statistics\n")
        f.write(f"- **Total Source Files:** {total_source}\n")
        f.write(f"- **Total Tests:** {total_tests}\n")
        f.write(f"- **Total Docs:** {total_docs}\n")
        f.write(f"- **Total Assets:** {total_assets}\n\n")
        
        f.write("## 3. Recovery Score\n")
        f.write(f"- **Average Repository Recovery %:** {avg_score:.2f}%\n\n")
        
        f.write("## 4. Top Missing Repositories (Priority Restoration)\n")
        for repo in top_missing:
            f.write(f"- **{repo['Repository']}** ({repo['Score (%)']}%)\n")
        f.write("\n")
        
        f.write("## 5. Integration Readiness (Eligible for Stage 3)\n")
        if ready_for_integration:
            for repo in ready_for_integration:
                f.write(f"- **{repo}**\n")
        else:
            f.write("None of the repositories meet the 80% threshold for immediate full integration.\n")

    print("Stage 2 recovery script completed successfully.")

if __name__ == "__main__":
    main()
