import pytest
import shutil
from pathlib import Path
from reconx.core.plugins.exceptions import PluginValidationError
from reconx.core.plugins.loader import PLUGINS_DIR, PluginLoader
import textwrap

@pytest.fixture
def fake_plugin_dir(tmp_path):
    # Ensure it's under PLUGINS_DIR for trusted path test
    target_dir = PLUGINS_DIR / "test_safe_plugin"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    yaml_content = "name: test_safe\nversion: 1.0\nauthor: admin"
    py_content = textwrap.dedent("""
    from reconx.core.plugins.base import ReconXPlugin
    class MyPlugin(ReconXPlugin):
        async def execute(self, target): return None
    def register():
        return MyPlugin
    """)
    
    (target_dir / "plugin.yaml").write_text(yaml_content)
    (target_dir / "plugin.py").write_text(py_content)
    
    yield target_dir
    
    # Cleanup
    shutil.rmtree(target_dir, ignore_errors=True)

def test_plugin_loader_safe(fake_plugin_dir):
    plugin_cls = PluginLoader.load_plugin(fake_plugin_dir)
    assert plugin_cls.__name__ == "MyPlugin"

def test_plugin_loader_traversal(tmp_path):
    # Create a plugin OUTSIDE the trusted PLUGINS_DIR
    target_dir = tmp_path / "evil_plugin"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    with pytest.raises(PluginValidationError) as exc:
        PluginLoader.load_plugin(target_dir)
    assert "Path traversal blocked" in str(exc.value)

def test_plugin_loader_unsafe_module(fake_plugin_dir):
    # Add execution at module level
    py_file = fake_plugin_dir / "plugin.py"
    with open(py_file, "a") as f:
        f.write("\nprint('I am executing!')\n")
        
    with pytest.raises(PluginValidationError) as exc:
        PluginLoader.load_plugin(fake_plugin_dir)
    assert "execution at module level" in str(exc.value)
