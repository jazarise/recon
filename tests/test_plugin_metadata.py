import pytest
import glob
import importlib
from pathlib import Path
import os

ROOT = Path(os.path.dirname(__file__)).parent
VALID_CATS = ["Discovery", "DNS", "Web", "OSINT", "Cloud", "Network", "Reporting", "Vulnerability", "Utility"]

def get_plugins():
    plugins = glob.glob(str(ROOT / "plugins" / "**" / "plugin.py"), recursive=True)
    return [os.path.relpath(p, ROOT).replace(os.sep, '.')[:-3] for p in plugins]

@pytest.mark.parametrize("plugin_mod", get_plugins()[:50]) # test subset for speed
def test_plugin_metadata(plugin_mod):
    mod = importlib.import_module(plugin_mod)
    assert hasattr(mod, "PLUGIN_NAME")
    assert hasattr(mod, "PLUGIN_VERSION")
    assert hasattr(mod, "PLUGIN_AUTHOR")
    assert hasattr(mod, "PLUGIN_CATEGORY")
    assert hasattr(mod, "PLUGIN_DESCRIPTION")
    assert hasattr(mod, "PLUGIN_TAGS")
    assert hasattr(mod, "PLUGIN_DEPENDENCIES")
    assert hasattr(mod, "PLUGIN_EXTERNAL_TOOLS")
    
    assert mod.PLUGIN_CATEGORY in VALID_CATS
    assert hasattr(mod, "run")

@pytest.mark.asyncio
async def test_plugin_output_schema():
    mod = importlib.import_module(get_plugins()[0])
    res = await mod.run("example.com", {})
    assert "success" in res
    assert "plugin" in res
    assert "target" in res
    assert "category" in res
    assert "data" in res
    assert "errors" in res
