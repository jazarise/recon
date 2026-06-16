import pytest
import os
import glob
import importlib
from pathlib import Path

ROOT = Path(os.path.dirname(__file__)).parent

def get_plugins():
    plugins = glob.glob(str(ROOT / "plugins" / "**" / "plugin.py"), recursive=True)
    return [os.path.relpath(p, ROOT).replace(os.sep, '.')[:-3] for p in plugins]

@pytest.mark.asyncio
@pytest.mark.parametrize("plugin_mod", get_plugins()[:10]) # test a subset for speed
async def test_plugin_load_and_execute(plugin_mod):
    mod = importlib.import_module(plugin_mod)
    assert hasattr(mod, 'run')
    
    res = await mod.run("example.com", {})
    assert isinstance(res, dict)
    assert "success" in res
    assert "data" in res
