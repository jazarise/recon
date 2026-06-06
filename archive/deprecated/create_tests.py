import os
from pathlib import Path

BASE_DIR = Path("e:/ReconX/Reconx_V_2.0.0")

TESTS = {
    "tests/plugins/test_subfinder.py": """from plugins.discovery.subfinder import SubfinderPlugin
from core.schemas import Domain

def test_subfinder_plugin_validate():
    plugin = SubfinderPlugin()
    assert plugin.validate() == True

def test_subfinder_plugin_run_and_normalize():
    plugin = SubfinderPlugin()
    results = plugin.run("example.com")
    normalized = plugin.normalize(results)
    assert isinstance(normalized, list)
    if normalized:
        assert isinstance(normalized[0], Domain)
""",
    "tests/plugins/test_httpx.py": """from plugins.web.httpx import HttpxPlugin
from core.schemas import URL

def test_httpx_plugin():
    plugin = HttpxPlugin()
    assert plugin.validate() == True
    results = plugin.run("example.com")
    normalized = plugin.normalize(results)
    assert isinstance(normalized, list)
    if normalized:
        assert isinstance(normalized[0], URL)
""",
    "tests/workflows/test_recon_workflow.py": """import yaml

def test_workflow_structure():
    with open("workflows/recon.yaml", "r") as f:
        data = yaml.safe_load(f)
    assert data['name'] == 'Core Recon Workflow'
    assert 'steps' in data
    assert len(data['steps']) == 5
    assert data['steps'][0]['plugin'] == 'subfinder'
""",
    "tests/engine/test_correlation.py": """from core.engine.correlation_engine import CorrelationEngine
from core.schemas import Domain, Port

def test_correlation_engine():
    engine = CorrelationEngine()
    engine.ingest([Domain(value="example.com")])
    engine.ingest([Port(number=80)])
    
    profiles = engine.get_profiles()
    assert len(profiles) == 1
    assert profiles[0].domain == "example.com"
    assert 80 in profiles[0].ports
"""
}

def main():
    for rel_path, content in TESTS.items():
        filepath = BASE_DIR / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    print("Tests created successfully.")

if __name__ == "__main__":
    main()
