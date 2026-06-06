import yaml

def test_workflow_structure():
    with open("workflows/recon.yaml", "r") as f:
        data = yaml.safe_load(f)
    assert data['name'] == 'Core Recon Workflow'
    assert 'steps' in data
    assert len(data['steps']) == 5
    assert data['steps'][0]['plugin'] == 'subfinder'
