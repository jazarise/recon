import os
import json
from pathlib import Path

# Load catalog
with open('e:/ReconX/Reconx_V_2.0.0/repository_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

out_dir = Path('e:/ReconX/Reconx_V_2.0.0/repository_audit')
out_dir.mkdir(exist_ok=True, parents=True)

for repo in catalog:
    name = repo['Repository Name']
    purpose = repo.get('Purpose', 'TBD')
    lang = repo.get('Language', 'TBD')
    deps = repo.get('Dependencies', 'TBD')
    features = ", ".join(repo.get('Features', []))
    reusables = ", ".join(repo.get('Reusable Components', []))
    classification = repo.get('Classification', 'TBD')
    
    with open(out_dir / f'{name}.md', 'w', encoding='utf-8') as f:
        f.write(f'# {name} Audit\n\n')
        f.write(f'- **Purpose**: {purpose}\n')
        f.write(f'- **Language**: {lang}\n')
        f.write(f'- **Dependencies**: {deps}\n')
        f.write(f'- **Core Features**: {features}\n')
        f.write('- **Unique Features**: TBD\n')
        f.write('- **Tool Integrations**: TBD\n')
        f.write('- **Execution Logic**: CLI\n')
        f.write('- **Data Models**: TBD\n')
        f.write('- **Reporting Logic**: TBD\n')
        f.write(f'- **Reusable Components**: {reusables}\n')
        f.write('- **Security Concerns**: TBD\n')
        f.write('- **Maintenance Status**: TBD\n\n')
        f.write(f'## Classification\n**{classification}**\n')

print(f'Generated {len(catalog)} audit files in repository_audit/')
