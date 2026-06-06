import asyncio
from core.orchestrator import orchestrator

def test_run_workflow(monkeypatch):
    class MockPlugin:
        async def execute(self, target):
            from core.models.finding import Finding
            return [Finding(category="test", value="test_value")]
            
    monkeypatch.setattr(orchestrator, "get_plugin_instance", lambda name: MockPlugin())
    
    context = asyncio.run(orchestrator.run_workflow("passive_recon", "example.com"))
    
    assert context.target == "example.com"
    assert len(context.findings) == 3
    assert context.findings[0].category == "test"
